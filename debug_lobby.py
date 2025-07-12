#!/usr/bin/env python3
"""
Debug script to test lobby creation and joining
"""

import socket
import json
import threading
import time

def test_lobby_connection():
    """Test lobby creation and joining with separate connections"""
    
    # Test connection to server for host
    print("Testing connection to server for host...")
    try:
        host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_socket.settimeout(5)
        host_socket.connect(('localhost', 5555))
        print("✓ Successfully connected host to server")
    except Exception as e:
        print(f"❌ Failed to connect host: {e}")
        return False
    
    # Test creating a lobby
    print("\nTesting lobby creation...")
    create_message = {
        'type': 'create_lobby',
        'player_name': 'TestHost'
    }
    
    try:
        host_socket.send(json.dumps(create_message).encode('utf-8'))
        response_data = host_socket.recv(1024).decode('utf-8')
        response = json.loads(response_data)
        print(f"Host received: {response}")
        
        if response.get('status') == 'success':
            lobby_code = response.get('lobby_code')
            print(f"✓ Successfully created lobby: {lobby_code}")
        else:
            print("❌ Failed to create lobby")
            return False
    except Exception as e:
        print(f"❌ Error creating lobby: {e}")
        return False
    
    # Test connection to server for guest
    print("\nTesting connection to server for guest...")
    try:
        guest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        guest_socket.settimeout(5)
        guest_socket.connect(('localhost', 5555))
        print("✓ Successfully connected guest to server")
    except Exception as e:
        print(f"❌ Failed to connect guest: {e}")
        return False
    
    # Test joining the same lobby
    print(f"\nTesting joining lobby: {lobby_code}")
    join_message = {
        'type': 'join_lobby',
        'lobby_code': lobby_code,
        'player_name': 'TestGuest'
    }
    
    try:
        guest_socket.send(json.dumps(join_message).encode('utf-8'))
        response_data = guest_socket.recv(1024).decode('utf-8')
        response = json.loads(response_data)
        print(f"Guest received: {response}")
        
        if response.get('status') == 'success':
            print("✓ Successfully joined lobby")
        else:
            print(f"❌ Failed to join lobby: {response.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error joining lobby: {e}")
        return False
    
    # Check if host received guest_joined message
    print("\nChecking if host received guest_joined message...")
    try:
        host_socket.settimeout(2)  # Short timeout for this check
        response_data = host_socket.recv(1024).decode('utf-8')
        response = json.loads(response_data)
        print(f"Host received: {response}")
        
        if response.get('type') == 'guest_joined':
            print("✓ Host correctly received guest_joined message")
        else:
            print("❌ Host received unexpected message")
    except socket.timeout:
        print("⚠ Host didn't receive guest_joined message (timeout)")
    except Exception as e:
        print(f"❌ Error checking host message: {e}")
    
    host_socket.close()
    guest_socket.close()
    return True

def test_invalid_lobby():
    """Test joining a non-existent lobby"""
    print("\nTesting joining invalid lobby...")
    
    try:
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj.settimeout(5)
        socket_obj.connect(('localhost', 5555))
        
        join_message = {
            'type': 'join_lobby',
            'lobby_code': '9999',  # Non-existent lobby
            'player_name': 'TestGuest'
        }
        
        socket_obj.send(json.dumps(join_message).encode('utf-8'))
        response_data = socket_obj.recv(1024).decode('utf-8')
        response = json.loads(response_data)
        print(f"Server response: {response}")
        
        if response.get('status') == 'error' and 'not found' in response.get('message', '').lower():
            print("✓ Correctly rejected invalid lobby")
        else:
            print("❌ Unexpected response for invalid lobby")
        
        socket_obj.close()
    except Exception as e:
        print(f"❌ Error testing invalid lobby: {e}")

def test_network_config():
    """Test network configuration"""
    print("\nTesting network configuration...")
    try:
        from network_config import get_server_host, get_server_port
        host = get_server_host()
        port = get_server_port()
        print(f"Current server config: {host}:{port}")
        
        # Test connection to configured server
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj.settimeout(5)
        socket_obj.connect((host, port))
        print("✓ Successfully connected to configured server")
        socket_obj.close()
    except Exception as e:
        print(f"❌ Failed to connect to configured server: {e}")

if __name__ == "__main__":
    print("Fantasy Fight Lobby Debug Tool")
    print("=" * 40)
    
    # Test network configuration
    test_network_config()
    
    # Test valid lobby creation and joining
    if test_lobby_connection():
        print("\n✅ Lobby creation and joining test passed!")
    else:
        print("\n❌ Lobby creation and joining test failed!")
    
    # Test invalid lobby joining
    test_invalid_lobby()
    
    print("\nDebug complete!") 