from ..states import gomoku_state
from ..players import gomoku_player
from . import game_regression

state = gomoku_state.create_state()
game_regression.main(state, gomoku_player.create_player)
