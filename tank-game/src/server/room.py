class Room:
    def __init__(self, room_code):
        self.room_code = room_code
        self.players = []
        self.max_players = 4
        self.status = "waiting"  # waiting, playing, finished

    def add_player(self, player_name):
        if len(self.players) < self.max_players:
            self.players.append(player_name)
            print(f"Player {player_name} added. Total: {len(self.players)}/{self.max_players}")
            return True
        return False

    def get_player_count(self):
        return len(self.players)

    def start_game(self):
        if len(self.players) >= 2:
            self.status = "playing"
            return True
        return False