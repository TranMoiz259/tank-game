import pygame
import random
import string
from enum import Enum

class MenuState(Enum):
    MAIN = 1
    CREATE_ROOM = 2
    JOIN_ROOM = 3
    SETTINGS = 4
    WAITING = 5

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
    def __init__(self, server_connection=None):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tank Game")
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.state = MenuState.MAIN
        self.running = True
        self.player_name = ""
        self.room_code = ""
        self.server = server_connection
        self.input_text = ""
        self.input_active = False
        
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
            elif event.type == pygame.KEYDOWN and self.input_active:
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
                self.input_text = ""
                self.input_active = True

    def handle_key_input(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            if self.state == MenuState.JOIN_ROOM:
                self.join_room(self.input_text)
            elif self.state == MenuState.SETTINGS:
                self.player_name = self.input_text
                self.state = MenuState.MAIN
                self.input_active = False
        elif event.unicode.isprintable():
            self.input_text += event.unicode

    def create_room(self):
        self.room_code = self.generate_room_code()
        self.state = MenuState.WAITING
        print(f"Room created with code: {self.room_code}")

    def join_room(self, code):
            self.room_code = code
            if self.server:
                self.server.send_join_request(code, self.player_name)
            self.state = MenuState.WAITING
            print(f"Attempting to join room: {self.room_code}")


    def generate_room_code(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def update(self):
        pass

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

    def draw_settings(self):
        title = self.font_large.render("Player Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))
        
        label = self.font_medium.render("Enter Player Name:", True, (255, 255, 255))
        self.screen.blit(label, (150, 250))
        
        pygame.draw.rect(self.screen, (100, 100, 100), (150, 320, 500, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), (150, 320, 500, 50), 2)
        input_text = self.font_small.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(input_text, (160, 330))

    def draw_waiting(self):
        title = self.font_large.render("Waiting for Players", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 150))
        
        code_text = self.font_medium.render(f"Room Code: {self.room_code}", True, (100, 255, 100))
        self.screen.blit(code_text, (self.width // 2 - code_text.get_width() // 2, 300))
        
        info = self.font_small.render("Waiting for at least 2 players to start...", True, (200, 200, 200))
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 400))