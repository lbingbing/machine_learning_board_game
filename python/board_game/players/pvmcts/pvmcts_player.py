from .. import player
from ..model import model_player
from . import pvmcts

class PVMctsPlayer(model_player.ModelPlayer):
    def __init__(self, player_id, model, sim_num):
        super().__init__(player_id, model)

        self.sim_num = sim_num

    def get_action(self, state):
        player.Player.get_action(self, state)
        pvmcts_tree = pvmcts.PVMctsTree(self.model, state, self.player_id, self.sim_num, is_training=False, dirichlet_factor=None, dirichlet_alpha=None)
        return pvmcts_tree.get_action(state, self.player_id)
