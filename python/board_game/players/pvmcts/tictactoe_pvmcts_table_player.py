from . import pvmcts_table_model
from . import pvmcts_player

def create_model(state):
    return pvmcts_table_model.PVMctsTableModel(state.get_name(), state.get_state_dim(), state.get_action_dim())

def create_player(player_id, state, sim_num):
    return pvmcts_player.PVMctsPlayer(player_id, create_model(state), sim_num)
