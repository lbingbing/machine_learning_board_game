from . import gmcc_table_model
from ..model import model_player

def create_model(state):
    return gmcc_table_model.GMCCTableModel(state.get_name(), state.get_state_dim(), state.get_action_dim())

def create_player(player_id, state):
    return model_player.ModelPlayer(player_id, create_model(state))
