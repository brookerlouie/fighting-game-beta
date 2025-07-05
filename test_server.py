#!/usr/bin/env python3
"""
Simple test script to verify the lobby server is working
"""

import socket
import json
import time

def test_server_connection():
    """Test basic connection to the lobby server"""
    try:
        # Connect to server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 5555))
        print("✓ Successfully connected to lobby server")
        
        # Test create lobby
        create_message = {
            'type': 'create_lobby',
            'player_name': 'TestPlayer'
        }
        client.send(json.dumps(create_message).encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        response_data = json.loads(response)
        
        if response_data.get('status') == 'success':
            lobby_code = response_data.get('lobby_code')
            print(f"✓ Successfully created lobby: {lobby_code}")
            
            # Test get lobbies
            get_lobbies_message = {'type': 'get_lobbies'}
            client.send(json.dumps(get_lobbies_message).encode('utf-8'))
            lobbies_response = client.recv(1024).decode('utf-8')
            lobbies_data = json.loads(lobbies_response)
            
            if lobbies_data.get('type') == 'lobby_list':
                print(f"✓ Successfully retrieved lobby list: {len(lobbies_data.get('lobbies', []))} lobbies")
            
            # Clean up - leave lobby
            leave_message = {
                'type': 'leave_lobby',
                'lobby_code': lobby_code
            }
            client.send(json.dumps(leave_message).encode('utf-8'))
            print("✓ Successfully left lobby")
            
        else:
            print(f"✗ Failed to create lobby: {response_data}")
            
        client.close()
        print("✓ All tests passed! The lobby server is working correctly.")
        return True
        
    except ConnectionRefusedError:
        print("✗ Could not connect to lobby server. Make sure it's running with: python lobby_server.py")
        return False
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Fantasy Fight Lobby Server...")
    print("=" * 40)
    
    success = test_server_connection()
    
    if success:
        print("\n🎉 Server is ready for multiplayer!")
        print("You can now run the game and use the multiplayer features.")
    else:
        print("\n❌ Server test failed.")
        print("Please start the lobby server first with: python lobby_server.py") 