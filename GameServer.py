import socket
import threading
import sys
import random

room_lock = threading.Lock()
game_rooms = {i: [] for i in range(1, 6)}
guesses = {}
player_state = {}

def handle_client(client_socket, users):
    player_room = None
    player_state[client_socket] = "AUTHENTICATING"
    try:
        while True:
            command = client_socket.recv(1024).decode('utf-8').strip()
            if player_state[client_socket] == "AUTHENTICATING" and command.startswith('/login'):
                try:
                    _, username, password = command.split()
                    if users.get(username) == password.strip():
                        client_socket.send("1001 Authentication successful".encode('utf-8'))
                        player_state[client_socket] = "IN_HALL"
                    else:
                        client_socket.send("1002 Authentication failed".encode('utf-8'))
                except ValueError:
                    client_socket.send("4002 Unrecognized message".encode('utf-8'))

            elif player_state[client_socket] == "IN_HALL" and command == '/list':
                with room_lock:
                    response = "3001 " + str(len(game_rooms)) + " " + " ".join(
                        str(len(game_rooms[i])) for i in range(1, 6)
                    )
                client_socket.send(response.encode('utf-8'))

            elif player_state[client_socket] == "IN_HALL" and command.startswith('/enter'):
                try:
                    _, room_number = command.split()
                    room_number = int(room_number)
                    if 1 <= room_number <= 5:
                        with room_lock:
                            if len(game_rooms[room_number]) < 2:
                                game_rooms[room_number].append(client_socket)
                                player_room = room_number
                                if len(game_rooms[room_number]) == 1:
                                    client_socket.send("3011 Wait".encode('utf-8'))
                                    player_state[client_socket] = "PLAYING"
                                else:
                                    player_state[client_socket] = "PLAYING"
                                    for player in game_rooms[room_number]:
                                        player.send("3012 Game started. Please guess true or false".encode('utf-8'))
                            else:
                                client_socket.send("3013 The room is full".encode('utf-8'))
                    else:
                        client_socket.send("4002 Unrecognized message".encode('utf-8'))
                except ValueError:
                    client_socket.send("4002 Unrecognized message".encode('utf-8'))

            elif player_state[client_socket] == "PLAYING" and command.startswith('/guess'):
                try:
                    _, guess = command.split()
                    valid_guesses = ["true", "false"]
                    if guess.lower() in valid_guesses:
                        with room_lock:
                            guesses[client_socket] = guess.lower()

                            if len(guesses) == 2:
                                player1, player2 = game_rooms[player_room]
                                guess1, guess2 = guesses[player1], guesses[player2]

                                if guess1 == guess2:
                                    for player in [player1, player2]:
                                        player.send("3023 The result is a tie".encode('utf-8'))
                                else:
                                    random_result = random.choice(valid_guesses)
                                    if guess1 == random_result:
                                        player1.send("3021 You are the winner".encode('utf-8'))
                                        player2.send("3022 You lost this game".encode('utf-8'))
                                    else:
                                        player1.send("3022 You lost this game".encode('utf-8'))
                                        player2.send("3021 You are the winner".encode('utf-8'))

                                game_rooms[player_room] = []
                                guesses.clear()
                                player_state[player1] = "IN_HALL"
                                player_state[player2] = "IN_HALL"
                    else:
                        client_socket.send("4002 Unrecognized message".encode('utf-8'))
                except ValueError:
                    client_socket.send("4002 Unrecognized message".encode('utf-8'))

            elif player_state[client_socket] == "IN_HALL" and command == '/exit':
                client_socket.send("4001 Bye bye".encode('utf-8'))
                break

            else:
                client_socket.send("4002 Unrecognized message".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
        handle_disconnection(client_socket, player_room)
    finally:
        client_socket.close()

def handle_disconnection(client_socket, player_room):
    if player_state.get(client_socket) == "PLAYING" and player_room is not None:
        with room_lock:
            if client_socket in game_rooms[player_room]:
                game_rooms[player_room].remove(client_socket)
            if len(game_rooms[player_room]) == 1:
                remaining_player = game_rooms[player_room][0]
                try:
                    remaining_player.send("3021 You are the winner".encode('utf-8'))
                except BrokenPipeError:
                    print("Failed to send message to the remaining player.")
                player_state[remaining_player] = "IN_HALL"
            game_rooms[player_room] = []

def load_users(file_path):
    try:
        users = {}
        with open(file_path, 'r') as f:
            for line in f:
                username, password = line.strip().split(':')
                users[username] = password
        return users
    except Exception as e:
        print(f"Error getting file: {e}")
        sys.exit(1)

def server_program(port, user_info_path):
    try:
        users = load_users(user_info_path)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        print(f"Server listening on port {port}")
    except Exception as e:
        print(f"Error occur while connecting to the server {e}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, users))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 GameServer.py <Server_port> <Path to UserInfo.txt file>")
        sys.exit(1)
    server_port = int(sys.argv[1])
    user_info_file = sys.argv[2]
    server_program(server_port, user_info_file)