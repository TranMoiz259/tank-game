import pygame
import random
import math

class Game:
    def __init__(self, room_code, players, player_name):
        self.room_code = room_code
        self.players = players  # List of player names
        self.player_name = player_name
        self.width = 1000
        self.height = 700
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tank Game - Battle")
        
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.countdown = 3
        self.countdown_timer = 0
        self.game_started = False
        self.kill_counts = {player: 0 for player in players}
        self.alive_players = set(players)
        
        # Generate maze
        self.maze = self.generate_maze()
        self.player_tanks = self.spawn_players()
        
    def generate_maze(self):
        """Generate random maze"""
        cell_size = 50
        cols = self.width // cell_size
        rows = self.height // cell_size
        
        maze = [[{'walls': {'N': True, 'S': True, 'E': True, 'W': True}, 'visited': False} 
                 for _ in range(cols)] for _ in range(rows)]
        
        # Simple random maze generation
        def carve(x, y):
            maze[y][x]['visited'] = True
            directions = [(0, -1, 'N', 'S'), (0, 1, 'S', 'N'), 
                         (-1, 0, 'W', 'E'), (1, 0, 'E', 'W')]
            random.shuffle(directions)
            
            for dx, dy, wall1, wall2 in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and not maze[ny][nx]['visited']:
                    maze[y][x]['walls'][wall1] = False
                    maze[ny][nx]['walls'][wall2] = False
                    carve(nx, ny)
        
        carve(0, 0)
        return maze
    
    def spawn_players(self):
        """Spawn players at random locations"""
        tanks = {}
        cell_size = 50
        
        for player in self.players:
            while True:
                x = random.randint(0, len(self.maze[0]) - 1)
                y = random.randint(0, len(self.maze) - 1)
                # Check if not occupied
                if not any(t['x'] == x and t['y'] == y for t in tanks.values()):
                    tanks[player] = {
                        'x': x * cell_size + cell_size // 2,
                        'y': y * cell_size + cell_size // 2,
                        'angle': random.randint(0, 359),
                        'alive': True
                    }
                    break
        
        return tanks
    
    def draw_maze(self):
        """Draw the maze"""
        cell_size = 50
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                rect_x = x * cell_size
                rect_y = y * cell_size
                
                # Draw walls
                if cell['walls']['N']:
                    pygame.draw.line(self.screen, (255, 255, 255), 
                                   (rect_x, rect_y), (rect_x + cell_size, rect_y), 2)
                if cell['walls']['S']:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                   (rect_x, rect_y + cell_size), (rect_x + cell_size, rect_y + cell_size), 2)
                if cell['walls']['W']:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                   (rect_x, rect_y), (rect_x, rect_y + cell_size), 2)
                if cell['walls']['E']:
                    pygame.draw.line(self.screen, (255, 255, 255),
                                   (rect_x + cell_size, rect_y), (rect_x + cell_size, rect_y + cell_size), 2)
    
    def draw_players(self):
        """Draw player tanks"""
        for player_name, tank in self.player_tanks.items():
            if tank['alive']:
                # Draw tank body
                color = (100, 255, 100) if player_name == self.player_name else (100, 100, 255)
                pygame.draw.circle(self.screen, color, (int(tank['x']), int(tank['y'])), 15)
                
                # Draw tank barrel
                end_x = tank['x'] + 20 * math.cos(math.radians(tank['angle']))
                end_y = tank['y'] + 20 * math.sin(math.radians(tank['angle']))
                pygame.draw.line(self.screen, color, (tank['x'], tank['y']), (end_x, end_y), 3)
                
                # Draw player name
                name_text = self.font_small.render(player_name, True, color)
                self.screen.blit(name_text, (tank['x'] - 20, tank['y'] - 35))
    
    def draw_ui(self):
        """Draw UI elements"""
        # Countdown
        if not self.game_started:
            countdown_text = self.font_large.render(str(self.countdown), True, (255, 100, 100))
            self.screen.blit(countdown_text, (self.width // 2 - countdown_text.get_width() // 2, 50))
        
        # Kill counts
        y_offset = 20
        for player_name in self.players:
            kills = self.kill_counts[player_name]
            color = (100, 255, 100) if player_name == self.player_name else (100, 100, 255)
            kill_text = self.font_small.render(f"{player_name}: {kills} kills", True, color)
            self.screen.blit(kill_text, (20, y_offset))
            y_offset += 30
        
        # Players alive
        alive_text = self.font_small.render(f"Alive: {len(self.alive_players)}", True, (200, 200, 200))
        self.screen.blit(alive_text, (self.width - 200, 20))
    
    def update_countdown(self):
        """Update countdown"""
        self.countdown_timer += 1
        if self.countdown_timer >= 60:  # 1 second at 60 FPS
            self.countdown_timer = 0
            self.countdown -= 1
            if self.countdown < 0:
                self.game_started = True
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while self.running:
            clock.tick(60)
            self.handle_events()
            
            if not self.game_started:
                self.update_countdown()
            
            self.draw()
        
        pygame.quit()

    def update(self):
        """Update game state"""
        if not self.game_started:
            self.update_countdown()
        else:
            # Update player positions, bullets, collisions, etc.
            pass
    
    def update_countdown(self):
        """Update countdown"""
        self.countdown_timer += 1
        if self.countdown_timer >= 60:  # 1 second at 60 FPS
            self.countdown_timer = 0
            self.countdown -= 1
            if self.countdown < 0:
                self.game_started = True
    
    def handle_events(self, event):
        """Handle user input during game"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle shooting, etc.
            pass
    
    def draw(self):
        """Draw game screen"""
        self.screen.fill((30, 30, 30))
        
        self.draw_maze()
        self.draw_players()
        self.draw_ui()
        
        pygame.display.flip()