from ..states import othello_state
from ..players import othello_player
from . import game_regression

state = othello_state.create_state()
game_regression.main(state, othello_player.create_player)
