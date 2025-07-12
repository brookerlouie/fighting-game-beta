import socket
import threading
import json
import uuid
import time
import random
from typing import Dict, List, Optional, Tuple

class LobbyManager:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.lobbies: Dict[str, Dict] = {}
        self.lobbies_lock = threading.Lock()
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """Start the lobby server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Lobby server started on {self.host}:{self.port}")
        
        # Start accepting connections in a separate thread
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()
        
    def accept_connections(self):
        """Accept incoming connections"""
        while self.running and self.server_socket:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
                    
    def handle_client(self, client_socket: socket.socket, address: Tuple):
        """Handle individual client connections"""
        lobby_code = None
        try:
            while self.running:
                try:
                    print(f"[SERVER] Waiting to receive from {address}")
                    data = client_socket.recv(1024).decode('utf-8')
                    print(f"[SERVER] Received from {address}: {data}")
                    if not data:
                        break
                    
                    message = json.loads(data)
                    response = self.process_message(message, client_socket)
                    
                    if response:
                        try:
                            print(f"[SERVER] Sending to {address}: {response}")
                            client_socket.send(json.dumps(response).encode('utf-8'))
                        except Exception as e:
                            print(f"Error sending response to {address}: {e}")
                        # Track lobby code for cleanup
                        if message.get('type') == 'create_lobby' and response:
                            lobby_code = response.get('lobby_code')
                        elif message.get('type') == 'join_lobby':
                            lobby_code = message.get('lobby_code', '').upper()
                except Exception as e:
                    print(f"Error handling client {address}: {e}")
                    break
        finally:
            # Find which lobby this client belongs to and clean up
            with self.lobbies_lock:
                # Find lobby by checking both host and guest sockets
                found_lobby_code = None
                for code, lobby in self.lobbies.items():
                    if lobby['host'] == client_socket or lobby['guest'] == client_socket:
                        found_lobby_code = code
                        break
                
                if found_lobby_code:
                    lobby = self.lobbies[found_lobby_code]
                    if lobby['host'] == client_socket:
                        # Host disconnected: close the lobby and notify guest
                        if lobby['guest']:
                            try:
                                leave_message = {'type': 'player_left'}
                                lobby['guest'].send(json.dumps(leave_message).encode('utf-8'))
                            except Exception:
                                pass
                        del self.lobbies[found_lobby_code]
                        print(f"Lobby {found_lobby_code} closed (host disconnected)")
                    elif lobby['guest'] == client_socket:
                        # Guest disconnected: just remove guest, notify host, but keep lobby open
                        try:
                            leave_message = {'type': 'player_left'}
                            lobby['host'].send(json.dumps(leave_message).encode('utf-8'))
                        except Exception:
                            pass
                        lobby['guest'] = None
                        lobby['guest_name'] = None
                        lobby['game_state'] = 'waiting'
                        print(f"Guest left lobby {found_lobby_code}, lobby still open")
            client_socket.close()
            
    def process_message(self, message: Dict, client_socket: socket.socket) -> Optional[Dict]:
        """Process client messages"""
        msg_type = message.get('type')
        
        if msg_type == 'create_lobby':
            return self.create_lobby(message, client_socket)
        elif msg_type == 'join_lobby':
            return self.join_lobby(message, client_socket)
        elif msg_type == 'get_lobbies':
            return self.get_lobbies()
        elif msg_type == 'game_action':
            return self.handle_game_action(message)
        elif msg_type == 'leave_lobby':
            return self.leave_lobby(message, client_socket)
            
        return {'error': 'Unknown message type'}
        
    def create_lobby(self, message: Dict, client_socket: socket.socket) -> Dict:
        print("DEBUG: USING 4-DIGIT LOBBY CODE GENERATION")
        """Create a new lobby"""
        chars = "0123456789"
        while True:
            lobby_code = ''.join(random.choice(chars) for _ in range(4))
            with self.lobbies_lock:
                if lobby_code not in self.lobbies:
                    break
        player_name = message.get('player_name', 'Player 1')
        with self.lobbies_lock:
            self.lobbies[lobby_code] = {
                'host': client_socket,
                'host_name': player_name,
                'guest': None,
                'guest_name': None,
                'game_state': 'waiting',
                'created_at': time.time(),
                'host_character': None,
                'guest_character': None,
                'both_ready': False
            }
        
        print(f"Lobby created: {lobby_code} by {player_name}")
        return {
            'type': 'lobby_created',
            'lobby_code': lobby_code,
            'status': 'success'
        }
        
    def join_lobby(self, message: Dict, client_socket: socket.socket) -> Dict:
        """Join an existing lobby"""
        lobby_code = message.get('lobby_code', '').upper()
        player_name = message.get('player_name', 'Player 2')
        
        with self.lobbies_lock:
            if lobby_code not in self.lobbies:
                return {'type': 'join_result', 'status': 'error', 'message': 'Lobby not found'}
            
            lobby = self.lobbies[lobby_code]
            if lobby['guest'] is not None:
                return {'type': 'join_result', 'status': 'error', 'message': 'Lobby is full'}
            
            lobby['guest'] = client_socket
            lobby['guest_name'] = player_name
            lobby['game_state'] = 'ready'
        
        # Notify host that guest joined
        try:
            host_message = {
                'type': 'guest_joined',
                'guest_name': player_name
            }
            lobby['host'].send(json.dumps(host_message).encode('utf-8'))
        except Exception:
            pass
            
        print(f"Player {player_name} joined lobby {lobby_code}")
        return {
            'type': 'join_result',
            'status': 'success',
            'host_name': lobby['host_name']
        }
        
    def get_lobbies(self) -> Dict:
        """Get list of available lobbies"""
        available_lobbies = []
        with self.lobbies_lock:
            for code, lobby in self.lobbies.items():
                if lobby['guest'] is None:  # Only show lobbies with space
                    available_lobbies.append({
                        'code': code,
                        'host_name': lobby['host_name'],
                        'created_at': lobby['created_at']
                    })
                
        return {
            'type': 'lobby_list',
            'lobbies': available_lobbies
        }
        
    def handle_game_action(self, message: Dict) -> Dict:
        """Handle game actions between players"""
        lobby_code = message.get('lobby_code')
        with self.lobbies_lock:
            if lobby_code not in self.lobbies:
                return {'error': 'Lobby not found'}
            
            lobby = self.lobbies[lobby_code]
            action = message.get('action')
            player = message.get('player')  # 'host' or 'guest'
            
            # Handle character selection
            if action == 'character_chosen':
                data = message.get('data', {})
                if player == 'host':
                    lobby['host_character'] = data
                else:
                    lobby['guest_character'] = data
                
                # Check if both players have chosen characters
                if lobby['host_character'] and lobby['guest_character']:
                    lobby['both_ready'] = True
                    # Send game_ready signal to both players
                    try:
                        ready_message = {'type': 'game_action', 'action': 'game_ready', 'data': {}}
                        if lobby['host']:
                            lobby['host'].send(json.dumps(ready_message).encode('utf-8'))
                        if lobby['guest']:
                            lobby['guest'].send(json.dumps(ready_message).encode('utf-8'))
                    except Exception as e:
                        print(f"Error sending game_ready: {e}")
            
            # Forward action to other player
            target_socket = lobby['guest'] if player == 'host' else lobby['host']
            
            if target_socket:
                try:
                    forward_message = {
                        'type': 'game_action',
                        'action': action,
                        'data': message.get('data', {})
                    }
                    target_socket.send(json.dumps(forward_message).encode('utf-8'))
                    return {'status': 'action_sent'}
                except Exception:
                    return {'error': 'Failed to send action'}
                
            return {'error': 'Other player not connected'}
        
    def leave_lobby(self, message: Dict, client_socket: socket.socket) -> Dict:
        """Handle player leaving lobby"""
        lobby_code = message.get('lobby_code')
        with self.lobbies_lock:
            if lobby_code in self.lobbies:
                lobby = self.lobbies[lobby_code]
                
                if client_socket == lobby['host']:
                    # Host is leaving: close the lobby and notify guest
                    if lobby['guest']:
                        try:
                            leave_message = {'type': 'player_left'}
                            lobby['guest'].send(json.dumps(leave_message).encode('utf-8'))
                        except Exception:
                            pass
                    del self.lobbies[lobby_code]
                    print(f"Lobby {lobby_code} closed (host left)")
                else:
                    # Guest is leaving: just remove guest, notify host, but keep lobby open
                    try:
                        leave_message = {'type': 'player_left'}
                        lobby['host'].send(json.dumps(leave_message).encode('utf-8'))
                    except Exception:
                        pass
                    lobby['guest'] = None
                    lobby['guest_name'] = None
                    lobby['game_state'] = 'waiting'
                    print(f"Guest left lobby {lobby_code}, lobby still open")
            
        return {'status': 'left_lobby'}
        
    def stop_server(self):
        """Stop the lobby server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()

