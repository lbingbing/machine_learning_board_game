from ..states import othello_state
from ..players import othello_player

def create_state():
    return othello_state.create_state()

def create_player(state, player_type, player_id):
    return othello_player.create_player(state, player_type, player_id)

def get_unit_size():
    return 40

def get_transcript_save_path():
    return 'othello.trans'
