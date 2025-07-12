#!/usr/bin/env python3
"""
Test that simulates both host and guest using the actual game UI
"""

import pygame
import time
import threading
from multiplayer_ui import MultiplayerUI

def test_game_ui():
    print("=== TESTING GAME UI ===")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Create UI
    ui = MultiplayerUI(screen, clock, 800, 600)
    
    # Simulate host creating lobby
    print("\n1. Host creating lobby...")
    host_client = ui.client
    
    if not host_client.connect():
        print("❌ Failed to connect host")
        return False
    
    lobby_code = host_client.create_lobby("TestHost")
    if not lobby_code:
        print("❌ Failed to create lobby")
        return False
    
    print(f"✅ Created lobby: {lobby_code}")
    
    # Start host UI in a separate thread
    host_result: dict[str, object] = {"result": None}
    
    def host_ui_thread():
        try:
            result = ui.waiting_lobby_screen(lobby_code, "TestHost", True)
            host_result["result"] = result
        except Exception as e:
            print(f"Host UI error: {e}")
            host_result["result"] = "error"
    
    host_thread = threading.Thread(target=host_ui_thread)
    host_thread.daemon = True
    host_thread.start()
    
    # Wait a moment for host UI to start
    time.sleep(2)
    
    # Create guest
    print("\n2. Creating guest...")
    guest_client = ui.client.__class__('localhost', 5555)
    
    if not guest_client.connect():
        print("❌ Failed to connect guest")
        return False
    
    if not guest_client.join_lobby(lobby_code, "TestGuest"):
        print("❌ Failed to join lobby")
        return False
    
    print("✅ Guest joined lobby")
    
    # Wait for host to process the message
    print("\n3. Waiting for host to process guest join...")
    time.sleep(5)
    
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
        return False
    
    # Wait a bit more to see if UI updates
    print("\n4. Waiting for UI to update...")
    time.sleep(3)
    
    # Cleanup
    pygame.quit()
    
    return guest_joined_found

if __name__ == "__main__":
    if test_game_ui():
        print("\n✅ Game UI test passed!")
    else:
        print("\n❌ Game UI test failed!") 