class MultiplayerClient:
    def __init__(self, server_host='localhost', server_port=5555):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.connected = False
        self.lobby_code = None
        self.is_host = False
        self.game_actions = []
        
    def connect(self) -> bool:
        """Connect to the lobby server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.socket.settimeout(5)  # 5 second timeout to prevent freezing
            self.connected = True
            print(f"[CLIENT] Connected to server at {self.server_host}:{self.server_port}")
            
            # Start listening for messages
            listen_thread = threading.Thread(target=self.listen_for_messages)
            listen_thread.daemon = True
            listen_thread.start()
            
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
            
    def create_lobby(self, player_name: str) -> Optional[str]:
        """Create a new lobby"""
        if not self.connected:
            return None
            
        message = {
            'type': 'create_lobby',
            'player_name': player_name
        }
        
        response = self.send_message(message)
        if response and response.get('status') == 'success':
            self.lobby_code = response.get('lobby_code')
            self.is_host = True
            return self.lobby_code
        return None
        
    def join_lobby(self, lobby_code: str, player_name: str) -> bool:
        """Join an existing lobby"""
        if not self.connected:
            return False
            
        message = {
            'type': 'join_lobby',
            'lobby_code': lobby_code,
            'player_name': player_name
        }
        
        response = self.send_message(message)
        if response and response.get('status') == 'success':
            self.lobby_code = lobby_code
            self.is_host = False
            return True
        return False
        
    def get_available_lobbies(self) -> List[Dict]:
        """Get list of available lobbies"""
        if not self.connected:
            return []
            
        message = {'type': 'get_lobbies'}
        response = self.send_message(message)
        
        if response and response.get('type') == 'lobby_list':
            return response.get('lobbies', [])
        return []
        
    def send_game_action(self, action: str, data: Optional[Dict] = None) -> bool:
        """Send a game action to the other player"""
        if not self.connected or not self.lobby_code:
            return False
            
        message = {
            'type': 'game_action',
            'lobby_code': self.lobby_code,
            'player': 'host' if self.is_host else 'guest',
            'action': action,
            'data': data if data is not None else {}
        }
        
        return self.send_message(message) is not None
        
    def send_message(self, message: Dict) -> Optional[Dict]:
        """Send a message to the server and wait for response"""
        if not self.socket:
            return None
        try:
            print(f"[CLIENT] Sending: {message}")
            self.socket.send(json.dumps(message).encode('utf-8'))
            
            # For certain message types, we expect an immediate response
            if message.get('type') in ['create_lobby', 'join_lobby', 'get_lobbies', 'leave_lobby']:
                data = self.socket.recv(1024).decode('utf-8')
                print(f"[CLIENT] Received: {data}")
                return json.loads(data) if data else None
            else:
                # For other messages, don't wait for response
                return {'status': 'sent'}
                
        except socket.timeout:
            print("[CLIENT] Socket timeout waiting for server response!")
            return None
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
            
    def listen_for_messages(self):
        """Listen for incoming messages from server"""
        while self.connected and self.socket:
            try:
                print("[CLIENT] Waiting for server message...")
                data = self.socket.recv(1024).decode('utf-8')
                print(f"[CLIENT] Received async: {data}")
                if not data:
                    break
                    
                message = json.loads(data)
                self.handle_message(message)
                
            except Exception as e:
                if self.connected:
                    print(f"Error receiving message: {e}")
                break
                
        self.connected = False
        
    def handle_message(self, message: Dict):
        """Handle incoming messages"""
        msg_type = message.get('type')
        print(f"[CLIENT DEBUG] Handling message: {message}")
        
        if msg_type == 'guest_joined':
            print(f"Guest joined: {message.get('guest_name')}")
            # Add to game actions queue so UI can process it
            self.game_actions.append(message)
            print(f"[CLIENT DEBUG] Added guest_joined to game_actions, queue now has {len(self.game_actions)} items")
        elif msg_type == 'player_left':
            print("Other player left the game")
            # Add to game actions queue so UI can process it
            self.game_actions.append(message)
            print(f"[CLIENT DEBUG] Added player_left to game_actions, queue now has {len(self.game_actions)} items")
        elif msg_type == 'game_action':
            # Add to game actions queue
            self.game_actions.append(message)
            print(f"[CLIENT DEBUG] Added game_action to game_actions, queue now has {len(self.game_actions)} items")
            
    def get_pending_actions(self) -> List[Dict]:
        """Get and clear pending game actions"""
        actions = self.game_actions.copy()
        self.game_actions.clear()
        return actions
        
    def leave_lobby(self):
        """Leave the current lobby"""
        if self.connected and self.lobby_code:
            message = {
                'type': 'leave_lobby',
                'lobby_code': self.lobby_code
            }
            self.send_message(message)
            
        self.lobby_code = None
        self.is_host = False
        
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        if self.socket:
            self.socket.close() 