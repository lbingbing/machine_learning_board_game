import argparse
import sys
import time
import threading
import socket
import struct
import pickle

from PySide6 import QtCore, QtGui, QtWidgets

from ..players import player

class GameMonitorWidget(QtWidgets.QWidget):
    def __init__(self, port):
        super().__init__()

        self.port = port
        self.state = self.create_state()

        self.unit_size = self.get_unit_size()
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFixedSize(self.unit_size * (self.state.get_board_shape()[1] + 1), self.unit_size * (self.state.get_board_shape()[0] + 1))

        self.init_get_state_worker()

        self.game_num = 0

        self.start()

    def create_state(self):
        raise NotImplementedError()

    def get_unit_size(self):
        raise NotImplementedError()

    def init_get_state_worker(self):
        self.state_polling_interval = 0.1
        self.step_delay = 0.5

        self.get_state_worker_running = True
        self.get_state_worker_cur_episode = []
        self.get_state_worker_cur_episode_end = False
        self.get_state_worker_next_episode = []
        self.get_state_worker_lock = threading.Lock()
        self.get_state_worker_thread = threading.Thread(target=self.get_state_worker)
        self.get_state_worker_thread.start()

        self.poll_state_timer = QtCore.QTimer(self)
        self.poll_state_timer.setInterval(self.state_polling_interval * 1000)
        self.poll_state_timer.setSingleShot(True)
        self.poll_state_timer.timeout.connect(self.poll_state)

    def get_state_worker(self):
        while True:
            with self.get_state_worker_lock:
                if not self.get_state_worker_running:
                    break
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('127.0.0.1', self.port))
                    print('monitor connected')
                    while True:
                        with self.get_state_worker_lock:
                            if not self.get_state_worker_running:
                                break
                        len_bytes = bytearray()
                        while len(len_bytes) < 8:
                            b = s.recv(8 - len(len_bytes))
                            if not b:
                                raise Exception('recv fails')
                            len_bytes += b
                        state_pickle_byte_len = struct.unpack('<Q', len_bytes)[0]
                        state_pickle_bytes = bytearray()
                        while len(state_pickle_bytes) < state_pickle_byte_len:
                            b = s.recv(state_pickle_byte_len - len(state_pickle_bytes))
                            if not b:
                                raise Exception('recv fails')
                            state_pickle_bytes += b
                        state = pickle.loads(state_pickle_bytes)
                        with self.get_state_worker_lock:
                            if self.get_state_worker_cur_episode_end:
                                self.get_state_worker_next_episode.append(state)
                                if state.is_end():
                                    self.get_state_worker_next_episode.clear()
                            else:
                                self.get_state_worker_cur_episode.append(state)
                                if state.is_end():
                                    self.get_state_worker_cur_episode_end = True
            except Exception as e:
                print('monitor disconnected')
            with self.get_state_worker_lock:
                self.get_state_worker_cur_episode = []
                self.get_state_worker_cur_episode_end = False
                self.get_state_worker_next_episode = []
            time.sleep(1)

    def stop_get_state_worker(self):
        with self.get_state_worker_lock:
            self.get_state_worker_running = False
        self.get_state_worker_thread.join()

    def stop_state_request(self):
        if self.poll_state_timer.isActive():
            self.poll_state_timer.stop()

    def start(self):
        self.reset_marker()
        self.update()
        self.request_state()

    def request_state(self):
        self.poll_state_timer.start()

    def poll_state(self):
        self.get_state_worker_lock.acquire()
        if self.get_state_worker_cur_episode:
            self.state = self.get_state_worker_cur_episode.pop(0)
            if self.state.is_end():
                assert not self.get_state_worker_cur_episode
                self.get_state_worker_cur_episode, self.get_state_worker_next_episode = self.get_state_worker_next_episode, self.get_state_worker_cur_episode
                self.get_state_worker_cur_episode_end = False
            self.get_state_worker_lock.release()
            last_action = self.state.get_last_action()
            if last_action is None:
                self.reset_marker()
            else:
                self.set_marker(last_action)
            time.sleep(self.step_delay)
            self.update_state()
        else:
            self.get_state_worker_lock.release()
            self.poll_state_timer.start()

    def update_state(self):
        self.update()
        result = self.state.get_result()
        if result >= 0:
            self.game_num += 1
            if result > 0:
                msg = 'game {}, player {} wins, action num: {}'.format(self.game_num, result, self.state.get_action_num())
            elif result == 0:
                msg = 'game {}, draw, action num: {}'.format(self.game_num, self.state.get_action_num())
            print(msg)
        self.request_state()

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

    def closeEvent(self, event):
        self.stop_state_request()
        self.stop_get_state_worker()

def main(Widget):
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, help='port')
    args = parser.parse_args()

    app = QtWidgets.QApplication([])
    widget = Widget(args.port)
    widget.show()
    sys.exit(app.exec())
