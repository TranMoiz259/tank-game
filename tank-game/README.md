# Tank Game

A multiplayer LAN-based tank game built with Python and Pygame.

## Features

- **Multiplayer LAN Support**: Play with up to 4 players on the same network
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

Look for "IPv4 Address" under your active network adapter (preferably Wi-Fi or Ethernet). Note: Use the `192.168.x.x` address if available, not `172.x.x.x`.

### Server Setup (Run Once)

**Important: Start the server BEFORE running any game clients!**

Start the dedicated server on one machine (keep this running):

```powershell
python -c "from src.server.server import Server; s = Server('YOUR_SERVER_IP', 12345); s.run()"
```

Replace `YOUR_SERVER_IP` with your server machine's IP address (e.g., `192.168.50.11`)

**Example:**
```powershell
python -c "from src.server.server import Server; s = Server('192.168.50.11', 12345); s.run()"
```

You should see: `Server started on 192.168.50.11:12345`

### Game Client Setup

**Server Machine & All Client Machines:**

Run the game:

```powershell
python src/main.py
```

## How to Play

### First Launch - Network Settings

1. **Server IP**: Enter the server machine's IP (e.g., `192.168.50.11`)
2. **Server Port**: Keep as `12345` (default)
3. Click **"Confirm"** to connect

### Main Menu

#### Creating a Room (Any Machine)
1. Click **"Create Room"**
2. A room code will be generated automatically
3. Share this code with other players
4. Wait for players to join

#### Joining a Room (Any Machine)
1. Click **"Join Room"**
2. Enter the room code provided by the host
3. Click to join

### Player Settings
- Click **"Player Settings"** to enter your player name before joining/creating a room

### Waiting Screen

Once 2+ players are in a room:
- Room code displays at the top
- Status shows "Waiting for at least 2 players to start..."
- When ready, click **"Start"**
- 3-2-1 countdown begins
- Game starts!

## Gameplay

- **Objective**: Be the last player standing
- **Kill Counter**: Displayed on screen showing your kills
- **Map Reset**: When only 1 player remains, the map regenerates and players respawn at random locations
- **Rounds**: Game continues with multiple rounds/maps

## Network Requirements

- All machines must be on the **same LAN (local network)**
- WiFi or Ethernet connection (can be mixed)
- Server machine must have a stable connection
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

**Allow Python through Firewall (permanent):**
1. Go to Windows Defender Firewall → Allow an app through firewall
2. Click "Allow another app"
3. Browse to your Python.exe installation
4. Click Add

## Troubleshooting

### Connection Issues

**Problem: "Failed to connect to server"**
- Verify server IP with `ipconfig` on server machine
- Ensure server is running: `Server started on...` message should appear
- Check firewall settings
- Confirm both machines are on same network: `ping <server_ip>`
- Make sure port 12345 is not blocked

**Problem: "Room not found"**
- Verify room code is correct
- Ensure server machine created a room BEFORE client tries to join
- Check that client connected to server successfully first

**Problem: Server shows "Client connected" but client shows "Attempting to connect"**
- Confirm server IP in client matches actual server IP
- Verify port is 12345 on both sides
- Try disconnecting and reconnecting

**Problem: Multiple clients disconnect randomly**
- Check network stability
- Verify firewall isn't blocking connections
- Ensure server machine isn't overloaded

### Testing Connection

Test connectivity from client machine:

```powershell
# Test if server is reachable
ping 192.168.50.11

# Test if port is open (replace IP)
telnet 192.168.50.11 12345
```

If telnet connects, you see a blank screen. If it fails, the server isn't listening.

### Check Server Status

On server machine:

```powershell
# Check if server is listening on port 12345
netstat -ano | findstr :12345
```

### Common Port Issues

If port 12345 is already in use:

```powershell
# Find what's using port 12345
netstat -ano | findstr :12345

# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

Or use a different port when starting the server:

```powershell
python -c "from src.server.server import Server; s = Server('192.168.50.11', 12346); s.run()"
```

Then update the port in the game's Network Settings screen.

## Project Structure

```
tank-game/
├── src/
│   ├── main.py              # Entry point
│   ├── client/
│   │   ├── menu.py          # Menu UI and game flow
│   │   ├── game.py          # Game screen and logic
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

## Quick Start Example

**Terminal 1 (Server Machine):**
```powershell
python -c "from src.server.server import Server; s = Server('192.168.50.11', 12345); s.run()"
```

**Terminal 2 (Server Machine - Game Client):**
```powershell
python src/main.py
# Enter IP: 192.168.50.11
# Enter Port: 12345
# Click Create Room → Get room code (e.g., ABC123)
```

**Terminal 3 (Client Machine):**
```powershell
python src/main.py
# Enter IP: 192.168.50.11 (server's IP)
# Enter Port: 12345
# Click Join Room → Enter code ABC123
```

Both should now see "Waiting for Players" screen. Once 2+ players are ready, click Start!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Feel free to submit issues or pull requests to improve the game. Your contributions are welcome!

## Support

For issues or questions, please open an issue on the GitHub repository.