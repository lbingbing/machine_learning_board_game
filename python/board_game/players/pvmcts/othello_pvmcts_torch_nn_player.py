from . import pvmcts_torch_nn_model
from ..model.torch import othello_torch_network
from . import pvmcts_player

def create_model(state):
    return pvmcts_torch_nn_model.PVMctsTorchNNModel(state.get_name(), othello_torch_network.PVNetwork(state.get_state_numpy_shape(), state.get_action_dim()))

def create_player(player_id, state, sim_num):
    return pvmcts_player.PVMctsPlayer(player_id, create_model(state), sim_num)
