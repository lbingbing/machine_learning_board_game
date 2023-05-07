from ..states import gomoku_state
from ..players import gomoku_player
from . import cmd_game

state = gomoku_state.create_state()
cmd_game.main(state, gomoku_player.create_player)
