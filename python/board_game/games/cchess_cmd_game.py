from ..states import cchess_state
from ..players import cchess_player
from . import cmd_game

state = cchess_state.create_state()
cmd_game.main(state, cchess_player.create_player)
