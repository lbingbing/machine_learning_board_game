from ..states import othello_state
from ..players import othello_player
from . import cmd_game

state = othello_state.create_state()
cmd_game.main(state, othello_player.create_player)
