import pygame
import sys
from multiplayer import MultiplayerClient
from network_config import get_server_host, get_server_port

class MultiplayerUI:
    def __init__(self, screen, clock, width, height):
        self.screen = screen
        self.clock = clock
        self.width = width
        self.height = height
        self.client = MultiplayerClient(server_host=get_server_host(), server_port=get_server_port())
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
    def show_multiplayer_menu(self):
        """Show the main multiplayer menu"""
        selected_option = 0
        options = ["Create Lobby", "Join Lobby", "Browse Lobbies", "Back to Main Menu"]
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Create Lobby
                            return self.create_lobby_screen()
                        elif selected_option == 1:  # Join Lobby
                            return self.join_lobby_screen()
                        elif selected_option == 2:  # Browse Lobbies
                            return self.browse_lobbies_screen()
                        elif selected_option == 3:  # Back
                            return "back"
            
            # Draw background
            self.screen.fill((100, 150, 255))
            
            # Draw title
            title = self.font_large.render("MULTIPLAYER", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width // 2, 150))
            self.screen.blit(title, title_rect)
            
            # Draw options
            for i, option in enumerate(options):
                color = (255, 255, 0) if i == selected_option else (255, 255, 255)
                text = self.font_medium.render(option, True, color)
                text_rect = text.get_rect(center=(self.width // 2, 300 + i * 60))
                self.screen.blit(text, text_rect)
            
            # Instructions
            instructions = [
                "Use W/S or Up/Down to navigate",
                "Press Enter to select, ESC to go back"
            ]
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, (50, 50, 50))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 100 + i * 40))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def create_lobby_screen(self):
        """Screen for creating a new lobby"""
        player_name = ""
        input_active = True
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                    elif event.key == pygame.K_RETURN and player_name.strip():
                        # Try to connect and create lobby
                        try:
                            if self.client.connect():
                                lobby_code = self.client.create_lobby(player_name.strip())
                                if lobby_code:
                                    return self.waiting_lobby_screen(lobby_code, player_name.strip(), True)
                                else:
                                    return self.show_error_screen("Failed to create lobby")
                            else:
                                return self.show_error_screen("Failed to connect to server. Make sure the lobby server is running.")
                        except Exception as e:
                            return self.show_error_screen(f"Connection error: {str(e)}")
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isprintable() and len(player_name) < 20:
                        player_name += event.unicode
            
            # Draw background
            self.screen.fill((100, 150, 255))
            
            # Draw title
            title = self.font_large.render("CREATE LOBBY", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width // 2, 150))
            self.screen.blit(title, title_rect)
            
            # Draw input prompt
            prompt = self.font_medium.render("Enter your name:", True, (255, 255, 255))
            prompt_rect = prompt.get_rect(center=(self.width // 2, 300))
            self.screen.blit(prompt, prompt_rect)
            
            # Draw input box
            input_box = pygame.Rect(self.width // 2 - 200, 350, 400, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
            
            # Draw input text
            if player_name:
                text = self.font_medium.render(player_name, True, (0, 0, 0))
                text_rect = text.get_rect(midleft=(input_box.x + 10, input_box.centery))
                self.screen.blit(text, text_rect)
            else:
                placeholder = self.font_medium.render("Your name...", True, (150, 150, 150))
                placeholder_rect = placeholder.get_rect(midleft=(input_box.x + 10, input_box.centery))
                self.screen.blit(placeholder, placeholder_rect)
            
            # Instructions
            instructions = [
                "Enter your name and press Enter to create lobby",
                "ESC to go back"
            ]
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, (50, 50, 50))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 100 + i * 40))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def join_lobby_screen(self):
        """Screen for joining an existing lobby"""
        lobby_code = ""
        player_name = ""
        input_mode = "code"  # "code" or "name"
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                    elif event.key == pygame.K_TAB:
                        # Switch between code and name input
                        input_mode = "name" if input_mode == "code" else "code"
                    elif event.key == pygame.K_RETURN:
                        if input_mode == "code" and lobby_code.strip():
                            input_mode = "name"
                        elif input_mode == "name" and player_name.strip() and lobby_code.strip():
                            # Try to connect and join lobby
                            try:
                                if self.client.connect():
                                    if self.client.join_lobby(lobby_code.strip().upper(), player_name.strip()):
                                        return self.waiting_lobby_screen(lobby_code.strip().upper(), player_name.strip(), False)
                                    else:
                                        return self.show_error_screen("Failed to join lobby. Check the code and try again.")
                                else:
                                    return self.show_error_screen("Failed to connect to server. Make sure the lobby server is running.")
                            except Exception as e:
                                return self.show_error_screen(f"Connection error: {str(e)}")
                    elif event.key == pygame.K_BACKSPACE:
                        if input_mode == "code":
                            lobby_code = lobby_code[:-1]
                        else:
                            player_name = player_name[:-1]
                    elif event.unicode.isprintable():
                        if input_mode == "code" and len(lobby_code) < 4:
                            lobby_code += event.unicode.upper()
                        elif input_mode == "name" and len(player_name) < 20:
                            player_name += event.unicode
            
            # Draw background
            self.screen.fill((100, 150, 255))
            
            # Draw title
            title = self.font_large.render("JOIN LOBBY", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width // 2, 150))
            self.screen.blit(title, title_rect)
            
            # Draw lobby code input
            code_prompt = self.font_medium.render("Lobby Code:", True, (255, 255, 255))
            code_prompt_rect = code_prompt.get_rect(center=(self.width // 2, 250))
            self.screen.blit(code_prompt, code_prompt_rect)
            
            code_box = pygame.Rect(self.width // 2 - 100, 280, 200, 50)
            color = (255, 255, 0) if input_mode == "code" else (255, 255, 255)
            pygame.draw.rect(self.screen, color, code_box, 2)
            
            if lobby_code:
                text = self.font_medium.render(lobby_code, True, (0, 0, 0))
                text_rect = text.get_rect(center=code_box.center)
                self.screen.blit(text, text_rect)
            else:
                placeholder = self.font_medium.render("4 DIGITS", True, (150, 150, 150))
                placeholder_rect = placeholder.get_rect(center=code_box.center)
                self.screen.blit(placeholder, placeholder_rect)
            
            # Draw name input
            name_prompt = self.font_medium.render("Your Name:", True, (255, 255, 255))
            name_prompt_rect = name_prompt.get_rect(center=(self.width // 2, 380))
            self.screen.blit(name_prompt, name_prompt_rect)
            
            name_box = pygame.Rect(self.width // 2 - 150, 410, 300, 50)
            color = (255, 255, 0) if input_mode == "name" else (255, 255, 255)
            pygame.draw.rect(self.screen, color, name_box, 2)
            
            if player_name:
                text = self.font_medium.render(player_name, True, (0, 0, 0))
                text_rect = text.get_rect(midleft=(name_box.x + 10, name_box.centery))
                self.screen.blit(text, text_rect)
            else:
                placeholder = self.font_medium.render("Your name...", True, (150, 150, 150))
                placeholder_rect = placeholder.get_rect(midleft=(name_box.x + 10, name_box.centery))
                self.screen.blit(placeholder, placeholder_rect)
            
            # Instructions
            instructions = [
                "Enter 4-digit lobby code and your name",
                "Tab to switch between fields, Enter to continue",
                "ESC to go back"
            ]
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, (50, 50, 50))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 120 + i * 30))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def browse_lobbies_screen(self):
        """Screen for browsing available lobbies"""
        lobbies = []
        selected_lobby = 0
        refresh_timer = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if lobbies:
                            selected_lobby = (selected_lobby - 1) % len(lobbies)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if lobbies:
                            selected_lobby = (selected_lobby + 1) % len(lobbies)
                    elif event.key == pygame.K_RETURN and lobbies:
                        # Join selected lobby
                        selected = lobbies[selected_lobby]
                        return self.join_specific_lobby_screen(selected['code'])
                    elif event.key == pygame.K_r:
                        # Refresh lobbies
                        if self.client.connect():
                            lobbies = self.client.get_available_lobbies()
                        else:
                            return self.show_error_screen("Failed to connect to server")
            
            # Auto-refresh lobbies every 5 seconds
            refresh_timer += self.clock.get_time()
            if refresh_timer > 5000:  # 5 seconds
                if self.client.connect():
                    lobbies = self.client.get_available_lobbies()
                refresh_timer = 0
            
            # Draw background
            self.screen.fill((100, 150, 255))
            
            # Draw title
            title = self.font_large.render("AVAILABLE LOBBIES", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width // 2, 100))
            self.screen.blit(title, title_rect)
            
            if not lobbies:
                no_lobbies = self.font_medium.render("No lobbies available", True, (255, 255, 255))
                no_lobbies_rect = no_lobbies.get_rect(center=(self.width // 2, 300))
                self.screen.blit(no_lobbies, no_lobbies_rect)
            else:
                # Draw lobby list
                for i, lobby in enumerate(lobbies):
                    color = (255, 255, 0) if i == selected_lobby else (255, 255, 255)
                    text = f"Lobby {lobby['code']} - Host: {lobby['host_name']}"
                    lobby_text = self.font_medium.render(text, True, color)
                    lobby_rect = lobby_text.get_rect(center=(self.width // 2, 250 + i * 60))
                    self.screen.blit(lobby_text, lobby_rect)
            
            # Instructions
            instructions = [
                "Use W/S to navigate, Enter to join",
                "R to refresh, ESC to go back"
            ]
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, (50, 50, 50))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 100 + i * 40))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def join_specific_lobby_screen(self, lobby_code):
        """Screen for joining a specific lobby from browse"""
        player_name = ""
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                    elif event.key == pygame.K_RETURN and player_name.strip():
                        if self.client.connect():
                            if self.client.join_lobby(lobby_code, player_name.strip()):
                                return self.waiting_lobby_screen(lobby_code, player_name.strip(), False)
                            else:
                                return self.show_error_screen("Failed to join lobby")
                        else:
                            return self.show_error_screen("Failed to connect to server")
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isprintable() and len(player_name) < 20:
                        player_name += event.unicode
            
            # Draw background
            self.screen.fill((100, 150, 255))
            
            # Draw title
            title = self.font_large.render(f"JOIN LOBBY {lobby_code}", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width // 2, 150))
            self.screen.blit(title, title_rect)
            
            # Draw name input
            name_prompt = self.font_medium.render("Enter your name:", True, (255, 255, 255))
            name_prompt_rect = name_prompt.get_rect(center=(self.width // 2, 300))
            self.screen.blit(name_prompt, name_prompt_rect)
            
            name_box = pygame.Rect(self.width // 2 - 150, 350, 300, 50)
            pygame.draw.rect(self.screen, (255, 255, 255), name_box, 2)
            
            if player_name:
                text = self.font_medium.render(player_name, True, (0, 0, 0))
                text_rect = text.get_rect(midleft=(name_box.x + 10, name_box.centery))
                self.screen.blit(text, text_rect)
            else:
                placeholder = self.font_medium.render("Your name...", True, (150, 150, 150))
                placeholder_rect = placeholder.get_rect(midleft=(name_box.x + 10, name_box.centery))
                self.screen.blit(placeholder, placeholder_rect)
            
            # Instructions
            instructions = [
                "Enter your name and press Enter to join",
                "ESC to go back"
            ]
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, (50, 50, 50))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 100 + i * 40))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def waiting_lobby_screen(self, lobby_code, player_name, is_host):
        """Screen shown while waiting for other player"""
        waiting_message = "Waiting for player to join..." if is_host else "Waiting for host to start..."
        guest_name = None
        can_start = False
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.client.leave_lobby()
                        return "back"
                    if is_host and can_start and event.key == pygame.K_RETURN:
                        # Host starts the game
                        return self.multiplayer_character_selection(lobby_code, player_name, is_host)
            
            # Check for pending actions (like guest joined)
            actions = self.client.get_pending_actions()
            for action in actions:
                if action.get('type') == 'guest_joined':
                    guest_name = action.get('guest_name')
                    can_start = True
                elif action.get('type') == 'player_left':
                    guest_name = None
                    can_start = False
            
            # Draw background
            self.screen.fill((100, 150, 255))
            
            # Draw title
            title = self.font_large.render("LOBBY", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width // 2, 150))
            self.screen.blit(title, title_rect)
            
            # Draw lobby code
            code_text = self.font_medium.render(f"Code: {lobby_code}", True, (255, 255, 0))
            code_rect = code_text.get_rect(center=(self.width // 2, 250))
            self.screen.blit(code_text, code_rect)
            
            # Draw player info
            role = "Host" if is_host else "Guest"
            player_text = self.font_medium.render(f"You: {player_name} ({role})", True, (255, 255, 255))
            player_rect = player_text.get_rect(center=(self.width // 2, 320))
            self.screen.blit(player_text, player_rect)
            
            # Draw guest info if present
            if is_host and guest_name:
                guest_text = self.font_medium.render(f"Guest: {guest_name}", True, (0, 255, 0))
                guest_rect = guest_text.get_rect(center=(self.width // 2, 370))
                self.screen.blit(guest_text, guest_rect)
            
            # Draw waiting message or start button
            if is_host:
                if guest_name:
                    start_text = self.font_medium.render("Press Enter to Start!", True, (255, 255, 0))
                    start_rect = start_text.get_rect(center=(self.width // 2, 430))
                    self.screen.blit(start_text, start_rect)
                else:
                    wait_text = self.font_medium.render(waiting_message, True, (255, 255, 255))
                    wait_rect = wait_text.get_rect(center=(self.width // 2, 430))
                    self.screen.blit(wait_text, wait_rect)
            else:
                wait_text = self.font_medium.render(waiting_message, True, (255, 255, 255))
                wait_rect = wait_text.get_rect(center=(self.width // 2, 430))
                self.screen.blit(wait_text, wait_rect)
            
            # Instructions
            instructions = [
                "Share the 4-digit lobby code with your friend",
                "ESC to leave lobby"
            ]
            if is_host and guest_name:
                instructions.insert(0, "Press Enter to start the game")
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, (50, 50, 50))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 100 + i * 40))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def show_error_screen(self, error_message):
        """Show error message screen"""
        timer = 0
        
        while timer < 3000:  # Show for 3 seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return "back"
            
            # Draw background
            self.screen.fill((100, 150, 255))
            
            # Draw error message
            error_text = self.font_medium.render(error_message, True, (255, 0, 0))
            error_rect = error_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(error_text, error_rect)
            
            # Instructions
            instruction = self.font_small.render("Press any key to continue", True, (50, 50, 50))
            instruction_rect = instruction.get_rect(center=(self.width // 2, self.height // 2 + 100))
            self.screen.blit(instruction, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
            timer += self.clock.get_time()
        
        return "back"
    
    def multiplayer_character_selection(self, lobby_code, player_name, is_host):
        """Character selection screen for multiplayer games"""
        classes = ["Warrior", "Mage", "Ghost"]
        selected = 0
        name = ""
        input_active = False
        done = False
        
        # Send character selection status to other player
        self.client.send_game_action("character_selecting", {"player": player_name})
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if not input_active:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            selected = (selected - 1) % len(classes)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            selected = (selected + 1) % len(classes)
                        elif event.key == pygame.K_RETURN:
                            input_active = True
                        elif event.key == pygame.K_ESCAPE:
                            self.client.leave_lobby()
                            return "back"
                    else:
                        if event.key == pygame.K_RETURN:
                            if name.strip() == "":
                                name = classes[selected]
                            # Send character choice to other player
                            self.client.send_game_action("character_chosen", {
                                "player": player_name,
                                "class": classes[selected],
                                "name": name.strip()
                            })
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            if len(name) < 12 and event.unicode.isprintable():
                                name += event.unicode
            
            # Check for other player's character choice
            actions = self.client.get_pending_actions()
            for action in actions:
                if action.get('type') == 'character_chosen':
                    other_player = action.get('data', {}).get('player')
                    other_class = action.get('data', {}).get('class')
                    # Remove the class the other player chose from available options
                    if other_class in classes:
                        classes.remove(other_class)
                        if selected >= len(classes):
                            selected = 0
            
            # Draw selection screen
            self.screen.fill((20, 20, 40))
            title = self.font_large.render(f"Choose Your Character - {player_name}", True, (255, 255, 255))
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))
            
            # Draw class options
            positions = [int((self.width * (j + 1)) / (len(classes) + 1)) for j in range(len(classes))]
            
            for i, (class_name, pos) in enumerate(zip(classes, positions)):
                color = (255, 255, 0) if i == selected else (255, 255, 255)
                text = self.font_medium.render(class_name, True, color)
                text_rect = text.get_rect(center=(pos, 300))
                self.screen.blit(text, text_rect)
                
                # Draw selection indicator
                if i == selected:
                    pygame.draw.rect(self.screen, color, (pos - 100, 320, 200, 4), 3)
            
            # Draw name input if active
            if input_active:
                name_prompt = self.font_medium.render("Enter your character name:", True, (255, 255, 255))
                self.screen.blit(name_prompt, (self.width // 2 - name_prompt.get_width() // 2, 400))
                
                name_box = pygame.Rect(self.width // 2 - 150, 450, 300, 50)
                pygame.draw.rect(self.screen, (255, 255, 255), name_box, 2)
                
                if name:
                    name_text = self.font_medium.render(name, True, (0, 0, 0))
                    name_rect = name_text.get_rect(midleft=(name_box.x + 10, name_box.centery))
                    self.screen.blit(name_text, name_rect)
                else:
                    placeholder = self.font_medium.render("Character name...", True, (150, 150, 150))
                    placeholder_rect = placeholder.get_rect(midleft=(name_box.x + 10, name_box.centery))
                    self.screen.blit(placeholder, placeholder_rect)
            
            # Draw instructions
            if not input_active:
                instructions = [
                    "Use A/D or Left/Right to choose class",
                    "Press Enter to confirm class",
                    "ESC to leave lobby"
                ]
            else:
                instructions = [
                    "Enter your character name",
                    "Press Enter to confirm",
                    "ESC to leave lobby"
                ]
            
            for i, instruction in enumerate(instructions):
                text = self.font_small.render(instruction, True, (150, 150, 150))
                text_rect = text.get_rect(center=(self.width // 2, self.height - 100 + i * 30))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
        
        # Wait for both players to be ready
        return self.wait_for_both_players_ready(lobby_code, player_name, is_host, classes[selected], name.strip())
    
    def wait_for_both_players_ready(self, lobby_code, player_name, is_host, chosen_class, chosen_name):
        """Wait for both players to finish character selection"""
        waiting_message = "Waiting for other player to choose character..."
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    self.client.leave_lobby()
                    return "back"
            
            # Check for game start signal
            actions = self.client.get_pending_actions()
            for action in actions:
                if action.get('type') == 'game_ready':
                    return {
                        "type": "start_game",
                        "player_name": chosen_name,
                        "player_class": chosen_class,
                        "is_host": is_host
                    }
            
            # Draw waiting screen
            self.screen.fill((100, 150, 255))
            
            title = self.font_large.render("CHARACTERS SELECTED", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width // 2, 150))
            self.screen.blit(title, title_rect)
            
            # Show player's choice
            choice_text = self.font_medium.render(f"You: {chosen_name} ({chosen_class})", True, (255, 255, 0))
            choice_rect = choice_text.get_rect(center=(self.width // 2, 250))
            self.screen.blit(choice_text, choice_rect)
            
            # Show waiting message
            wait_text = self.font_medium.render(waiting_message, True, (255, 255, 255))
            wait_rect = wait_text.get_rect(center=(self.width // 2, 350))
            self.screen.blit(wait_text, wait_rect)
            
            # Instructions
            instruction = self.font_small.render("ESC to leave lobby", True, (50, 50, 50))
            instruction_rect = instruction.get_rect(center=(self.width // 2, self.height - 100))
            self.screen.blit(instruction, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(30) 