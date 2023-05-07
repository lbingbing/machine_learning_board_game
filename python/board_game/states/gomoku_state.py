from .blackwhite_state import BlackWhiteState

class GomokuState(BlackWhiteState):
    def __init__(self, size):
        super().__init__((size, size))

        assert size >= 5

        self.target = 5

    def reset(self):
        super().reset()
        self.legal_actions = set((i, j) for i in range(self.board_shape[0]) for j in range(self.board_shape[1]))

    def get_name(self):
        return 'gomoku_{}_{}'.format(*self.board_shape)

    def get_legal_actions(self, player_id):
        super().get_legal_actions(player_id)
        return tuple(self.legal_actions)

    def get_result(self):
        if self.last_action == None:
            return -1
        prev_player_id = self.get_prev_player_id(self.cur_player_id)
        prev_player_piece = self.get_player_piece(prev_player_id)
        # row
        j1 = self.last_action[1]
        while j1-1 >= 0 and self.board[self.last_action[0]][j1-1] == prev_player_piece:
            j1 -= 1
        j2 = self.last_action[1]
        while j2+1 < self.board_shape[1] and self.board[self.last_action[0]][j2+1] == prev_player_piece:
            j2 += 1
        if j2-j1+1 >= self.target:
            return prev_player_id
        # column
        i1 = self.last_action[0]
        while i1-1 >= 0 and self.board[i1-1][self.last_action[1]] == prev_player_piece:
            i1 -= 1
        i2 = self.last_action[0]
        while i2+1 < self.board_shape[0] and self.board[i2+1][self.last_action[1]] == prev_player_piece:
            i2 += 1
        if i2-i1+1 >= self.target:
            return prev_player_id
        # diagonal 1
        i1 = self.last_action[0]
        j1 = self.last_action[1]
        while i1-1 >= 0 and j1-1 >= 0 and self.board[i1-1][j1-1] == prev_player_piece:
            i1 -= 1
            j1 -= 1
        i2 = self.last_action[0]
        j2 = self.last_action[1]
        while i2+1 < self.board_shape[0] and j2+1 < self.board_shape[1] and self.board[i2+1][j2+1] == prev_player_piece:
            i2 += 1
            j2 += 1
        if i2-i1+1 >= self.target:
            return prev_player_id
        # diagonal 2
        i1 = self.last_action[0]
        j1 = self.last_action[1]
        while i1-1 >= 0 and j1+1 < self.board_shape[1] and self.board[i1-1][j1+1] == prev_player_piece:
            i1 -= 1
            j1 += 1
        i2 = self.last_action[0]
        j2 = self.last_action[1]
        while i2+1 < self.board_shape[0] and j2-1 >= 0 and self.board[i2+1][j2-1] == prev_player_piece:
            i2 += 1
            j2 -= 1
        if i2-i1+1 >= self.target:
            return prev_player_id
        # draw or not end yet
        return 0 if self.piece_num == self.board_shape[0] * self.board_shape[1] else -1

    def do_action(self, player_id, action):
        super().do_action(player_id, action)
        self.legal_actions.remove(action)

def create_state():
    return GomokuState(9)
