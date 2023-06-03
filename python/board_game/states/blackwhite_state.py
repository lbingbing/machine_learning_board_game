import copy

import numpy as np

def piece_value_to_player_id(piece_value):
    if piece_value > 0:
        return 1
    elif piece_value < 0:
        return 2
    else:
        return 0

class BlackWhiteState:
    def __init__(self, board_shape):
        self.board_shape = board_shape
        self.reset()

    def clone(self):
        return copy.deepcopy(self)

    def reset(self):
        self.board = [[0 for j in range(self.board_shape[1])] for i in range(self.board_shape[0])]
        self.cur_player_id = 1
        self.last_action = None
        self.piece_num = 0
        self.action_num = 0

    def get_name(self):
        raise NotImplementedError()

    def get_board_shape(self):
        return self.board_shape

    def get_board(self):
        return self.board

    def get_action_num(self):
        return self.action_num

    def piece_to_char(self, p):
        if p == 1:
            return 'O'
        elif p == -1:
            return 'X'
        else:
            return '-'

    def to_str(self):
        return '\n\n'.join(map(lambda row: '  '.join(map(self.piece_to_char, row)), self.board))

    def to_compact_str(self):
        return ''.join(map(lambda row: ''.join(map(self.piece_to_char, row)), self.board))

    def get_player_piece(self, player_id):
        return 3 - player_id * 2

    def get_cur_player_id(self):
        return self.cur_player_id

    def get_next_player_id(self, player_id):
        return 3 - player_id

    def get_prev_player_id(self, player_id):
        return 3 - player_id

    def get_legal_actions(self, player_id):
        assert player_id == self.cur_player_id

    def is_end(self, result=None):
        if result is None:
            result = self.get_result()
        return result >= 0

    def get_result(self):
        '''
        return result:
            -1 when if game dones't end
            0 when if it is draw
            n when player n wins
        '''
        raise NotImplementedError()

    def do_action(self, player_id, action):
        assert player_id == self.cur_player_id
        assert self.board[action[0]][action[1]] == 0
        self.board[action[0]][action[1]] = self.get_player_piece(self.cur_player_id)
        self.cur_player_id = self.get_next_player_id(self.cur_player_id)
        self.last_action = action
        self.piece_num += 1
        self.action_num += 1

    def swap_players(self):
        for row in self.board:
            for i in range(len(row)):
                row[i] = -row[i]
        self.cur_player_id = self.get_next_player_id(self.cur_player_id)

    def swap_action(self, action):
        return action

    def get_swapped_action_index_table(self):
        return [self.action_to_action_index(self.swap_action(self.action_index_to_action(action_index))) for action_index in range(self.get_action_dim())]

    def get_state_dim(self):
        return 3 ** (self.board_shape[0] * self.board_shape[1])

    def get_state_index(self, board):
        index = 0
        base = 1
        for row in board:
            for piece in row:
                d = piece_value_to_player_id(piece)
                index += d * base
                base *= 3
        return index

    def to_state_index(self):
        return self.get_state_index(self.board)

    def get_state_numpy_shape(self):
        return 1, 1, self.board_shape[0], self.board_shape[1]

    def to_state_numpy(self):
        return np.array(self.board, dtype=np.float32).reshape(1, 1, self.board_shape[0], self.board_shape[1])

    def get_action_dim(self):
        return self.board_shape[0] * self.board_shape[1]

    def action_to_action_index(self, action):
        return action[0] * self.board_shape[1] + action[1]

    def action_index_to_action(self, action_index):
        return action_index // self.board_shape[1], action_index % self.board_shape[1]

    def action_to_action_numpy(self, action):
        action_index = self.action_to_action_index(action)
        action_numpy = np.zeros((self.get_action_dim(),), dtype=bool)
        action_numpy[action_index] = True
        return action_numpy.reshape(1, self.get_action_dim())

    def get_legal_action_indexes(self):
        return [self.action_to_action_index(action) for action in self.get_legal_actions(self.get_cur_player_id())]

    def get_legal_action_mask_numpy(self):
        legal_action_mask_numpy = np.zeros((self.get_action_dim(),), dtype=bool)
        legal_action_indexes = [self.action_to_action_index(action) for action in self.get_legal_actions(self.cur_player_id)]
        legal_action_mask_numpy[legal_action_indexes] = True
        return legal_action_mask_numpy.reshape(1, self.get_action_dim())

    def get_equivalent_num(self):
        return 8

    def get_rot90_board(self, board):
        h = len(board)
        w = len(board[0])
        board1 = [[0 for j in range(h)] for i in range(w)]
        for i in range(w):
            for j in range(h):
                board1[i][j] = board[j][w-1-i]
        return board1

    def get_flip_y_board(self, board):
        h = len(board)
        w = len(board[0])
        board1 = [[0 for j in range(w)] for i in range(h)]
        for i in range(h):
            for j in range(w):
                board1[i][j] = board[h-1-i][j]
        return board1

    def get_equivalent_state_indexes(self, state_index):
        state_index1 = state_index
        board = [[0 for j in range(self.board_shape[1])] for i in range(self.board_shape[0])]
        for i in range(self.board_shape[0]):
            for j in range(self.board_shape[1]):
                board[i][j] = state_index1 % 3
                state_index1 //= 3
        rot1_board = self.get_rot90_board(board)
        rot2_board = self.get_rot90_board(rot1_board)
        rot3_board = self.get_rot90_board(rot2_board)
        flip_y_board = self.get_flip_y_board(board)
        flip_y_rot1_board = self.get_rot90_board(flip_y_board)
        flip_y_rot2_board = self.get_rot90_board(flip_y_rot1_board)
        flip_y_rot3_board = self.get_rot90_board(flip_y_rot2_board)
        return [
            state_index,
            self.get_state_index(rot1_board),
            self.get_state_index(rot2_board),
            self.get_state_index(rot3_board),
            self.get_state_index(flip_y_board),
            self.get_state_index(flip_y_rot1_board),
            self.get_state_index(flip_y_rot2_board),
            self.get_state_index(flip_y_rot3_board),
            ]

    def get_rot90_action(self, action):
        return (self.board_shape[0] - 1 - action[1], action[0])

    def get_flip_y_action(self, action):
        return (self.board_shape[0] - 1 - action[0], action[1])

    def get_equivalent_action_indexes(self, action_index):
        action = self.action_index_to_action(action_index)
        rot1_action = self.get_rot90_action(action)
        rot2_action = self.get_rot90_action(rot1_action)
        rot3_action = self.get_rot90_action(rot2_action)
        flip_y_action = self.get_flip_y_action(action)
        flip_y_rot1_action = self.get_rot90_action(flip_y_action)
        flip_y_rot2_action = self.get_rot90_action(flip_y_rot1_action)
        flip_y_rot3_action = self.get_rot90_action(flip_y_rot2_action)
        return [
            action_index,
            self.action_to_action_index(rot1_action),
            self.action_to_action_index(rot2_action),
            self.action_to_action_index(rot3_action),
            self.action_to_action_index(flip_y_action),
            self.action_to_action_index(flip_y_rot1_action),
            self.action_to_action_index(flip_y_rot2_action),
            self.action_to_action_index(flip_y_rot3_action),
            ]

    def get_equivalent_state_numpy(self, state_numpy):
        state_numpy_flip_y = np.flip(state_numpy, axis=2)
        return np.concatenate(
            [
            state_numpy,
            np.rot90(state_numpy, k=1, axes=(2, 3)),
            np.rot90(state_numpy, k=2, axes=(2, 3)),
            np.rot90(state_numpy, k=3, axes=(2, 3)),
            state_numpy_flip_y,
            np.rot90(state_numpy_flip_y, k=1, axes=(2, 3)),
            np.rot90(state_numpy_flip_y, k=2, axes=(2, 3)),
            np.rot90(state_numpy_flip_y, k=3, axes=(2, 3)),
            ],
            axis=0)

    def get_equivalent_action_numpy(self, action_numpy):
        action_numpy = action_numpy.reshape(action_numpy.shape[0], self.board_shape[0], self.board_shape[1])
        action_numpy_flip_y = np.flip(action_numpy, axis=1)
        return np.concatenate(
            [
            action_numpy,
            np.rot90(action_numpy, k=1, axes=(1, 2)),
            np.rot90(action_numpy, k=2, axes=(1, 2)),
            np.rot90(action_numpy, k=3, axes=(1, 2)),
            action_numpy_flip_y,
            np.rot90(action_numpy_flip_y, k=1, axes=(1, 2)),
            np.rot90(action_numpy_flip_y, k=2, axes=(1, 2)),
            np.rot90(action_numpy_flip_y, k=3, axes=(1, 2)),
            ],
            axis=0).reshape(action_numpy.shape[0]*self.get_equivalent_num(), self.get_action_dim())
