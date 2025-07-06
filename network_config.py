# Network Configuration for Fantasy Fight Multiplayer
# Update these settings based on your network setup

# For local network play (same WiFi/LAN)
LOCAL_HOST = 'localhost'
LOCAL_PORT = 5555

# For Hamachi VPN play (cross-network)
# Replace 'YOUR_HAMACHI_IP' with your actual Hamachi IP address
HAMACHI_HOST = 'YOUR_HAMACHI_IP'  # e.g., '25.0.0.10'
HAMACHI_PORT = 5555

# Current connection mode
# Set to 'local' for same network, 'hamachi' for VPN
CONNECTION_MODE = 'local'

def get_server_config():
    """Get the current server configuration based on connection mode"""
    if CONNECTION_MODE == 'hamachi':
        return HAMACHI_HOST, HAMACHI_PORT
    else:
        return LOCAL_HOST, LOCAL_PORT

def get_server_host():
    """Get the current server host"""
    return get_server_config()[0]

def get_server_port():
    """Get the current server port"""
    return get_server_config()[1] 