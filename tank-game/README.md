# Tank Game

## Overview
This is a multiplayer tank game that runs on a Local Area Network (LAN). Players can create or join game rooms, and the gameplay is inspired by the classic game Tank Trouble. The game features a menu for room management, player settings, and engaging tank battles.

## Features
- **Create or Join Room**: Players can easily create a new game room or join an existing one using a randomly generated room code.
- **Player Settings**: Customize player settings before entering the game.
- **Gameplay Mechanics**: Enjoy fast-paced tank battles with movement, shooting, and collision detection.
- **Networked Multiplayer**: Play with friends over a LAN connection.

## Project Structure
```
tank-game
├── src
│   ├── main.py               # Entry point of the application
│   ├── client
│   │   ├── __init__.py       # Client package marker
│   │   ├── menu.py           # Menu management
│   │   ├── game.py           # Gameplay mechanics
│   │   └── ui.py             # User interface management
│   ├── server
│   │   ├── __init__.py       # Server package marker
│   │   ├── server.py         # Network management and player handling
│   │   ├── room.py           # Game room representation
│   │   └── game_logic.py     # Game rules and logic
│   ├── shared
│   │   ├── __init__.py       # Shared package marker
│   │   ├── constants.py       # Game constants
│   │   ├── network.py        # Network communication functions
│   │   └── types.py          # Data types and structures
│   └── assets
│       └── config.py         # Game configuration settings
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd tank-game
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Game
To start the game, run the following command:
```
python src/main.py
```

## Gameplay Instructions
- Use the menu to create or join a room.
- Follow the on-screen instructions to customize your tank and settings.
- Enjoy the game with your friends!

## Contributing
Feel free to submit issues or pull requests to improve the game. Your contributions are welcome!