from .. import player
from . import mcts

class MctsPlayer(player.Player):
    def __init__(self, player_id, sim_num):
        super().__init__(player_id)

        self.sim_num = sim_num

    def get_type(self):
        return player.MCTS_PLAYER

    def get_action(self, state):
        super().get_action(state)
        mcts_tree = mcts.MctsTree(state, self.player_id, self.sim_num)
        return mcts_tree.get_action(state, self.player_id)
