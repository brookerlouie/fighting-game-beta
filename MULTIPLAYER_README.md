# Fantasy Fight - Multiplayer Setup Guide

## Overview

The multiplayer system allows players to create and join lobbies to play against each other over the network. The system uses a client-server architecture where:

- **Lobby Server**: Handles lobby creation, joining, character selection coordination, and game synchronization
- **Game Clients**: Connect to the server to create/join lobbies, select characters, and play games

## Setup Instructions

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install pygame pillow
```

### 2. Start the Lobby Server

Before players can connect, you need to start the lobby server:

```bash
python lobby_server.py
```

The server will start on `0.0.0.0:5555` and display:
```
Starting Fantasy Fight Lobby Server...
Press Ctrl+C to stop the server
```

**Important**: The server must be running for multiplayer to work!

### 3. Configure Network Access

For players on different computers to connect:

1. **Find your computer's IP address**:
   - Windows: Run `ipconfig` in Command Prompt
   - Mac/Linux: Run `ifconfig` or `ip addr` in Terminal

2. **Configure firewall** to allow connections on port 5555

3. **Update the client connection** in `multiplayer_ui.py`:
   ```python
   # Change 'localhost' to your computer's IP address
   self.client = MultiplayerClient(server_host='YOUR_IP_ADDRESS', server_port=5555)
   ```

## How to Play Multiplayer

### Complete Multiplayer Flow

#### For the Host (Player 1):

1. Start the game and select **"Play with Others"**
2. Choose **"Create Lobby"**
3. Enter your name and press Enter
4. You'll receive a **4-digit lobby code** (e.g., "1234")
5. Share this code with your friend
6. **Character Selection**: Choose your character class and name
7. Wait for the guest to join and complete their selection
8. Once both players are ready, the game will automatically start

#### For the Guest (Player 2):

1. Start the game and select **"Play with Others"**
2. Choose **"Join Lobby"**
3. Enter the 4-digit lobby code your friend gave you
4. Enter your name and press Enter
5. **Character Selection**: Choose your character class and name
6. Wait for the host to complete their selection
7. Once both players are ready, the game will automatically start

### Character Selection in Multiplayer

The multiplayer system now includes **synchronized character selection**:

- **Real-time Coordination**: Both players choose characters simultaneously
- **Class Filtering**: If one player selects a class, it's automatically removed from the other player's options
- **Custom Names**: Each player can set their own character name
- **Visual Feedback**: See your selection and wait for the other player
- **Coordinated Start**: Game only begins when both players have completed selection

#### Character Selection Controls:
- **A/D** or **Left/Right**: Navigate between available classes
- **Enter**: Confirm class selection
- **Type**: Enter custom character name
- **Enter**: Confirm name and complete selection

### Alternative: Browse Available Lobbies

Instead of using a code, you can:

1. Select **"Browse Lobbies"** from the multiplayer menu
2. See a list of all available lobbies
3. Select one and enter your name to join
4. Proceed through character selection

## Network Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Player 1      │    │   Lobby Server  │    │   Player 2      │
│   (Host)        │◄──►│   (Port 5555)   │◄──►│   (Guest)       │
│                 │    │                 │    │                 │
│ - Creates lobby │    │ - Manages       │    │ - Joins lobby   │
│ - Gets code     │    │   lobbies       │    │ - Uses code     │
│ - Chooses char  │    │ - Coordinates   │    │ - Chooses char  │
│ - Waits for P2  │    │   char selection│    │ - Waits for P1  │
└─────────────────┘    │ - Forwards      │    └─────────────────┘
                       │   game actions  │
                       └─────────────────┘
```

## Lobby System Features

### Lobby Management
- **4-digit numeric codes** for easy sharing
- **Player Limits**: Maximum 2 players per lobby
- **Auto-Cleanup**: Lobbies are removed when players leave
- **Real-time Updates**: Players are notified when others join/leave

### Character Selection Coordination
- **Synchronized Selection**: Both players choose simultaneously
- **Class Deduplication**: Prevents duplicate character classes
- **Name Customization**: Each player sets their character name
- **Ready State Tracking**: Server knows when both players are ready
- **Automatic Game Start**: Game begins when both selections are complete

### Game Synchronization
- **Action Forwarding**: Game actions are sent to the other player
- **Turn Management**: Turn-based gameplay is synchronized
- **State Updates**: Health, abilities, and game state are shared

