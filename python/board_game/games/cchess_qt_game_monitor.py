from ..states import cchess_state
from . import cchess_qt_game_utils
from . import qt_game_monitor

class CChessMonitorWidget(qt_game_monitor.GameMonitorWidget):
    def create_state(self):
        return cchess_qt_game_utils.create_state()

    def get_unit_size(self):
        return cchess_qt_game_utils.get_unit_size()

    def reset_marker(self):
        self.src_marker = None
        self.dst_marker = None

    def set_marker(self, action):
        self.set_src_marker((action[0], action[1]))
        self.set_dst_marker((action[2], action[3]))

    def set_src_marker(self, position):
        self.src_marker = position

    def set_dst_marker(self, position):
        self.dst_marker = position

    def draw_board(self, painter):
        cchess_qt_game_utils.draw_board(self.state, self.unit_size, painter)

    def draw_pieces(self, painter):
        cchess_qt_game_utils.draw_pieces(self.state, self.get_piece_rect, painter)

    def draw_marker(self, painter):
        cchess_qt_game_utils.draw_src_marker(self.src_marker, self.get_piece_rect, painter)
        cchess_qt_game_utils.draw_dst_marker(self.dst_marker, self.get_piece_rect, painter)

qt_game_monitor.main(CChessMonitorWidget)
