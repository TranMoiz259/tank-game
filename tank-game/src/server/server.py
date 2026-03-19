import socket
import threading
import random
import string
import json
from .room import Room

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.rooms = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.client_lock = threading.Lock()

    def generate_room_code(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def create_room(self):
        room_code = self.generate_room_code()
        self.rooms[room_code] = Room(room_code)
        return room_code

    def join_room(self, room_code, player):
        if room_code in self.rooms:
            self.rooms[room_code].add_player(player)
            return True
        return False

    def run(self):
        """Start the server and listen for client connections"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, client_address = self.socket.accept()
                print(f"Client connected: {client_address}")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.socket.close()

    def handle_client(self, client_socket, client_address):
        """Handle communication with a connected client"""
        player_name = None
        room_code = None
        try:
            # First message must be version check
            data = client_socket.recv(1024).decode()
            if not data:
                return
            
            message = json.loads(data)
            if message.get('action') == 'version_check':
                client_version = message.get('version', '0.0.0')
                server_version = '1.0.0'
                if client_version != server_version:
                    response = {'status': 'error', 'message': f'Version mismatch. Client: {client_version}, Server: {server_version}'}
                    client_socket.send(json.dumps(response).encode())
                    print(f"Client {client_address} rejected: version mismatch")
                    return
                else:
                    response = {'status': 'success', 'message': 'Version OK'}
                    client_socket.send(json.dumps(response).encode())
            
            # Continue with normal communication
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    action = message.get('action')
                    
                    if action == 'create_room':
                        room_code = self.create_room()
                        player_name = message.get('player_name', 'Host')
                        self.rooms[room_code].add_player(player_name)
                        player_count = self.rooms[room_code].get_player_count()
                        response = {
                            'status': 'success',
                            'room_code': room_code,
                            'player_count': player_count
                        }
                        client_socket.send(json.dumps(response).encode())
                        print(f"Room {room_code} created by {player_name}. Players: {player_count}/4")
                    
                    elif action == 'join_room':
                        room_code = message.get('room_code')
                        player_name = message.get('player_name')
                        if room_code in self.rooms:
                            if player_name in self.rooms[room_code].players:
                                response = {'status': 'error', 'message': 'Player name already taken'}
                                client_socket.send(json.dumps(response).encode())
                                print(f"Failed: Player name '{player_name}' already in room {room_code}")
                            elif self.rooms[room_code].add_player(player_name):
                                response = {
                                    'status': 'success',
                                    'message': 'Joined room',
                                    'player_count': self.rooms[room_code].get_player_count()
                                }
                                client_socket.send(json.dumps(response).encode())
                                print(f"{player_name} joined room {room_code}. Players: {self.rooms[room_code].get_player_count()}/4")
                            else:
                                response = {'status': 'error', 'message': 'Room is full'}
                                client_socket.send(json.dumps(response).encode())
                        else:
                            response = {'status': 'error', 'message': 'Room not found'}
                            client_socket.send(json.dumps(response).encode())
                    
                    elif action == 'leave_room':
                        room_code = message.get('room_code')
                        player_name = message.get('player_name')
                        if room_code in self.rooms and player_name in self.rooms[room_code].players:
                            self.rooms[room_code].players.remove(player_name)
                            print(f"{player_name} left room {room_code}. Players: {self.rooms[room_code].get_player_count()}/4")
                            
                            # Delete room if empty
                            if self.rooms[room_code].get_player_count() == 0:
                                del self.rooms[room_code]
                                print(f"Room {room_code} deleted (empty)")
                    
                    elif action == 'get_player_count':
                        room_code = message.get('room_code')
                        if room_code in self.rooms:
                            response = {
                                'status': 'success',
                                'player_count': self.rooms[room_code].get_player_count()
                            }
                        else:
                            response = {'status': 'error', 'player_count': 0}
                        client_socket.send(json.dumps(response).encode())
                    
                    elif action == 'start_game':
                        room_code = message.get('room_code')
                        if room_code in self.rooms:
                            if self.rooms[room_code].start_game():
                                response = {'status': 'success', 'message': 'Game started'}
                                client_socket.send(json.dumps(response).encode())
                                print(f"Game started in room {room_code}")
                            else:
                                response = {'status': 'error', 'message': 'Not enough players'}
                                client_socket.send(json.dumps(response).encode())
                        else:
                            response = {'status': 'error', 'message': 'Room not found'}
                            client_socket.send(json.dumps(response).encode())
                    
                    elif action == 'list_rooms':
                        rooms_list = list(self.rooms.keys())
                        response = {'status': 'success', 'rooms': rooms_list}
                        client_socket.send(json.dumps(response).encode())
                        
                except json.JSONDecodeError:
                    print(f"Invalid JSON from {client_address}")
                    
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            # Remove player from room when disconnecting
            if room_code and player_name and room_code in self.rooms:
                if player_name in self.rooms[room_code].players:
                    self.rooms[room_code].players.remove(player_name)
                    print(f"{player_name} disconnected from room {room_code}. Players: {self.rooms[room_code].get_player_count()}/4")
                    
                    # Delete room if empty
                    if self.rooms[room_code].get_player_count() == 0:
                        del self.rooms[room_code]
                        print(f"Room {room_code} deleted (empty)")
            client_socket.close()