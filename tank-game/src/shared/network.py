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
            self.socket.settimeout(5)
            self.socket.connect((self.host, self.port))
            
            # Send version check first
            version_msg = {'action': 'version_check', 'version': '1.0.0'}
            self.socket.send(json.dumps(version_msg).encode())
            self.socket.settimeout(5)
            response = self.socket.recv(1024).decode()
            response_data = json.loads(response)
            
            if response_data.get('status') != 'success':
                print(f"Server rejected: {response_data.get('message')}")
                self.socket.close()
                return False
            
            # Set non-blocking for regular communication
            self.socket.setblocking(False)
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except socket.timeout:
            print(f"Connection timeout: Server not responding at {self.host}:{self.port}")
            return False
        except ConnectionRefusedError:
            print(f"Connection refused: No server at {self.host}:{self.port}")
            return False
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    def send_message(self, message):
        """Send a message to the server"""
        try:
            self.socket.send(json.dumps(message).encode())
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def receive_message(self, timeout=0.5):
        """Receive a message from the server (non-blocking)"""
        try:
            # Use select for timeout on non-blocking socket
            import select
            ready = select.select([self.socket], [], [], timeout)
            if ready[0]:
                data = self.socket.recv(1024).decode()
                if data:
                    return json.loads(data)
            return None
        except json.JSONDecodeError:
            print("Invalid JSON received")
            return None
        except Exception as e:
            print(f"Failed to receive message: {e}")
            return None
    
    def send_join_request(self, room_code, player_name):
        """Send join room request"""
        message = {
            'action': 'join_room',
            'room_code': room_code,
            'player_name': player_name
        }
        self.send_message(message)
    
    def close(self):
        """Close the connection"""
        if self.socket:
            self.socket.close()