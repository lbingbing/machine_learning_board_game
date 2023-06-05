import enum

from ..states import cchess_state
from . import cchess_qt_game_utils
from . import qt_game

@enum.unique
class ActionPhase(enum.Enum):
    SRC = 0
    DST = 1

class CChessWidget(qt_game.GameWidget):
    def create_state(self):
        return cchess_qt_game_utils.create_state()

    def create_player(self, state, player_type, player_id):
        return cchess_qt_game_utils.create_player(state, player_type, player_id)

    def get_unit_size(self):
        return cchess_qt_game_utils.get_unit_size()

    def get_transcript_save_path(self):
        return cchess_qt_game_utils.get_transcript_save_path()

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
        if not self.state.is_end() and self.is_human_turn():
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
        cchess_qt_game_utils.draw_board(self.state, self.unit_size, painter)

    def draw_pieces(self, painter):
        cchess_qt_game_utils.draw_pieces(self.state, self.get_piece_rect, painter)

    def draw_marker(self, painter):
        cchess_qt_game_utils.draw_src_marker(self.src_marker, self.get_piece_rect, painter)
        cchess_qt_game_utils.draw_dst_marker(self.dst_marker, self.get_piece_rect, painter)
        cchess_qt_game_utils.draw_legal_dst_markers(self.legal_dst_markers, self.get_piece_rect, painter)

qt_game.main(CChessWidget)
