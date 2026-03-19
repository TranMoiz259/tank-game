import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from src.client.menu import Menu
from src.server.server_gui import ServerGUI

class LauncherMenu:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tank Game Launcher")
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.running = True
        
    def run(self):
        """Show launcher menu"""
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.handle_events()
            self.draw()
        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
    
    def handle_click(self, pos):
        # Client button
        if pygame.Rect(150, 250, 500, 80).collidepoint(pos):
            self.running = False
            pygame.quit()
            menu = Menu()
            menu.run()
            sys.exit()
        
        # Server button
        elif pygame.Rect(150, 370, 500, 80).collidepoint(pos):
            self.running = False
            pygame.quit()
            server_gui = ServerGUI('0.0.0.0', 12345)
            server_gui.run()
            sys.exit()
    
    def draw(self):
        if not pygame.display.get_surface():
            return
            
        self.screen.fill((30, 30, 30))
        
        title = self.font_large.render("Tank Game", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 80))
        
        subtitle = self.font_medium.render("Select Mode", True, (200, 200, 200))
        self.screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 160))
        
        # Client button
        pygame.draw.rect(self.screen, (100, 100, 100), (150, 250, 500, 80))
        pygame.draw.rect(self.screen, (255, 255, 255), (150, 250, 500, 80), 2)
        client_text = self.font_medium.render("Play Game (Client)", True, (255, 255, 255))
        self.screen.blit(client_text, (self.width // 2 - client_text.get_width() // 2, 270))
        
        # Server button
        pygame.draw.rect(self.screen, (100, 100, 100), (150, 370, 500, 80))
        pygame.draw.rect(self.screen, (255, 255, 255), (150, 370, 500, 80), 2)
        server_text = self.font_medium.render("Start Server", True, (255, 255, 255))
        self.screen.blit(server_text, (self.width // 2 - server_text.get_width() // 2, 390))
        
        pygame.display.flip()

def main():
    launcher = LauncherMenu()
    launcher.run()

if __name__ == "__main__":
    main()