from ..states import tictactoe_state
from ..players import tictactoe_player

def create_state():
    return tictactoe_state.create_state()

def create_player(state, player_type, player_id):
    return tictactoe_player.create_player(state, player_type, player_id)

def get_unit_size():
    return 40

def get_transcript_save_path():
    return 'tictactoe.trans'
