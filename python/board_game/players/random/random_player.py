import random

from .. import player

class RandomPlayer(player.Player):
    def get_type(self):
        return player.RANDOM_PLAYER

    def get_action(self, state):
        super().get_action(state)
        return random.choice(state.get_legal_actions(self.player_id))
