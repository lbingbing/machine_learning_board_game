from PySide6 import QtCore, QtGui

from ..states import blackwhite_state
from . import qt_game

class BlackWhiteGameWidget(qt_game.GameWidget):
    def handle_human_action(self, x, y):
        if not self.state.is_end() and not self.is_computer_trun():
            action = self.get_board_position(x, y)
            if action is not None and action in self.state.get_legal_actions(self.get_cur_player().get_player_id()):
                self.apply_action(action)
                self.set_marker(action)
                self.update()
                self.on_action_end()

    def reset_marker(self):
        self.marker = None

    def set_marker(self, action):
        self.marker = action

    def draw_board(self, painter):
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setBrush(QtCore.Qt.NoBrush)
        for i in range(1, self.state.get_board_shape()[0]+1):
            x0 = self.unit_size
            x1 = self.state.get_board_shape()[1] * self.unit_size
            y = i * self.unit_size
            painter.drawLine(x0, y, x1, y)
        for j in range(1, self.state.get_board_shape()[1]+1):
            x = j * self.unit_size
            y0 = self.unit_size
            y1 = self.state.get_board_shape()[0] * self.unit_size
            painter.drawLine(x, y0, x, y1)

    def draw_pieces(self, painter):
        painter.setPen(QtGui.QColor(0, 0, 0))
        board = self.state.get_board()
        for i in range(self.state.get_board_shape()[0]):
            for j in range(self.state.get_board_shape()[1]):
                piece = board[i][j]
                if piece != 0:
                    piece_color = QtGui.QColor(0, 0, 0) if blackwhite_state.piece_value_to_player_id(piece) == 1 else QtGui.QColor(255, 255, 255)
                    painter.setBrush(piece_color)
                    rect = self.get_piece_rect((i, j))
                    painter.drawEllipse(*rect)

    def draw_marker(self, painter):
        if self.marker is not None:
            painter.setPen(QtGui.QColor(0, 255, 0))
            painter.setBrush(QtCore.Qt.NoBrush)
            rect = self.get_piece_rect(self.marker)
            painter.drawRect(*rect)
