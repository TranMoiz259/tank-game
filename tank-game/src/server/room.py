class Room:
    def __init__(self, room_code, max_players=2):
        self.room_code = room_code
        self.players = []
        self.max_players = max_players

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        return False

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
            return True
        return False

    def is_full(self):
        return len(self.players) >= self.max_players

    def get_player_list(self):
        return self.players

    def get_room_code(self):
        return self.room_code

    def reset_room(self):
        self.players = []