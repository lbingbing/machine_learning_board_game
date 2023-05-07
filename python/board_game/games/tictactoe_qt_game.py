from ..states import tictactoe_state
from ..players import tictactoe_player
from . import qt_game
from . import blackwhite_qt_game

class TicTacToeWidget(blackwhite_qt_game.BlackWhiteGameWidget):
    def init_state(self):
        self.state = tictactoe_state.create_state()

    def create_player(self, state, player_type, player_id):
        return tictactoe_player.create_player(state, player_type, player_id)

    def init_gui_parameters(self):
        self.unit_size = 40

    def get_transcript_save_path(self):
        return 'tictactoe.trans'

qt_game.main(TicTacToeWidget)
