#!/usr/bin/env python3
"""
Test using actual MultiplayerClient to verify message handling
"""

import time
from multiplayer import MultiplayerClient

def test_client_message_handling():
    print("Testing MultiplayerClient message handling...")
    
    # Create host client
    host_client = MultiplayerClient('localhost', 5555)
    
    # Connect and create lobby
    if not host_client.connect():
        print("❌ Failed to connect host")
        return False
    
    lobby_code = host_client.create_lobby("TestHost")
    if not lobby_code:
        print("❌ Failed to create lobby")
        return False
    
    print(f"✅ Created lobby: {lobby_code}")
    
    # Wait a moment for the listening thread to start
    time.sleep(1)
    
    # Create guest client
    guest_client = MultiplayerClient('localhost', 5555)
    
    # Connect and join lobby
    if not guest_client.connect():
        print("❌ Failed to connect guest")
        return False
    
    if not guest_client.join_lobby(lobby_code, "TestGuest"):
        print("❌ Failed to join lobby")
        return False
    
    print("✅ Guest joined lobby")
    
    # Wait for host to receive guest_joined message
    time.sleep(2)
    
    # Check if host received the message
    actions = host_client.get_pending_actions()
    print(f"Host pending actions: {actions}")
    
    guest_joined_found = False
    for action in actions:
        if action.get('type') == 'guest_joined':
            guest_joined_found = True
            print(f"✅ Host received guest_joined: {action}")
            break
    
    if not guest_joined_found:
        print("❌ Host did not receive guest_joined message")
    
    # Cleanup
    host_client.disconnect()
    guest_client.disconnect()
    
    return guest_joined_found

if __name__ == "__main__":
    if test_client_message_handling():
        print("\n✅ Client message handling test passed!")
    else:
        print("\n❌ Client message handling test failed!") 