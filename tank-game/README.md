# Tank Game

A multiplayer LAN-based tank game built with Python and Pygame.

## Features

- **Multiplayer LAN Support**: Play with up to multiple players on the same network
- **Room System**: Create or join game rooms with unique codes
- **Dynamic Maze Generation**: Randomly generated maze for each round
- **Kill Counter**: Track kills instead of wins
- **Auto-restart**: Map resets when only 1 player remains
- **Countdown Timer**: 3-2-1 countdown before game starts

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. Clone the repository:
```bash
git clone https://github.com/TranMoiz259/tank-game.git
cd tank-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup & Running

### Network Configuration

First, identify your machine's IP address:

**Windows:**
```powershell
ipconfig
```

Look for "IPv4 Address" under your active network adapter (preferably Wi-Fi or Ethernet).

### Server Setup (Run Once)

**Server Machine Only:**

Start the dedicated server (keep this running):

```powershell
python -c "from src.server.server import Server; s = Server('YOUR_SERVER_IP', 12345); s.run()"
```

Replace `YOUR_SERVER_IP` with your server machine's IP address (e.g., `192.168.50.11`)

Example:
```powershell
python -c "from src.server.server import Server; s = Server('192.168.50.11', 12345); s.run()"
```

### Game Client Setup

**Server Machine & Client Machines:**

Run the game:

```powershell
python src/main.py
```

## How to Play

### First Launch

1. **Network Settings Screen**
   - Answer "Are you the Server Host?"
   - **If YES** (server machine): Click checkbox, then Continue
   - **If NO** (client machine): Leave unchecked, enter server's IP address, click Continue

### Main Menu

#### Server Machine (Host)
1. Click **"Create Room"**
2. Share the displayed room code with other players
3. Wait for players to join

#### Client Machines
1. Click **"Join Room"**
2. Enter the room code from the server host
3. Click to join

### Player Settings
- Click **"Player Settings"** to enter your player name

### Game Start

Once 2+ players are in a room:
- Confirm input settings
- Click **"Start"**
- Watch the 3-2-1 countdown
- Game begins!

## Gameplay

- **Objective**: Be the last player standing
- **Kill Counter**: Displayed on screen
- **Map Reset**: When only 1 player remains, map regenerates and players respawn
- **Controls**: (To be implemented)

## Network Requirements

- All machines must be on the **same LAN (local network)**
- Firewall must allow Python or port 12345
- No internet connection required

### Firewall Setup (if needed)

**Windows - Temporarily disable firewall for testing:**
```powershell
netsh advfirewall set allprofiles state off
```

**Re-enable firewall:**
```powershell
netsh advfirewall set allprofiles state on
```

## Troubleshooting

### Connection Issues

**Problem: "Failed to connect to server"**
- Verify server machine IP with `ipconfig`
- Ensure server is running and listening
- Check firewall settings
- Confirm both machines are on same network: `ping <server_ip>`

**Problem: "Room not found"**
- Make sure server machine created a room first
- Verify you're using correct room code
- Check that both machines are connected to the same server

**Problem: Server shows "Client connected" but then "Room not found"**
- Confirm server IP and port are correct in client settings
- Ensure room was created BEFORE joining

### Testing Connection

Test connectivity from client machine:

```powershell
# Test if server is reachable
ping 192.168.50.11

# Test if port is open (replace IP)
telnet 192.168.50.11 12345
```

### Check Server Status

On server machine:

```powershell
# Check if server is listening on port 12345
netstat -ano | findstr :12345
```

## Project Structure

```
tank-game/
├── src/
│   ├── main.py              # Entry point
│   ├── client/
│   │   ├── menu.py          # Menu UI and logic
│   │   ├── game.py          # Game screen
│   │   └── ui.py            # UI components
│   ├── server/
│   │   ├── server.py        # Server implementation
│   │   ├── room.py          # Room management
│   │   └── game_logic.py    # Game logic
│   ├── shared/
│   │   ├── network.py       # Network client
│   │   ├── constants.py     # Game constants
│   │   └── types.py         # Data types
│   └── assets/
│       └── config.py        # Configuration
├── requirements.txt         # Project dependencies
├── .gitignore              # Git ignore file
├── LICENSE                 # MIT License
└── README.md               # This file
```

## Requirements

- pygame==2.6.1
- Python 3.8+

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to submit issues or pull requests to improve the game. Your contributions are welcome!

## Support

For issues or questions, please open an issue on the GitHub repository.