#!/usr/bin/env python3
"""
Test script to verify lobby persistence
"""

import socket
import json
import time

def test_lobby_persistence():
    print("Testing lobby persistence...")
    
    # Create host connection
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.settimeout(5)
    host_socket.connect(('localhost', 5555))
    
    # Create lobby
    create_msg = {'type': 'create_lobby', 'player_name': 'TestHost'}
    host_socket.send(json.dumps(create_msg).encode('utf-8'))
    response = json.loads(host_socket.recv(1024).decode('utf-8'))
    lobby_code = response.get('lobby_code')
    print(f"Created lobby: {lobby_code}")
    
    # Guest 1 joins
    guest1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    guest1_socket.settimeout(5)
    guest1_socket.connect(('localhost', 5555))
    
    join_msg = {'type': 'join_lobby', 'lobby_code': lobby_code, 'player_name': 'Guest1'}
    guest1_socket.send(json.dumps(join_msg).encode('utf-8'))
    response = json.loads(guest1_socket.recv(1024).decode('utf-8'))
    print(f"Guest1 join result: {response}")
    
    # Guest 1 disconnects
    guest1_socket.close()
    print("Guest1 disconnected")
    
    # Wait a moment
    time.sleep(1)
    
    # Guest 2 tries to join the same lobby
    guest2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    guest2_socket.settimeout(5)
    guest2_socket.connect(('localhost', 5555))
    
    join_msg = {'type': 'join_lobby', 'lobby_code': lobby_code, 'player_name': 'Guest2'}
    guest2_socket.send(json.dumps(join_msg).encode('utf-8'))
    response = json.loads(guest2_socket.recv(1024).decode('utf-8'))
    print(f"Guest2 join result: {response}")
    
    if response.get('status') == 'success':
        print("✅ SUCCESS: Lobby persisted after guest disconnect!")
    else:
        print("❌ FAILED: Lobby was deleted when guest disconnected")
    
    # Cleanup
    host_socket.close()
    guest2_socket.close()

if __name__ == "__main__":
    test_lobby_persistence() 