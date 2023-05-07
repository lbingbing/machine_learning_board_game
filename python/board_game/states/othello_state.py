from .blackwhite_state import BlackWhiteState

class OthelloState(BlackWhiteState):
    def __init__(self, size):
        super().__init__((size, size))

        assert size >= 4 and size % 2 == 0

    def reset(self):
        super().reset()
        self.board[self.board_shape[0]//2-1][self.board_shape[1]//2-1] = self.get_player_piece(1)
        self.board[self.board_shape[0]//2-1][self.board_shape[1]//2] = self.get_player_piece(2)
        self.board[self.board_shape[0]//2][self.board_shape[1]//2-1] = self.get_player_piece(2)
        self.board[self.board_shape[0]//2][self.board_shape[1]//2] = self.get_player_piece(1)

    def get_name(self):
        return 'othello_{}_{}'.format(*self.board_shape)

    def get_target_pos(self, i, j, idir, jdir, player_id):
        player_piece = self.get_player_piece(player_id)
        i1 = i + idir
        j1 = j + jdir
        while (idir == 0 or (idir < 0 and i1 > 0) or (idir > 0 and i1 < self.board_shape[0]-1)) and \
              (jdir == 0 or (jdir < 0 and j1 > 0) or (jdir > 0 and j1 < self.board_shape[1]-1)) and \
              self.board[i1][j1] != 0 and self.board[i1][j1] != player_piece:
            i1 += idir
            j1 += jdir
        if (idir == 0 or (idir < 0 and i1 >= 0 and i1 < i-1) or (idir > 0 and i1 <= self.board_shape[0]-1 and i1 > i+1)) and \
           (jdir == 0 or (jdir < 0 and j1 >= 0 and j1 < j-1) or (jdir > 0 and j1 <= self.board_shape[1]-1 and j1 > j+1)) and \
           self.board[i1][j1] == player_piece:
            return i1, j1
        else:
            if idir == 0:
                pos_i = None
            else:
                pos_i = self.board_shape[0] if idir < 0 else -1
            if jdir == 0:
                pos_j = None
            else:
                pos_j = self.board_shape[1] if jdir < 0 else -1
            return pos_i, pos_j

    def get_legal_actions(self, player_id):
        super().get_legal_actions(player_id)
        legal_actions = []
        for i in range(self.board_shape[0]):
            for j in range(self.board_shape[1]):
                if self.board[i][j] == 0:
                    if self.get_target_pos(i, j, -1,  0, player_id)[0] < i-1 or \
                       self.get_target_pos(i, j,  1,  0, player_id)[0] > i+1 or \
                       self.get_target_pos(i, j,  0, -1, player_id)[1] < j-1 or \
                       self.get_target_pos(i, j,  0,  1, player_id)[1] > j+1 or \
                       self.get_target_pos(i, j, -1, -1, player_id)[0] < i-1 or \
                       self.get_target_pos(i, j, -1,  1, player_id)[0] < i-1 or \
                       self.get_target_pos(i, j,  1, -1, player_id)[0] > i+1 or \
                       self.get_target_pos(i, j,  1,  1, player_id)[0] > i+1:
                        legal_actions.append((i, j))
        return legal_actions

    def get_result(self):
        if self.last_action == None:
            return -1
        if self.get_legal_actions(self.cur_player_id):
            return -1
        black_piece = self.get_player_piece(1)
        white_piece = self.get_player_piece(2)
        black_num = sum(1 for row in self.board for p in row if p == black_piece)
        white_num = sum(1 for row in self.board for p in row if p == white_piece)
        if black_num > white_num:
            return 1
        if black_num < white_num:
            return 2
        else:
            return 0

    def change_color(self, i, j, idir, jdir, player_id):
        player_piece = self.get_player_piece(player_id)
        target = self.get_target_pos(i, j, idir, jdir, player_id)
        i1 = target[0] - idir if idir != 0 else i
        j1 = target[1] - jdir if jdir != 0 else j
        while (idir == 0 or (idir < 0 and i1 < i) or (idir > 0 and i1 > i)) and \
              (jdir == 0 or (jdir < 0 and j1 < j) or (jdir > 0 and j1 > j)):
            self.board[i1][j1] = player_piece
            i1 -= idir
            j1 -= jdir

    def do_action(self, player_id, action):
        super().do_action(player_id, action)
        i, j = action
        self.change_color(i, j, -1,  0, player_id)
        self.change_color(i, j,  1,  0, player_id)
        self.change_color(i, j,  0, -1, player_id)
        self.change_color(i, j,  0,  1, player_id)
        self.change_color(i, j, -1, -1, player_id)
        self.change_color(i, j, -1,  1, player_id)
        self.change_color(i, j,  1, -1, player_id)
        self.change_color(i, j,  1,  1, player_id)

def create_state():
    return OthelloState(8)
