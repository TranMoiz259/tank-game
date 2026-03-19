from random import randint

class GameLogic:
    def __init__(self):
        self.players = {}
        self.scores = {}
        self.game_state = "waiting"  # possible states: waiting, playing, finished

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players[player_id] = {"position": (0, 0), "lives": 3}
            self.scores[player_id] = 0

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            del self.scores[player_id]

    def update_position(self, player_id, new_position):
        if player_id in self.players:
            self.players[player_id]["position"] = new_position

    def shoot(self, player_id):
        if player_id in self.players:
            # Logic for shooting
            pass

    def check_collision(self, player_id):
        # Logic for checking collisions with walls or other players
        pass

    def update_scores(self, player_id, points):
        if player_id in self.scores:
            self.scores[player_id] += points

    def generate_room_code(self):
        return f"{randint(1000, 9999)}"

    def start_game(self):
        if len(self.players) > 1:
            self.game_state = "playing"

    def end_game(self):
        self.game_state = "finished"
        # Logic to determine winner and reset game state
        pass

    def reset_game(self):
        self.players.clear()
        self.scores.clear()
        self.game_state = "waiting"