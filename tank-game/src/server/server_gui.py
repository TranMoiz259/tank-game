import pygame
import threading
from .server import Server

class ServerGUI:
    def __init__(self, host='0.0.0.0', port=12345):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tank Game Server")
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.host = host
        self.port = port
        self.server = Server(host, port)
        self.running = True
        self.server_running = False
        self.logs = []
        self.max_logs = 15
        
    def start_server(self):
        """Start server in background thread"""
        if not self.server_running:
            self.server_running = True
            server_thread = threading.Thread(target=self.server.run)
            server_thread.daemon = True
            server_thread.start()
            self.add_log(f"Server started on {self.host}:{self.port}")
    
    def stop_server(self):
        """Stop the server"""
        if self.server_running:
            self.server_running = False
            self.add_log("Server stopping...")
    
    def add_log(self, message):
        """Add message to log"""
        self.logs.append(message)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        print(message)
    
    def run(self):
        """Main server GUI loop"""
        clock = pygame.time.Clock()
        self.start_server()
        
        while self.running:
            clock.tick(60)
            self.handle_events()
            self.draw()
        
        self.stop_server()
        pygame.quit()
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def handle_click(self, pos):
        """Handle mouse clicks on buttons"""
        # Stop button
        if pygame.Rect(300, 450, 200, 50).collidepoint(pos):
            if self.server_running:
                self.stop_server()
            else:
                self.start_server()
    
    def draw(self):
        """Draw the GUI"""
        self.screen.fill((30, 30, 30))
        
        # Title
        title = self.font_large.render("Tank Game Server", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 30))
        
        # Server status
        status_color = (100, 255, 100) if self.server_running else (255, 100, 100)
        status_text = "Running" if self.server_running else "Stopped"
        status = self.font_medium.render(f"Status: {status_text}", True, status_color)
        self.screen.blit(status, (self.width // 2 - status.get_width() // 2, 100))
        
        # Server info
        info = self.font_small.render(f"Host: {self.server.host} | Port: {self.server.port}", True, (200, 200, 200))
        self.screen.blit(info, (self.width // 2 - info.get_width() // 2, 160))
        
        # Active rooms
        room_count = len(self.server.rooms)
        rooms_text = self.font_small.render(f"Active Rooms: {room_count}", True, (100, 200, 255))
        self.screen.blit(rooms_text, (50, 220))
        
        # Player count
        total_players = sum(room.get_player_count() for room in self.server.rooms.values())
        players_text = self.font_small.render(f"Total Players: {total_players}", True, (100, 200, 255))
        self.screen.blit(players_text, (50, 260))
        
        # Logs
        log_title = self.font_small.render("Logs:", True, (200, 200, 200))
        self.screen.blit(log_title, (50, 310))
        
        for i, log in enumerate(self.logs):
            log_text = self.font_small.render(log, True, (150, 150, 150))
            self.screen.blit(log_text, (70, 340 + i * 22))
        
        # Button
        button_text = "Stop Server" if self.server_running else "Start Server"
        button_color = (200, 50, 50) if self.server_running else (50, 200, 50)
        
        pygame.draw.rect(self.screen, button_color, (300, 450, 200, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), (300, 450, 200, 50), 2)
        
        btn_text = self.font_medium.render(button_text, True, (255, 255, 255))
        self.screen.blit(btn_text, (310, 460))
        
        # Instructions
        instr = self.font_small.render("Press ESC to quit", True, (100, 100, 100))
        self.screen.blit(instr, (self.width // 2 - instr.get_width() // 2, 550))
        
        pygame.display.flip()