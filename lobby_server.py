#!/usr/bin/env python3
"""
Lobby Server for Fantasy Fight Multiplayer
Run this script to start the lobby server that handles multiplayer connections.
"""

import sys
import signal
print("DEBUG: LOBBY SERVER STARTING - USING UPDATED CODE")
from multiplayer import LobbyManager

def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully shutdown the server"""
    print("\nShutting down lobby server...")
    if lobby_manager:
        lobby_manager.stop_server()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start lobby manager
    lobby_manager = LobbyManager(host='0.0.0.0', port=5555)
    
    print("Starting Fantasy Fight Lobby Server...")
    print("Press Ctrl+C to stop the server")
    
    try:
        lobby_manager.start_server()
        
        # Keep the main thread alive
        while True:
            import time
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        lobby_manager.stop_server()
        print("Server stopped.") 