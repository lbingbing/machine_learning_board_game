from ..states import tictactoe_state
from ..players import tictactoe_player
from . import game_regression

state = tictactoe_state.create_state()
game_regression.main(state, tictactoe_player.create_player)
