#!/usr/bin/env python3
"""
Debug script to test the exact lobby flow
"""

import time
import threading
from multiplayer import MultiplayerClient

def test_lobby_flow():
    print("=== DEBUGGING LOBBY FLOW ===")
    
    # Create host client
    print("\n1. Creating host client...")
    host_client = MultiplayerClient('localhost', 5555)
    
    # Connect host
    print("\n2. Connecting host...")
    if not host_client.connect():
        print("❌ Failed to connect host")
        return False
    
    # Create lobby
    print("\n3. Creating lobby...")
    lobby_code = host_client.create_lobby("TestHost")
    if not lobby_code:
        print("❌ Failed to create lobby")
        return False
    
    print(f"✅ Created lobby: {lobby_code}")
    
    # Wait for listening thread to start
    print("\n4. Waiting for host listening thread...")
    time.sleep(2)
    
    # Check if host is receiving messages
    print("\n5. Testing host message reception...")
    for i in range(5):
        actions = host_client.get_pending_actions()
        print(f"   Frame {i+1}: {len(actions)} actions")
        time.sleep(0.5)
    
    # Create guest client
    print("\n6. Creating guest client...")
    guest_client = MultiplayerClient('localhost', 5555)
    
    # Connect guest
    print("\n7. Connecting guest...")
    if not guest_client.connect():
        print("❌ Failed to connect guest")
        return False
    
    # Join lobby
    print("\n8. Guest joining lobby...")
    if not guest_client.join_lobby(lobby_code, "TestGuest"):
        print("❌ Failed to join lobby")
        return False
    
    print("✅ Guest joined lobby")
    
    # Wait for host to receive message
    print("\n9. Waiting for host to receive guest_joined message...")
    time.sleep(3)
    
    # Check host's pending actions
    print("\n10. Checking host's pending actions...")
    for i in range(10):
        actions = host_client.get_pending_actions()
        print(f"   Frame {i+1}: {len(actions)} actions - {actions}")
        
        for action in actions:
            if action.get('type') == 'guest_joined':
                print(f"   ✅ Found guest_joined: {action}")
                return True
        
        time.sleep(0.5)
    
    print("❌ Host never received guest_joined message")
    return False

if __name__ == "__main__":
    if test_lobby_flow():
        print("\n✅ Lobby flow test passed!")
    else:
        print("\n❌ Lobby flow test failed!") 