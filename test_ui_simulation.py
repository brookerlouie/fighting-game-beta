#!/usr/bin/env python3
"""
Test that simulates the exact UI behavior
"""

import time
from multiplayer import MultiplayerClient

def simulate_ui_loop():
    print("=== SIMULATING UI LOOP ===")
    
    # Create host client (like in the game)
    host_client = MultiplayerClient('localhost', 5555)
    
    # Connect and create lobby (like in create_lobby_screen)
    if not host_client.connect():
        print("❌ Failed to connect")
        return False
    
    lobby_code = host_client.create_lobby("TestHost")
    if not lobby_code:
        print("❌ Failed to create lobby")
        return False
    
    print(f"✅ Created lobby: {lobby_code}")
    
    # Simulate the waiting_lobby_screen loop
    print("\n=== SIMULATING waiting_lobby_screen ===")
    guest_name = None
    can_start = False
    
    # Simulate 5 frames before guest joins
    print("\n--- Before guest joins ---")
    for i in range(5):
        actions = host_client.get_pending_actions()
        print(f"Frame {i+1}: guest_name={guest_name}, can_start={can_start}, actions={actions}")
        
        for action in actions:
            if action.get('type') == 'guest_joined':
                guest_name = action.get('guest_name')
                can_start = True
                print(f"  ✅ Processed guest_joined: {guest_name}")
            elif action.get('type') == 'player_left':
                guest_name = None
                can_start = False
                print(f"  Processed player_left")
        
        time.sleep(0.5)
    
    # Now create guest
    print("\n--- Creating guest ---")
    guest_client = MultiplayerClient('localhost', 5555)
    guest_client.connect()
    guest_client.join_lobby(lobby_code, "TestGuest")
    print("✅ Guest joined")
    
    # Continue simulating UI loop
    print("\n--- After guest joins ---")
    for i in range(10):
        actions = host_client.get_pending_actions()
        print(f"Frame {i+6}: guest_name={guest_name}, can_start={can_start}, actions={actions}")
        
        for action in actions:
            if action.get('type') == 'guest_joined':
                guest_name = action.get('guest_name')
                can_start = True
                print(f"  ✅ Processed guest_joined: {guest_name}")
            elif action.get('type') == 'player_left':
                guest_name = None
                can_start = False
                print(f"  Processed player_left")
        
        if can_start:
            print(f"  🎮 CAN START GAME! Guest: {guest_name}")
            return True
        
        time.sleep(0.5)
    
    print("❌ Never got can_start=True")
    return False

if __name__ == "__main__":
    if simulate_ui_loop():
        print("\n✅ UI simulation passed!")
    else:
        print("\n❌ UI simulation failed!") 