## Multiplayer Game Flow

### Phase 1: Lobby Creation
1. Host creates lobby → Gets 4-digit code
2. Guest joins lobby → Both players connected
3. Server tracks lobby state and player connections

### Phase 2: Character Selection
1. Both players enter character selection screen
2. Real-time class filtering prevents duplicates
3. Each player chooses class and custom name
4. Server coordinates when both are ready
5. Game start signal sent to both players

### Phase 3: Game Play
1. Game starts with selected characters
2. Turn-based combat with synchronized actions
3. Real-time health and status effect updates
4. Game continues until one player wins

## Troubleshooting

### Common Issues

1. **"Failed to connect to server"**
   - Make sure the lobby server is running
   - Check if the IP address is correct
   - Verify firewall settings

2. **"Lobby not found"**
   - Verify the 4-digit code is correct
   - Check if the lobby still exists (may have timed out)
   - Ensure the server is running

3. **"Connection timeout"**
   - Check network connectivity
   - Verify port 5555 is open
   - Try restarting the server

4. **Character selection stuck**
   - Check if both players are connected
   - Try refreshing the lobby
   - Restart the game if needed

5. **Can't join from different network**
   - Configure port forwarding on router (port 5555)
   - Use a VPN service like Hamachi
   - Check firewall settings

### Server Issues

1. **Server crashes or freezes**
   - Delete `__pycache__` folders
   - Restart the server with `python -B lobby_server.py`
   - Check for Python path issues

2. **Socket timeout errors**
   - Server has built-in timeout handling
   - Check network stability
   - Verify client connections

### Network Setup for Internet Play

#### Option 1: Port Forwarding
1. Find your public IP address (whatismyipaddress.com)
2. Access your router's admin panel
3. Set up port forwarding for port 5555 to your computer
4. Update client connection settings with your public IP

#### Option 2: VPN Services
- **Hamachi**: Free virtual LAN service
- **ZeroTier**: Free tier available
- **ngrok**: For testing (creates tunnel)

#### Option 3: Local Network
- Works automatically on same WiFi/LAN
- No additional setup required

## Advanced Configuration

### Custom Server Settings
Edit `lobby_server.py` to change:
- Server port (default: 5555)
- Host address (default: 0.0.0.0)
- Lobby timeout settings
- Maximum players per lobby

### Client Connection Settings
Edit `multiplayer_ui.py` to change:
- Default server host
- Connection timeout values
- Retry logic

### Debug Mode
Enable debug prints by setting:
```python
DEBUG = True
```
in the relevant files to see detailed connection information.

## Performance Tips

1. **Local Network**: Best performance, no latency issues
2. **Internet Play**: May have slight latency, but turn-based nature minimizes impact
3. **Server Location**: Host server closer to players for better performance
4. **Network Quality**: Stable internet connection recommended

## Security Considerations

- The current system is designed for friendly play
- No authentication or encryption implemented
- Use trusted networks or VPNs for security
- Consider firewall rules for public servers

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Test with local network first
4. Check server logs for error messages
5. Ensure both players are using the same game version

For additional help, refer to the main `README.md` or contact the developers.

## Future Enhancements

Potential improvements for the multiplayer system:

1. **Authentication**: Player accounts and login system
2. **Encryption**: Secure communication between clients and server
3. **Matchmaking**: Automatic pairing of players
4. **Spectator Mode**: Allow others to watch games
5. **Tournament System**: Organized competitions
6. **Replay System**: Save and replay games
7. **Chat System**: In-game communication
8. **Custom Lobbies**: Private lobbies with passwords

## Technical Details

### Protocol

The multiplayer system uses JSON messages over TCP:

```json
{
  "type": "create_lobby",
  "player_name": "Player1"
}
```

### Message Types

- `create_lobby`: Create a new lobby
- `join_lobby`: Join an existing lobby
- `get_lobbies`: Get list of available lobbies
- `game_action`: Send game action to other player
- `leave_lobby`: Leave current lobby

### Port Configuration

- **Default Port**: 5555
- **Protocol**: TCP
- **Host**: 0.0.0.0 (accepts connections from any IP)

To change the port, modify both `lobby_server.py` and `multiplayer_ui.py`. 