# Hamachi Setup for Fantasy Fight

## Your Network Details
- **Network Name**: fantasyfight
- **Password**: fantasyfight123
- **Status**: ✅ Network Created

## Next Steps

### 1. Get Your Hamachi IP Address
1. Open Hamachi
2. Look at your computer in the network list
3. Note the IP address (should look like `25.0.0.x` or `5.x.x.x`)
4. **Tell me this IP address so I can update the configuration**

### 2. Update Network Configuration
✅ **COMPLETED** - Your Hamachi IP has been configured:
```python
HAMACHI_HOST = '25.54.132.81'  # Your Hamachi IP address
CONNECTION_MODE = 'hamachi'     # Set to use Hamachi
```

### 3. Start the Lobby Server
Run this command in your terminal:
```bash
python lobby_server.py
```

You should see:
```
Starting Fantasy Fight Lobby Server...
Press Ctrl+C to stop the server
```

### 4. Share with Your Friend
Tell your friend to:
1. Install Hamachi
2. Join network "fantasyfight" with password "fantasyfight123"
3. Get their Hamachi IP
4. Update their `network_config.py` with your Hamachi IP
5. Start the game and join your lobby

## Testing the Connection

### For You (Host):
1. Start the lobby server
2. Start the game
3. Select "Play with Others" → "Create Lobby"
4. Enter your name
5. You'll get a 4-digit lobby code
6. Share this code with your friend

### For Your Friend (Guest):
1. Join the Hamachi network
2. Start the game
3. Select "Play with Others" → "Join Lobby"
4. Enter the lobby code you gave them
5. Enter their name
6. Both players should connect successfully

## Troubleshooting

### If Connection Fails:
1. **Check Hamachi**: Make sure both computers are in the same network
2. **Check IP Address**: Verify the Hamachi IP is correct in `network_config.py`
3. **Check Firewall**: Allow Hamachi through Windows Firewall
4. **Restart Services**: Restart Hamachi and the lobby server

### Common Issues:
- **"Failed to connect"**: Check if lobby server is running
- **"Lobby not found"**: Verify the 4-digit code is correct
- **High latency**: Normal for VPN connections, but turn-based gameplay should still work fine

## Quick Configuration Switch

To switch between local and Hamachi play:
1. Edit `network_config.py`
2. Change `CONNECTION_MODE = 'local'` to `CONNECTION_MODE = 'hamachi'`
3. Make sure `HAMACHI_HOST` has your correct Hamachi IP

---

## 🎮 You're Ready to Play!

Your game is now configured for cross-network multiplayer via Hamachi!

### For Your Friend:
Tell them to update their `network_config.py` with:
```python
HAMACHI_HOST = '25.54.132.81'  # Your Hamachi IP
CONNECTION_MODE = 'hamachi'
```

### Next Steps:
1. Start the lobby server: `python lobby_server.py`
2. Start the game and create a lobby
3. Share the 4-digit code with your friend
4. Enjoy cross-network multiplayer!

**Status**: ✅ Fully Configured and Ready! 