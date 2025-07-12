#!/usr/bin/env python3
"""
Test script to verify guest join message handling
"""

import socket
import json
import time
import threading

def test_guest_join_messages():
    print("Testing guest join message handling...")
    
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
    
    # Start listening for messages on host socket
    host_messages = []
    def listen_host():
        try:
            while True:
                data = host_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                host_messages.append(message)
                print(f"Host received: {message}")
        except Exception as e:
            print(f"Host listener error: {e}")
    
    host_thread = threading.Thread(target=listen_host)
    host_thread.daemon = True
    host_thread.start()
    
    # Wait a moment for thread to start
    time.sleep(0.5)
    
    # Guest joins
    guest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    guest_socket.settimeout(5)
    guest_socket.connect(('localhost', 5555))
    
    join_msg = {'type': 'join_lobby', 'lobby_code': lobby_code, 'player_name': 'TestGuest'}
    guest_socket.send(json.dumps(join_msg).encode('utf-8'))
    response = json.loads(guest_socket.recv(1024).decode('utf-8'))
    print(f"Guest join result: {response}")
    
    # Wait for host to receive guest_joined message
    time.sleep(1)
    
    # Check if host received guest_joined message
    guest_joined_found = False
    for msg in host_messages:
        if msg.get('type') == 'guest_joined':
            guest_joined_found = True
            print(f"✅ Host received guest_joined: {msg}")
            break
    
    if not guest_joined_found:
        print("❌ Host did not receive guest_joined message")
        print(f"Host messages received: {host_messages}")
    
    # Cleanup
    host_socket.close()
    guest_socket.close()
    
    return guest_joined_found

if __name__ == "__main__":
    if test_guest_join_messages():
        print("\n✅ Guest join message test passed!")
    else:
        print("\n❌ Guest join message test failed!") 