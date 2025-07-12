#!/usr/bin/env python3
"""
Test the UI flow to see if guest join messages are processed correctly
"""

import time
from multiplayer import MultiplayerClient

def test_ui_flow():
    print("Testing UI flow...")
    
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
    
    # Simulate the UI checking for pending actions
    print("\n--- Simulating UI loop ---")
    for i in range(10):  # Simulate 10 UI frames
        actions = host_client.get_pending_actions()
        print(f"Frame {i+1}: Got {len(actions)} pending actions: {actions}")
        
        if actions:
            for action in actions:
                if action.get('type') == 'guest_joined':
                    print(f"✅ Found guest_joined action: {action}")
                    return True
        
        time.sleep(0.5)  # Simulate frame time
    
    # Now create guest
    print("\n--- Creating guest ---")
    guest_client = MultiplayerClient('localhost', 5555)
    
    if not guest_client.connect():
        print("❌ Failed to connect guest")
        return False
    
    if not guest_client.join_lobby(lobby_code, "TestGuest"):
        print("❌ Failed to join lobby")
        return False
    
    print("✅ Guest joined lobby")
    
    # Continue simulating UI loop
    print("\n--- Continuing UI loop after guest joined ---")
    for i in range(10):  # Simulate 10 more UI frames
        actions = host_client.get_pending_actions()
        print(f"Frame {i+11}: Got {len(actions)} pending actions: {actions}")
        
        if actions:
            for action in actions:
                if action.get('type') == 'guest_joined':
                    print(f"✅ Found guest_joined action: {action}")
                    guest_name = action.get('guest_name')
                    print(f"✅ Guest name: {guest_name}")
                    return True
        
        time.sleep(0.5)  # Simulate frame time
    
    print("❌ Never found guest_joined action")
    return False

if __name__ == "__main__":
    if test_ui_flow():
        print("\n✅ UI flow test passed!")
    else:
        print("\n❌ UI flow test failed!") 