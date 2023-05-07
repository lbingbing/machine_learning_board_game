from ..states import cchess_state
from ..players import cchess_player
from . import game_regression

state = cchess_state.create_state()
game_regression.main(state, cchess_player.create_player)
