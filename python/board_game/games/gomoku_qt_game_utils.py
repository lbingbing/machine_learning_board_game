from ..states import gomoku_state
from ..players import gomoku_player

def create_state():
    return gomoku_state.create_state()

def create_player(state, player_type, player_id):
    return gomoku_player.create_player(state, player_type, player_id)

def get_unit_size():
    return 40

def get_transcript_save_path():
    return 'gomoku.trans'
