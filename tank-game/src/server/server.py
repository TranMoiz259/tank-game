import socket
import threading
import random
import string
import json
from .room import Room

class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.rooms = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

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
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    action = message.get('action')
                    
                    if action == 'create_room':
                        room_code = self.create_room()
                        response = {'status': 'success', 'room_code': room_code}
                        client_socket.send(json.dumps(response).encode())
                        print(f"Room {room_code} created by {client_address}")
                    
                    elif action == 'join_room':
                        room_code = message.get('room_code')
                        player_name = message.get('player_name')
                        if self.join_room(room_code, player_name):
                            response = {'status': 'success', 'message': 'Joined room'}
                            client_socket.send(json.dumps(response).encode())
                            print(f"{player_name} joined room {room_code}")
                        else:
                            response = {'status': 'error', 'message': 'Room not found'}
                            client_socket.send(json.dumps(response).encode())
                            print(f"Failed: Room {room_code} not found")
                except json.JSONDecodeError:
                    print(f"Invalid JSON from {client_address}")
                    
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()