import argparse
import sys
import time
import threading
import queue

from PySide6 import QtCore, QtGui, QtWidgets

from ..players import player
from ..players.transcript import transcript_player
from . import utils

class GameWidget(QtWidgets.QWidget):
    def __init__(self, player_types, is_save_transcript):
        super().__init__()

        self.is_save_transcript = is_save_transcript

        self.state = self.create_state()
        self.players = [self.create_player(self.state, player_type, player_id) for player_id, player_type in enumerate(player_types, 1)]
        self.has_human_player = any(player.is_human(p) for p in self.players)

        self.unit_size = self.get_unit_size()
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFixedSize(self.unit_size * (self.state.get_board_shape()[1] + 1), self.unit_size * (self.state.get_board_shape()[0] + 1))
        self.installEventFilter(self)

        self.init_get_action_worker()

        self.game_num = 0

        self.reset()

    def create_state(self):
        raise NotImplementedError()

    def create_player(self, state, player_type, player_id):
        raise NotImplementedError()

    def get_unit_size(self):
        raise NotImplementedError()

    def init_get_action_worker(self):
        self.step_delay = 0.5
        self.action_polling_interval = 0.1

        self.action_requested = False

        self.get_action_request_queue = queue.Queue()
        self.get_action_response_queue = queue.Queue()
        self.get_action_worker_thread = threading.Thread(target=self.get_action_worker)
        self.get_action_worker_thread.start()

        self.poll_action_timer = QtCore.QTimer(self)
        self.poll_action_timer.setInterval(self.action_polling_interval * 1000)
        self.poll_action_timer.setSingleShot(True)
        self.poll_action_timer.timeout.connect(self.poll_action)

    def get_action_worker(self):
        while True:
            item = self.get_action_request_queue.get()
            if item is None:
                break
            func, arg = item
            action = func(arg)
            time.sleep(self.step_delay)
            self.get_action_response_queue.put(action)

    def stop_get_action_worker(self):
        self.get_action_request_queue.put(None)
        self.get_action_worker_thread.join()

    def stop_action_request(self):
        if self.poll_action_timer.isActive():
            self.poll_action_timer.stop()
        if self.action_requested:
            self.get_action_response_queue.get()
            self.action_requested = False

    def reset(self):
        self.stop_action_request()

        self.cur_player_index = 0
        self.state.reset()
        self.actions = []
        self.reset_marker()
        self.update()

    def start(self):
        if not self.is_human_turn():
            self.request_action()

    def get_cur_player(self):
        return self.players[self.cur_player_index]

    def toggle_player(self):
        self.cur_player_index = (self.cur_player_index + 1) % len(self.players)

    def is_human_turn(self):
        return player.is_human(self.get_cur_player())

    def request_action(self):
        self.get_action_request_queue.put((self.get_cur_player().get_action, self.state))
        self.action_requested = True
        self.poll_action_timer.start()

    def poll_action(self):
        try:
            action = self.get_action_response_queue.get(block=False)
            self.action_requested = False
            self.apply_action(action)
            self.set_marker(action)
            self.update()
            self.on_action_end()
        except queue.Empty:
            self.poll_action_timer.start()

    def handle_human_action(self, x, y):
        raise NotImplementedError()

    def apply_action(self, action):
        self.state.do_action(self.get_cur_player().get_player_id(), action)
        self.actions.append(action)
        self.update()

    def on_action_end(self):
        result = self.state.get_result()
        if result >= 0:
            self.game_num += 1
            if result > 0:
                msg = 'game {}, player {} ({}) wins'.format(self.game_num, result, self.get_cur_player().get_type())
            elif result == 0:
                msg = 'game {}, draw'.format(self.game_num)
            QtWidgets.QMessageBox.information(self, 'Info', msg)
            if self.is_save_transcript:
                transcript_player.save_transcript(self.get_transcript_save_path(), self.actions)
        else:
            self.toggle_player()
            if not self.is_human_turn():
                self.request_action()

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
        self.stop_action_request()
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
