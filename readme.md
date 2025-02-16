
# Multiplayer Guessing Game in Python

A Python-based multiplayer guessing game that allows two players to compete against each other over a network. The game incorporates user authentication, room management, and real-time gameplay using socket programming. Players can log in, join game rooms, and engage in a simple guessing challenge where they predict a randomly generated outcome.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Server Setup](#server-setup)
  - [Client Setup](#client-setup)
- [Gameplay Instructions](#gameplay-instructions)
- [Directory Structure](#directory-structure)
- [User Authentication](#user-authentication)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **User Authentication:** Secure login system requiring a username and password.
- **Room Management:** Players can view available game rooms and join a room with another player.
- **Real-Time Gameplay:** Once two players are in a room, they engage in a guessing game.
- **Multithreading:** Server handles multiple clients concurrently using threading.
- **Socket Programming:** Utilizes Python's socket library for network communication.
- **Graceful Handling:** Manages unexpected disconnections and server shutdowns gracefully.

## Prerequisites

- **Python 3.x:** Ensure Python is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).
- **Basic Knowledge of Terminal/Command Prompt:** Familiarity with navigating directories and running Python scripts.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Multiplayer-Guessing-Game.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd Multiplayer-Guessing-Game
   ```

3. **Prepare User Credentials**

   - Create a `UserInfo.txt` file in the project root directory.
   - Add user credentials in the format `username:password` on separate lines.

   ```plaintext
   alice:password123
   bob:securepass
   charlie:charliepwd
   ```

## Usage

The game consists of two main components: the **Server** and the **Client**. The server manages game rooms and facilitates communication between clients. Each player runs a client to connect to the server and participate in the game.

### Server Setup

1. **Navigate to the Project Directory**

   Ensure you are in the project root directory where `GameServer.py` is located.

2. **Run the Server**

   ```bash
   python3 GameServer.py <Server_port> <Path to UserInfo.txt>
   ```

   - **`<Server_port>`:** The port number on which the server will listen for incoming connections (e.g., `12345`).
   - **`<Path to UserInfo.txt>`:** The relative or absolute path to the `UserInfo.txt` file containing user credentials.

   **Example:**

   ```bash
   python3 GameServer.py 12345 UserInfo.txt
   ```

   The server will start and listen for client connections.

### Client Setup

1. **Open a New Terminal/Command Prompt**

   Each player should run their own client instance, potentially on different machines connected over a network.

2. **Navigate to the Project Directory**

   Ensure you are in the project root directory where `GameClient.py` is located.

3. **Run the Client**

   ```bash
   python3 GameClient.py <Server_hostname> <Server_port>
   ```

   - **`<Server_hostname>`:** The hostname or IP address where the server is running (e.g., `localhost` or `192.168.1.100`).
   - **`<Server_port>`:** The port number on which the server is listening (must match the server's port, e.g., `12345`).

   **Example:**

   ```bash
   python3 GameClient.py localhost 12345
   ```

## Gameplay Instructions

1. **Authentication:**

   - Upon running the client, you will be prompted to enter your **username** and **password**.
   - The client sends these credentials to the server for verification.
   - Successful authentication receives a `1001 Authentication successful` message.
   - Failed authentication receives a `1002 Authentication failed` message and prompts for re-entry.

2. **Main Menu:**

   After successful login, you can perform the following actions:

   - **List Available Rooms:**

     ```plaintext
     /list
     ```

     Retrieves the list of available game rooms and the number of players in each.

   - **Enter a Room:**

     ```plaintext
     /enter <room_number>
     ```

     Joins the specified game room (e.g., `/enter 2`). Each room can host up to two players.

   - **Exit the Game:**

     ```plaintext
     /exit
     ```

     Exits the game gracefully.

3. **Gameplay:**

   - Once two players are in the same room, the game starts.
   - Players are prompted to make a guess:

     ```plaintext
     /guess true
     ```

     or

     ```plaintext
     /guess false
     ```

   - After both players have made their guesses, the server randomly determines the outcome and notifies both players of the result:

     - `3021 You are the winner`
     - `3022 You lost this game`
     - `3023 The result is a tie`

4. **Disconnections:**

   - If a player disconnects unexpectedly, the remaining player is declared the winner automatically.

## Directory Structure

```
Multiplayer-Guessing-Game/
├── GameClient.py
├── GameServer.py
├── UserInfo.txt
└── README.md
```

- **`GameClient.py`**: Client-side script that players run to connect to the server and participate in the game.
- **`GameServer.py`**: Server-side script that manages client connections, authentication, game rooms, and game logic.
- **`UserInfo.txt`**: File containing user credentials in the format `username:password`.
- **`README.md`**: Documentation file (this file).

## User Authentication

- **User Credentials:**

  - Stored in `UserInfo.txt` with each line containing a `username:password` pair.
  - Example:

    ```plaintext
    alice:password123
    bob:securepass
    charlie:charliepwd
    ```

- **Authentication Process:**

  - Clients send `/login <username> <password>` to the server.
  - Server verifies credentials against `UserInfo.txt`.
  - Successful authentication allows the player to access game functionalities.
  - Failed authentication prompts the client to retry.

## Commands

### Client Commands

- **Login:**

  ```plaintext
  /login <username> <password>
  ```

- **List Rooms:**

  ```plaintext
  /list
  ```

- **Enter Room:**

  ```plaintext
  /enter <room_number>
  ```

- **Make a Guess:**

  ```plaintext
  /guess true
  ```

  or

  ```plaintext
  /guess false
  ```

- **Exit Game:**

  ```plaintext
  /exit
  ```

### Server Responses

- **Authentication Success:**

  ```plaintext
  1001 Authentication successful
  ```

- **Authentication Failure:**

  ```plaintext
  1002 Authentication failed
  ```

- **List Rooms Response:**

  ```plaintext
  3001 <number_of_rooms> <players_in_room_1> <players_in_room_2> ... <players_in_room_5>
  ```

- **Enter Room Responses:**

  - **Waiting for another player:**

    ```plaintext
    3011 Wait
    ```

  - **Game Started:**

    ```plaintext
    3012 Game started. Please guess true or false
    ```

  - **Room Full:**

    ```plaintext
    3013 The room is full
    ```

- **Game Results:**

  - **Winner:**

    ```plaintext
    3021 You are the winner
    ```

  - **Loser:**

    ```plaintext
    3022 You lost this game
    ```

  - **Tie:**

    ```plaintext
    3023 The result is a tie
    ```

- **Unhandled Commands:**

  ```plaintext
  4002 Unrecognized message
  ```

- **Exit Confirmation:**

  ```plaintext
  4001 Bye bye
  ```

## Contributing

Contributions are welcome! If you'd like to improve the game, fix bugs, or add new features, please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Your Changes**

4. **Commit Your Changes**

   ```bash
   git commit -m "Add feature: YourFeatureName"
   ```

5. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Open a Pull Request**

   Describe your changes and submit for review.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the terms of the license.

## Acknowledgments

- **Python Socket Programming:** Leveraged for real-time network communication between server and clients.
- **Threading Module:** Utilized to handle multiple clients concurrently on the server side.
- **Open-Source Community:** For providing valuable resources and support in developing networked applications.

---
