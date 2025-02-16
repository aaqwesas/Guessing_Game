import socket
import sys
import select

def client_program(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_host, server_port))

        while True:
            # Authentication
            while True:
                username = input("Please input your username:\n")
                password = input("Please input your password:\n")
                client_socket.send(f"/login {username} {password}".encode('utf-8'))
                
                response = client_socket.recv(1024).decode('utf-8')
                if not response:
                    print("Server disconnected unexpectedly.")
                    client_socket.close()
                    sys.exit(1)
                    break

                print(response)
                if response.startswith("1001"):
                    break

                    
            while True:
                try:
                    ready_to_read, _, _ = select.select([sys.stdin, client_socket], [], [])

                    if sys.stdin in ready_to_read:
                        command = input()
                        client_socket.send(command.encode('utf-8'))

                    if client_socket in ready_to_read:
                        response = client_socket.recv(1024).decode('utf-8')
                        if not response:  # Server has closed the connection
                            client_socket.close()
                            sys.exit(1)
                            break
                        print(response)

                        if command.startswith('/exit') and response.startswith("4001"):
                            print("Client ends")
                            return

                        if response.startswith("3012"):
                            while True:
                                ready_to_read, _, _ = select.select([sys.stdin, client_socket], [], [])

                                if client_socket in ready_to_read:
                                    response = client_socket.recv(1024).decode('utf-8')
                                    if not response:
                                        print("Server disconnected unexpectedly.")
                                        client_socket.close()
                                        sys.exit(1)
                                        break
                                    print(response)
                                    if response.startswith("3021") or response.startswith("3022") or response.startswith("3023"):
                                        break

                                if sys.stdin in ready_to_read:
                                    guess = input()
                                    if guess in ["/guess true", "/guess false"]:
                                        client_socket.send(f"{guess}".encode('utf-8'))
                                    else:
                                        print("4002 Unrecognized message")
                except (ConnectionResetError, ConnectionAbortedError):
                    print("Server disconnected unexpectedly.")
                    break
                

    except (ConnectionResetError, ConnectionAbortedError):
        print("Server disconnected.")
    except KeyboardInterrupt:
            print(f"KeyboardInterrupt occur.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 GameClient.py <Server_hostname> <Server_port>")
        sys.exit(1)

    server_hostname = sys.argv[1]
    server_port = int(sys.argv[2])
    client_program(server_hostname, server_port)