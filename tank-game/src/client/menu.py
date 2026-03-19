import pygame
import random
import string
import socket
from enum import Enum
from src.shared.network import NetworkClient
from src.server.server import Server
import threading
import time

class MenuState(Enum):
    MAIN = 1
    CREATE_ROOM = 2
    JOIN_ROOM = 3
    SETTINGS = 4
    WAITING = 5
    NETWORK_SETTINGS = 6
    GAME = 7

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface, font):
        color = (150, 150, 150) if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)

class Menu:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tank Game")
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.state = MenuState.NETWORK_SETTINGS
        self.running = True
        self.player_name = ""
        self.room_code = ""
        self.server_ip = "192.168.50.11"
        self.server_port = 12345
        self.network = None
        self.server = None
        self.input_text = ""
        self.input_active = False
        self.current_input_field = 0
        self.player_count = 1
        self.last_count_check = 0
        
        self.setup_main_menu()

    def setup_main_menu(self):
        self.create_room_btn = Button(150, 200, 500, 80, "Create Room")
        self.join_room_btn = Button(150, 320, 500, 80, "Join Room")
        self.settings_btn = Button(150, 440, 500, 80, "Player Settings")

    def run(self):
        """Main menu loop"""
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.update_button_hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_input(event)

    def update_button_hover(self, pos):
        if self.state == MenuState.MAIN:
            self.create_room_btn.update(pos)
            self.join_room_btn.update(pos)
            self.settings_btn.update(pos)

    def handle_click(self, pos):
        if self.state == MenuState.MAIN:
            if self.create_room_btn.is_clicked(pos):
                self.create_room()
            elif self.join_room_btn.is_clicked(pos):
                self.state = MenuState.JOIN_ROOM
                self.input_text = ""
                self.input_active = True
            elif self.settings_btn.is_clicked(pos):
                self.state = MenuState.SETTINGS
                self.input_text = self.player_name
                self.input_active = True
        elif self.state == MenuState.WAITING:
            if pygame.Rect(300, 410, 200, 50).collidepoint(pos) and self.player_count >= 2:
                self.start_game()
            elif pygame.Rect(50, 520, 100, 40).collidepoint(pos):
                self.leave_room()
        elif self.state == MenuState.GAME:
            if pygame.Rect(300, 520, 200, 40).collidepoint(pos):
                self.state = MenuState.MAIN
                self.room_code = ""
        elif self.state == MenuState.JOIN_ROOM:
            if pygame.Rect(50, 520, 100, 40).collidepoint(pos):
                self.state = MenuState.MAIN
        elif self.state == MenuState.SETTINGS:
            if pygame.Rect(50, 520, 100, 40).collidepoint(pos):
                self.state = MenuState.MAIN
        elif self.state == MenuState.NETWORK_SETTINGS:
            self.save_network_field(self.current_input_field)
            
            if pygame.Rect(150, 170, 500, 40).collidepoint(pos):
                self.current_input_field = 0
                self.input_text = self.server_ip
                self.input_active = True
            elif pygame.Rect(150, 260, 500, 40).collidepoint(pos):
                self.current_input_field = 1
                self.input_text = str(self.server_port)
                self.input_active = True
            elif pygame.Rect(300, 370, 200, 50).collidepoint(pos):
                self.save_network_field(self.current_input_field)
                self.confirm_network_settings()

    def leave_room(self):
        """Leave the current room"""
        if self.network:
            message = {
                'action': 'leave_room',
                'room_code': self.room_code,
                'player_name': self.player_name
            }
            self.network.send_message(message)
        self.room_code = ""
        self.state = MenuState.MAIN
        print(f"{self.player_name} left the room")

    def start_game(self):
        """Start the game"""
        if self.network:
            message = {
                'action': 'start_game',
                'room_code': self.room_code
            }
            self.network.send_message(message)
            response = self.network.receive_message()
            if response and response.get('status') == 'success':
                print("Game started!")
                self.state = MenuState.GAME
            else:
                print("Cannot start game. Need 2+ players.")
        else:
            print("Not connected to server")

    def save_network_field(self, field_index):
        """Save the current input field value"""
        if field_index == 0:
            self.server_ip = self.input_text
        elif field_index == 1:
            try:
                self.server_port = int(self.input_text)
            except:
                pass

    def handle_key_input(self, event):
        if not self.input_active:
            return
            
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            if self.state == MenuState.JOIN_ROOM:
                self.join_room(self.input_text)
            elif self.state == MenuState.SETTINGS:
                self.player_name = self.input_text
                self.state = MenuState.MAIN
                self.input_active = False
            elif self.state == MenuState.NETWORK_SETTINGS:
                self.save_network_field(self.current_input_field)
                self.confirm_network_settings()
        elif event.unicode.isprintable():
            self.input_text += event.unicode

    def confirm_network_settings(self):
        """Confirm network settings and connect"""
        try:
            self.server_port = int(self.server_port) if isinstance(self.server_port, str) else self.server_port
            
            self.network = NetworkClient(host=self.server_ip, port=self.server_port)
            if self.network.connect():
                self.state = MenuState.MAIN
                self.input_active = False
                print("Connected successfully!")
            else:
                print("Failed to connect to server. Make sure server is running.")
                self.state = MenuState.NETWORK_SETTINGS
                self.current_input_field = 0
                self.input_text = self.server_ip
                self.input_active = True
        except Exception as e:
            print(f"Error: {e}")
            self.state = MenuState.NETWORK_SETTINGS

    def create_room(self):
        """Create a room"""
        if not self.player_name:
            print("Error: Please set your player name first!")
            self.state = MenuState.SETTINGS
            self.input_text = ""
            self.input_active = True
            return
            
        if self.network:
            message = {'action': 'create_room', 'player_name': self.player_name}
            self.network.send_message(message)
            response = self.network.receive_message()
            if response and response.get('status') == 'success':
                self.room_code = response.get('room_code')
                self.player_count = response.get('player_count', 1)
                print(f"Room created: {self.room_code}. Players: {self.player_count}")
                self.state = MenuState.WAITING
        
    def join_room(self, code):
        """Join an existing room"""
        if not self.player_name:
            print("Error: Please set your player name first!")
            self.state = MenuState.SETTINGS
            self.input_text = ""
            self.input_active = True
            return
            
        self.room_code = code
        if self.network:
            self.network.send_join_request(code, self.player_name)
            response = self.network.receive_message()
            if response and response.get('status') == 'success':
                self.player_count = response.get('player_count', 1)
                print(f"Joined room. Players: {self.player_count}")
                self.state = MenuState.WAITING
            else:
                error_msg = response.get('message', 'Failed to join')
                print(f"Failed to join: {error_msg}")

    def check_player_count(self):
        """Poll server for current player count"""
        if self.network and self.room_code:
            try:
                message = {
                    'action': 'get_player_count',
                    'room_code': self.room_code
                }
                self.network.send_message(message)
                response = self.network.receive_message()
                if response and response.get('status') == 'success':
                    self.player_count = response.get('player_count', 1)
            except Exception as e:
                print(f"Error checking player count: {e}")

    def generate_room_code(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def update(self):
        """Update game state"""
        if self.state == MenuState.WAITING:
            current_time = time.time()
            if current_time - self.last_count_check > 1:
                self.last_count_check = current_time
                self.check_player_count()

    def draw(self):
        self.screen.fill((30, 30, 30))
        
        if self.state == MenuState.MAIN:
            self.draw_main_menu()
        elif self.state == MenuState.JOIN_ROOM:
            self.draw_join_room()
        elif self.state == MenuState.SETTINGS:
            self.draw_settings()
        elif self.state == MenuState.WAITING:
            self.draw_waiting()
        elif self.state == MenuState.NETWORK_SETTINGS:
            self.draw_network_settings()
        elif self.state == MenuState.GAME:
            self.draw_game()
        
        pygame.display.flip()

    def draw_main_menu(self):
        title = self.font_large.render("Tank Game", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        
        self.create_room_btn.draw(self.screen, self.font_medium)
        self.join_room_btn.draw(self.screen, self.font_medium)
        self.settings_btn.draw(self.screen, self.font_medium)

    def draw_join_room(self):
        title = self.font_large.render("Join Room", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))
        
        label = self.font_medium.render("Enter Room Code:", True, (255, 255, 255))
        self.screen.blit(label, (150, 250))
        
        pygame.draw.rect(self.screen, (100, 100, 100), (150, 320, 500, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), (150, 320, 500, 50), 2)
        input_text = self.font_small.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(input_text, (160, 330))
        
        back_btn = Button(50, 520, 100, 40, "Back")
        back_btn.draw(self.screen, self.font_small)

    def draw_settings(self):
        title = self.font_large.render("Player Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))
        
        label = self.font_medium.render("Enter Player Name:", True, (255, 255, 255))
        self.screen.blit(label, (150, 250))
        
        pygame.draw.rect(self.screen, (100, 100, 100), (150, 320, 500, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), (150, 320, 500, 50), 2)
        input_text = self.font_small.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(input_text, (160, 330))
        
        back_btn = Button(50, 520, 100, 40, "Back")
        back_btn.draw(self.screen, self.font_small)

    def draw_waiting(self):
        title = self.font_large.render("Waiting for Players", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
        
        code_text = self.font_medium.render(f"Room Code: {self.room_code}", True, (100, 255, 100))
        self.screen.blit(code_text, (self.width // 2 - code_text.get_width() // 2, 150))
        
        player_text = self.font_small.render(f"Player: {self.player_name}", True, (200, 200, 200))
        self.screen.blit(player_text, (self.width // 2 - player_text.get_width() // 2, 230))
        
        count_text = self.font_small.render(f"Players in Room: {self.player_count}/4", True, (100, 200, 100))
        self.screen.blit(count_text, (self.width // 2 - count_text.get_width() // 2, 280))
        
        if self.player_count >= 2:
            info = self.font_small.render("Ready to start! Click Start Game.", True, (100, 255, 100))
        else:
            info = self.font_small.render(f"Waiting for {2 - self.player_count} more player(s)...", True, (200, 200, 200))
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 330))
        
        if self.player_count >= 2:
            start_btn = Button(300, 410, 200, 50, "Start Game")
            start_btn.draw(self.screen, self.font_small)
        
        leave_btn = Button(50, 520, 100, 40, "Leave")
        leave_btn.draw(self.screen, self.font_small)

    def draw_game(self):
        title = self.font_large.render("GAME STARTED!", True, (100, 255, 100))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 200))
        
        info = self.font_medium.render(f"Room: {self.room_code}", True, (200, 200, 200))
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 300))
        
        players = self.font_small.render(f"Players: {self.player_count}", True, (200, 200, 200))
        self.screen.blit(players, (self.width // 2 - players.get_width() // 2, 380))
        
        msg = self.font_small.render("Game logic coming soon...", True, (150, 150, 150))
        self.screen.blit(msg, (self.width // 2 - msg.get_width() // 2, 450))
        
        exit_btn = Button(300, 520, 200, 40, "Exit Game")
        exit_btn.draw(self.screen, self.font_small)

    def draw_network_settings(self):
        title = self.font_large.render("Network Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 30))
        
        label = self.font_small.render("Server IP:", True, (255, 255, 255))
        self.screen.blit(label, (150, 150))
        pygame.draw.rect(self.screen, (100, 100, 100), (150, 170, 500, 40))
        pygame.draw.rect(self.screen, (255, 255, 255) if self.current_input_field == 0 else (100, 100, 100), (150, 170, 500, 40), 2)
        display_text = self.input_text if self.current_input_field == 0 else self.server_ip
        text = self.font_small.render(display_text, True, (255, 255, 255))
        self.screen.blit(text, (160, 177))
        
        label = self.font_small.render("Server Port:", True, (255, 255, 255))
        self.screen.blit(label, (150, 240))
        pygame.draw.rect(self.screen, (100, 100, 100), (150, 260, 500, 40))
        pygame.draw.rect(self.screen, (255, 255, 255) if self.current_input_field == 1 else (100, 100, 100), (150, 260, 500, 40), 2)
        display_text = self.input_text if self.current_input_field == 1 else str(self.server_port)
        text = self.font_small.render(display_text, True, (255, 255, 255))
        self.screen.blit(text, (160, 267))
        
        confirm_btn = Button(300, 370, 200, 50, "Confirm")
        confirm_btn.draw(self.screen, self.font_small)