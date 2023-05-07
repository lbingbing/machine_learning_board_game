from ..states import gomoku_state
from ..players import gomoku_player
from . import qt_game
from . import blackwhite_qt_game

class GomokuWidget(blackwhite_qt_game.BlackWhiteGameWidget):
    def init_state(self):
        self.state = gomoku_state.create_state()

    def create_player(self, state, player_type, player_id):
        return gomoku_player.create_player(state, player_type, player_id)

    def init_gui_parameters(self):
        self.unit_size = 40

    def get_transcript_save_path(self):
        return 'gomoku.trans'

qt_game.main(GomokuWidget)
