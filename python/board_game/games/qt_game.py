import argparse
import sys
import time
import threading
import queue

from PySide6 import QtCore, QtGui, QtWidgets

from ..players import player
from . import utils

class GameWidget(QtWidgets.QWidget):
    def __init__(self, player_types, is_save_transcript):
        super().__init__()

        self.is_save_transcript = is_save_transcript

        self.init_state()
        self.init_players(player_types)
        self.has_human_player = any(player.is_human(p) for p in self.players)

        self.init_gui_parameters()
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFixedSize(self.unit_size * (self.state.get_board_shape()[1] + 1), self.unit_size * (self.state.get_board_shape()[0] + 1))
        self.installEventFilter(self)

        self.init_get_action_worker()

        self.reset()

    def init_state(self):
        raise NotImplementedError()

    def init_players(self, player_types):
        self.players = [self.create_player(self.state, player_type, player_id) for player_id, player_type in enumerate(player_types, 1)]

    def create_player(self, state, player_type, player_id):
        raise NotImplementedError()

    def init_gui_parameters(self):
        raise NotImplementedError()

    def init_get_action_worker(self):
        self.computer_step_delay = 0.5
        self.computer_action_polling_interval = 0.1

        self.computer_action_requested = False

        self.request_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self.get_action_worker)
        self.worker_thread.start()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(self.computer_action_polling_interval * 1000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.poll_computer_action)

    def get_action_worker(self):
        while True:
            item = self.request_queue.get()
            if item is None:
                break
            func, arg = item
            action = func(arg)
            time.sleep(self.computer_step_delay)
            self.response_queue.put(action)

    def stop_get_action_worker(self):
        self.request_queue.put(None)
        self.worker_thread.join()

    def stop_compute_action_request(self):
        if self.timer.isActive():
            self.timer.stop()
        if self.computer_action_requested:
            self.response_queue.get()
            self.computer_action_requested = False

    def reset(self):
        self.stop_compute_action_request()

        self.cur_player_index = 0
        self.state.reset()
        self.actions = []
        self.reset_marker()
        self.update()

    def start(self):
        if self.is_computer_trun():
            self.computer_step()

    def get_cur_player(self):
        return self.players[self.cur_player_index]

    def toggle_player(self):
        self.cur_player_index = (self.cur_player_index + 1) % len(self.players)

    def is_computer_trun(self):
        return not player.is_human(self.get_cur_player())

    def computer_step(self):
        self.request_computer_action()

    def request_computer_action(self):
        self.request_queue.put((self.get_cur_player().get_action, self.state))
        self.computer_action_requested = True
        self.timer.start()

    def poll_computer_action(self):
        try:
            action = self.response_queue.get(block=False)
            self.computer_action_requested = False
            self.apply_action(action)
            self.set_marker(action)
            self.update()
            self.on_action_end()
        except queue.Empty:
            self.timer.start()

    def handle_human_action(self, x, y):
        raise NotImplementedError()

    def apply_action(self, action):
        self.state.do_action(self.get_cur_player().get_player_id(), action)
        self.actions.append(action)
        self.update()

    def on_action_end(self):
        result = self.state.get_result()
        if result >= 0:
            if result > 0:
                msg = 'player {} ({}) wins'.format(result, self.get_cur_player().get_type())
                QtWidgets.QMessageBox.information(self, 'Info', msg)
            elif result == 0:
                msg = 'draw'
                QtWidgets.QMessageBox.information(self, 'Info', msg)
            if self.is_save_transcript:
                save_transcript(self.get_transcript_save_path(), self.actions)
        else:
            self.toggle_player()
            if self.is_computer_trun():
                self.computer_step()

    def get_transcript_save_path(self):
        raise NotImplementedError()

    def reset_marker(self):
        raise NotImplementedError()

    def set_marker(self, action):
        raise NotImplementedError()

    def get_board_position(self, x, y):
        if x < self.unit_size / 2 or \
           y < self.unit_size / 2 or \
           x > self.unit_size * (self.state.get_board_shape()[1] + 1) - self.unit_size / 2 or \
           y > self.unit_size * (self.state.get_board_shape()[0] + 1) - self.unit_size / 2:
            return None
        j = int(x / self.unit_size - 0.5)
        i = int(y / self.unit_size - 0.5)
        return i, j

    def get_piece_rect(self, position):
        x = (position[1] + 0.5) * self.unit_size
        y = (position[0] + 0.5) * self.unit_size
        w = self.unit_size
        h = self.unit_size
        return x, y, w, h

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.draw_background(painter)
        self.draw_board(painter)
        self.draw_pieces(painter)
        self.draw_marker(painter)

    def draw_background(self, painter):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(255, 255, 255))
        painter.drawRect(self.rect())

    def draw_board(self, painter):
        raise NotImplementedError()

    def draw_pieces(self, painter):
        raise NotImplementedError()

    def draw_marker(self, painter):
        raise NotImplementedError()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                self.reset()
                self.start()
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                if self.has_human_player:
                    self.handle_human_action(event.pos().x(), event.pos().y())
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        self.stop_compute_action_request()
        self.stop_get_action_worker()

def main(Widget):
    parser = argparse.ArgumentParser()
    player.add_player_options(parser)
    utils.add_game_options(parser)
    args = parser.parse_args()

    app = QtWidgets.QApplication([])
    widget = Widget((args.player_type1, args.player_type2), args.save_transcript)
    widget.show()
    sys.exit(app.exec())
