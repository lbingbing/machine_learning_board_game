import enum

from PySide6 import QtCore, QtGui

from ..states import cchess_state
from ..players import cchess_player
from . import qt_game

@enum.unique
class ActionPhase(enum.Enum):
    SRC = 0
    DST = 1

class CChessWidget(qt_game.GameWidget):
    def init_state(self):
        self.state = cchess_state.create_state()

    def create_player(self, state, player_type, player_id):
        return cchess_player.create_player(state, player_type, player_id)

    def init_gui_parameters(self):
        self.unit_size = 50

    def get_transcript_save_path(self):
        return 'cchess.trans'

    def reset(self):
        super().reset()

        self.human_action_phase = ActionPhase.SRC
        self.human_action_src_position = None
        self.human_action_legal_dst_positions = []

    def reset_marker(self):
        self.src_marker = None
        self.dst_marker = None
        self.reset_legal_dst_markers()

    def set_marker(self, action):
        self.set_src_marker((action[0], action[1]))
        self.set_dst_marker((action[2], action[3]))

    def set_src_marker(self, position):
        self.src_marker = position

    def set_dst_marker(self, position):
        self.dst_marker = position

    def reset_legal_dst_markers(self):
        self.legal_dst_markers = []

    def set_legal_dst_markers(self, positions):
        self.legal_dst_markers = positions

    def handle_human_action(self, x, y):
        if not self.state.is_end() and not self.is_computer_trun():
            position = self.get_board_position(x, y)
            if position is not None:
                if self.is_self_piece(self.get_cur_player().get_player_id(), position):
                    legal_dst_positions = [(action[2], action[3]) for action in self.state.get_legal_actions(self.get_cur_player().get_player_id()) if (action[0], action[1]) == position]
                    self.human_action_phase = ActionPhase.DST
                    self.human_action_src_position = position
                    self.human_action_legal_dst_positions = legal_dst_positions
                    self.reset_marker()
                    self.set_src_marker(self.human_action_src_position)
                    self.set_legal_dst_markers(self.human_action_legal_dst_positions)
                    self.update()
                elif self.human_action_phase == ActionPhase.DST and position in self.human_action_legal_dst_positions:
                    action = (*self.human_action_src_position, *position)
                    self.apply_action(action)
                    self.reset_legal_dst_markers()
                    self.set_dst_marker(position)
                    self.human_action_phase = ActionPhase.SRC
                    self.human_action_src_position = None
                    self.human_action_legal_dst_positions = []
                    self.update()
                    self.on_action_end()

    def is_self_piece(self, player_id, position):
        return cchess_state.piece_value_to_player_id(self.state.get_board()[position[0]][position[1]]) == player_id

    def draw_board(self, painter):
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setBrush(QtCore.Qt.NoBrush)
        for i in range(1, self.state.get_board_shape()[0]+1):
            x0 = self.unit_size
            x1 = self.state.get_board_shape()[1] * self.unit_size
            y = i * self.unit_size
            painter.drawLine(x0, y, x1, y)
        for j in range(1, self.state.get_board_shape()[1]+1):
            if j == 1 or j == self.state.get_board_shape()[1]:
                x = j * self.unit_size
                y0 = self.unit_size
                y1 = self.state.get_board_shape()[0] * self.unit_size
                painter.drawLine(x, y0, x, y1)
            else:
                x = j * self.unit_size
                y0 = self.unit_size
                y1 = 5 * self.unit_size
                painter.drawLine(x, y0, x, y1)
                y0 = 6 * self.unit_size
                y1 = self.state.get_board_shape()[0] * self.unit_size
                painter.drawLine(x, y0, x, y1)
        painter.drawLine(4 * self.unit_size, 1 * self.unit_size, 6 * self.unit_size, 3 * self.unit_size)
        painter.drawLine(4 * self.unit_size, 3 * self.unit_size, 6 * self.unit_size, 1 * self.unit_size)
        painter.drawLine(4 * self.unit_size, 8 * self.unit_size, 6 * self.unit_size, 10 * self.unit_size)
        painter.drawLine(4 * self.unit_size, 10 * self.unit_size, 6 * self.unit_size, 8 * self.unit_size)

    def draw_pieces(self, painter):
        painter.setPen(QtGui.QColor(0, 0, 0))
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)
        board = self.state.get_board()
        for i in range(self.state.get_board_shape()[0]):
            for j in range(self.state.get_board_shape()[1]):
                piece_value = board[i][j]
                if piece_value != cchess_state.NUL:
                    piece_color = QtGui.QColor(255, 0, 0) if cchess_state.piece_value_to_player_id(piece_value) == 1 else QtGui.QColor(0, 0, 0)
                    painter.setPen(piece_color)
                    painter.setBrush(QtGui.QColor(255, 255, 255))
                    rect = self.get_piece_rect((i, j))
                    painter.drawEllipse(*rect)
                    painter.setBrush(piece_color)
                    piece_name = cchess_state.piece_value_to_name(piece_value)
                    painter.drawText(*rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, piece_name)

    def draw_marker(self, painter):
        self.draw_src_marker(painter)
        self.draw_dst_marker(painter)
        self.draw_legal_dst_markers(painter)

    def draw_src_marker(self, painter):
        if self.src_marker is not None:
            painter.setPen(QtGui.QColor(255, 0, 0))
            painter.setBrush(QtCore.Qt.NoBrush)
            rect = self.get_piece_rect(self.src_marker)
            painter.drawRect(*rect)

    def draw_dst_marker(self, painter):
        if self.dst_marker is not None:
            painter.setPen(QtGui.QColor(0, 255, 0))
            painter.setBrush(QtCore.Qt.NoBrush)
            rect = self.get_piece_rect(self.dst_marker)
            painter.drawRect(*rect)

    def draw_legal_dst_markers(self, painter):
        painter.setPen(QtGui.QColor(0, 0, 255))
        painter.setBrush(QtCore.Qt.NoBrush)
        for dst_position in self.human_action_legal_dst_positions:
            rect = self.get_piece_rect(dst_position)
            painter.drawRect(*rect)

qt_game.main(CChessWidget)
