class Room:
    def __init__(self, room_code):
        self.room_code = room_code
        self.players = []
        self.max_players = 4
        self.game_started = False

    def add_player(self, player_name):
        """Add a player to the room"""
        if len(self.players) < self.max_players:
            self.players.append(player_name)
            return True
        return False

    def get_player_count(self):
        """Get current player count"""
        return len(self.players)

    def start_game(self):
        """Start the game if conditions are met"""
        if len(self.players) >= 2:
            self.game_started = True
            return True
        return False

    def reset_game(self):
        """Reset game state for new round"""
        self.game_started = False