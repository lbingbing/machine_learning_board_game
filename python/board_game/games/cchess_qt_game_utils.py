from PySide6 import QtCore, QtGui

from ..states import cchess_state
from ..players import cchess_player

def create_state():
    return cchess_state.create_state()

def create_player(state, player_type, player_id):
    return cchess_player.create_player(state, player_type, player_id)

def get_unit_size():
    return 50

def get_transcript_save_path():
    return 'cchess.trans'

def draw_board(state, unit_size, painter):
    painter.setPen(QtGui.QColor(0, 0, 0))
    painter.setBrush(QtCore.Qt.NoBrush)
    for i in range(1, state.get_board_shape()[0]+1):
        x0 = unit_size
        x1 = state.get_board_shape()[1] * unit_size
        y = i * unit_size
        painter.drawLine(x0, y, x1, y)
    for j in range(1, state.get_board_shape()[1]+1):
        if j == 1 or j == state.get_board_shape()[1]:
            x = j * unit_size
            y0 = unit_size
            y1 = state.get_board_shape()[0] * unit_size
            painter.drawLine(x, y0, x, y1)
        else:
            x = j * unit_size
            y0 = unit_size
            y1 = 5 * unit_size
            painter.drawLine(x, y0, x, y1)
            y0 = 6 * unit_size
            y1 = state.get_board_shape()[0] * unit_size
            painter.drawLine(x, y0, x, y1)
    painter.drawLine(4 * unit_size, 1 * unit_size, 6 * unit_size, 3 * unit_size)
    painter.drawLine(4 * unit_size, 3 * unit_size, 6 * unit_size, 1 * unit_size)
    painter.drawLine(4 * unit_size, 8 * unit_size, 6 * unit_size, 10 * unit_size)
    painter.drawLine(4 * unit_size, 10 * unit_size, 6 * unit_size, 8 * unit_size)

def draw_pieces(state, get_piece_rect, painter):
    painter.setPen(QtGui.QColor(0, 0, 0))
    font = painter.font()
    font.setPointSize(20)
    painter.setFont(font)
    board = state.get_board()
    for i in range(state.get_board_shape()[0]):
        for j in range(state.get_board_shape()[1]):
            piece_value = board[i][j]
            if piece_value != cchess_state.NUL:
                piece_color = QtGui.QColor(255, 0, 0) if cchess_state.piece_value_to_player_id(piece_value) == 1 else QtGui.QColor(0, 0, 0)
                painter.setPen(piece_color)
                painter.setBrush(QtGui.QColor(255, 255, 255))
                rect = get_piece_rect((i, j))
                painter.drawEllipse(*rect)
                painter.setBrush(piece_color)
                piece_name = cchess_state.piece_value_to_name(piece_value)
                painter.drawText(*rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, piece_name)

def draw_src_marker(src_marker, get_piece_rect, painter):
    if src_marker is not None:
        painter.setPen(QtGui.QColor(255, 0, 0))
        painter.setBrush(QtCore.Qt.NoBrush)
        rect = get_piece_rect(src_marker)
        painter.drawRect(*rect)

def draw_dst_marker(dst_marker, get_piece_rect, painter):
    if dst_marker is not None:
        painter.setPen(QtGui.QColor(0, 255, 0))
        painter.setBrush(QtCore.Qt.NoBrush)
        rect = get_piece_rect(dst_marker)
        painter.drawRect(*rect)

def draw_legal_dst_markers(legal_dst_markers, get_piece_rect, painter):
    painter.setPen(QtGui.QColor(0, 0, 255))
    painter.setBrush(QtCore.Qt.NoBrush)
    for dst_marker in legal_dst_markers:
        rect = get_piece_rect(dst_marker)
        painter.drawRect(*rect)
