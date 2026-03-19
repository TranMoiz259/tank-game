class Player:
    def __init__(self, player_id, name, position, score=0):
        self.player_id = player_id
        self.name = name
        self.position = position  # (x, y) coordinates
        self.score = score

class Room:
    def __init__(self, room_code, players=None):
        self.room_code = room_code
        self.players = players if players is not None else []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player_id):
        self.players = [player for player in self.players if player.player_id != player_id]

    def is_full(self):
        return len(self.players) >= 4  # Assuming a max of 4 players per room

class GameState:
    def __init__(self, room_code, players, game_status='waiting'):
        self.room_code = room_code
        self.players = players  # List of Player objects
        self.game_status = game_status  # 'waiting', 'in_progress', 'finished'