from ..states import tictactoe_state
from ..players import tictactoe_player
from . import cmd_game

state = tictactoe_state.create_state()
cmd_game.main(state, tictactoe_player.create_player)
