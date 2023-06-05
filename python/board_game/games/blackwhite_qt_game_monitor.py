from . import blackwhite_qt_game_utils
from . import qt_game_monitor

class BlackWhiteGameMonitorWidget(qt_game_monitor.GameMonitorWidget):
    def reset_marker(self):
        self.marker = None

    def set_marker(self, action):
        self.marker = action

    def draw_board(self, painter):
        blackwhite_qt_game_utils.draw_board(self.state, self.unit_size, painter)

    def draw_pieces(self, painter):
        blackwhite_qt_game_utils.draw_pieces(self.state, self.get_piece_rect, painter)

    def draw_marker(self, painter):
        blackwhite_qt_game_utils.draw_marker(self.marker, self.get_piece_rect, painter)
