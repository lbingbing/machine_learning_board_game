from . import blackwhite_qt_game
from . import tictactoe_qt_game_utils
from . import qt_game

class TicTacToeWidget(blackwhite_qt_game.BlackWhiteGameWidget):
    def create_state(self):
        return tictactoe_qt_game_utils.create_state()

    def create_player(self, state, player_type, player_id):
        return tictactoe_qt_game_utils.create_player(state, player_type, player_id)

    def get_unit_size(self):
        return tictactoe_qt_game_utils.get_unit_size()

    def get_transcript_save_path(self):
        return tictactoe_qt_game_utils.get_transcript_save_path()

qt_game.main(TicTacToeWidget)
