import socket
import json

class NetworkClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Connect to the server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def send_message(self, message):
        """Send a message to the server"""
        try:
            self.socket.send(json.dumps(message).encode())
            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False

    def receive_message(self):
        """Receive a message from the server"""
        try:
            data = self.socket.recv(1024).decode()
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Failed to receive message: {e}")
            return None

    def send_join_request(self, room_code, player_name):
        """Send a join room request"""
        message = {
            'action': 'join_room',
            'room_code': room_code,
            'player_name': player_name
        }
        return self.send_message(message)

    def close(self):
        """Close the connection"""
        if self.socket:
            self.socket.close()