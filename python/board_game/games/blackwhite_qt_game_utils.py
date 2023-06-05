from PySide6 import QtCore, QtGui

from ..states import blackwhite_state

def draw_board(state, unit_size, painter):
    painter.setPen(QtGui.QColor(0, 0, 0))
    painter.setBrush(QtCore.Qt.NoBrush)
    for i in range(1, state.get_board_shape()[0]+1):
        x0 = unit_size
        x1 = state.get_board_shape()[1] * unit_size
        y = i * unit_size
        painter.drawLine(x0, y, x1, y)
    for j in range(1, state.get_board_shape()[1]+1):
        x = j * unit_size
        y0 = unit_size
        y1 = state.get_board_shape()[0] * unit_size
        painter.drawLine(x, y0, x, y1)

def draw_pieces(state, get_piece_rect, painter):
    painter.setPen(QtGui.QColor(0, 0, 0))
    board = state.get_board()
    for i in range(state.get_board_shape()[0]):
        for j in range(state.get_board_shape()[1]):
            piece = board[i][j]
            if piece != 0:
                piece_color = QtGui.QColor(0, 0, 0) if blackwhite_state.piece_value_to_player_id(piece) == 1 else QtGui.QColor(255, 255, 255)
                painter.setBrush(piece_color)
                rect = get_piece_rect((i, j))
                painter.drawEllipse(*rect)

def draw_marker(marker, get_piece_rect, painter):
    if marker is not None:
        painter.setPen(QtGui.QColor(0, 255, 0))
        painter.setBrush(QtCore.Qt.NoBrush)
        rect = get_piece_rect(marker)
        painter.drawRect(*rect)
