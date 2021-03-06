from . import blackwhite_qt_game_utils
from . import qt_game

class BlackWhiteGameWidget(qt_game.GameWidget):
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

    def handle_human_action(self, x, y):
        if not self.state.is_end() and self.is_human_turn():
            action = self.get_board_position(x, y)
            if action is not None and action in self.state.get_legal_actions(self.get_cur_player().get_player_id()):
                self.apply_action(action)
                self.set_marker(action)
                self.update()
                self.on_action_end()
