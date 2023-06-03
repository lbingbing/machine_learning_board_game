import copy

import numpy as np

#    0   1   2   3   4   5   6   7   8
#  0 +---+---+---+---+---+---+---+---+
#    |   |   |   | \ | / |   |   |   |
#  1 +---+---+---+---+---+---+---+---+
#    |   |   |   | / | \ |   |   |   |
#  2 +---x---+---+---+---+---+---x---+
#    |   |   |   |   |   |   |   |   |
#  3 +---+---+---+---+---+---+---+---+
#    |   |   |   |   |   |   |   |   |
#  4 +---+---+---+---+---+---+---+---+
#    |                               |
#  5 +---+---+---+---+---+---+---+---+
#    |   |   |   |   |   |   |   |   |
#  6 +---+---+---+---+---+---+---+---+
#    |   |   |   |   |   |   |   |   |
#  7 +---x---+---+---+---+---+---x---+
#    |   |   |   | \ | / |   |   |   |
#  8 +---+---+---+---+---+---+---+---+
#    |   |   |   | / | \ |   |   |   |
#  9 +---+---+---+---+---+---+---+---+

BOARD_WIDTH = 9
BOARD_HEIGHT = 10

MAX_ACTION_NUM = 200
MAX_NO_KILL_ACTION_NUM = 50

NUL = 0
R_JIANG = 1
R_SHI   = 2
R_XIANG = 3
R_BING  = 4
R_PAO   = 5
R_MA    = 6
R_JU    = 7
B_JIANG = -1
B_SHI   = -2
B_XIANG = -3
B_BING  = -4
B_PAO   = -5
B_MA    = -6
B_JU    = -7

def piece_value_to_player_id(piece_value):
    if piece_value > NUL:
        return 1
    elif piece_value < NUL:
        return 2
    else:
        return 0

def piece_value_to_name(piece_value):
    if True:
        if piece_value == R_JIANG:
            return b'\xe5\xb8\x85'.decode()
        elif piece_value == B_JIANG:
            return b'\xe5\xb0\x86'.decode()
        elif piece_value == R_SHI:
            return b'\xe4\xbb\x95'.decode()
        elif piece_value == B_SHI:
            return b'\xe5\xa3\xab'.decode()
        elif piece_value == R_XIANG:
            return b'\xe7\x9b\xb8'.decode()
        elif piece_value == B_XIANG:
            return b'\xe8\xb1\xa1'.decode()
        elif piece_value == R_BING or piece_value == B_BING:
            return b'\xe5\x85\xb5'.decode()
        elif piece_value == R_PAO:
            return b'\xe7\x82\xae'.decode()
        elif piece_value == B_PAO:
            return b'\xe7\xa0\xb2'.decode()
        elif piece_value == R_MA or piece_value == B_MA:
            return b'\xe9\xa9\xac'.decode()
        elif piece_value == R_JU or piece_value == B_JU:
            return b'\xe8\xbd\xa6'.decode()
        else:
            assert(0)
    else:
        if piece_value == R_JIANG:
            return 'shuai'
        elif piece_value == B_JIANG:
            return 'Jiang'
        elif piece_value == R_SHI or piece_value == B_SHI:
            return 'Shi'
        elif piece_value == R_XIANG or piece_value == B_XIANG:
            return 'Xiang'
        elif piece_value == R_BING or piece_value == B_BING:
            return 'Bing'
        elif piece_value == R_PAO or piece_value == B_PAO:
            return 'Pao'
        elif piece_value == R_MA or piece_value == B_MA:
            return 'Ma'
        elif piece_value == R_JU or piece_value == B_JU:
            return 'Ju'
        else:
            assert(0)

def get_action_and_action_index_mapping():
    action_to_action_index = {}
    index = 0
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            # SHI
            if (i, j) in ((0, 3), (0, 5), (1, 4), (2, 3), (2, 5), (7, 3), (7, 5), (8, 4), (9, 3), (9, 5)):
                if (i <= 2 and i >= 1 or i >= 8) and j >= 4:
                    action_to_action_index[(i, j, i-1, j-1)] = index
                    index += 1
                if (i <= 2 and i >= 1 or i >= 8) and j <= 4:
                    action_to_action_index[(i, j, i-1, j+1)] = index
                    index += 1
                if (i <= 1 or i >= 7 and i <= BOARD_HEIGHT-2) and j >= 4:
                    action_to_action_index[(i, j, i+1, j-1)] = index
                    index += 1
                if (i <= 1 or i >= 7 and i <= BOARD_HEIGHT-2) and j <= 4:
                    action_to_action_index[(i, j, i+1, j+1)] = index
                    index += 1
            # XIANG
            if (i, j) in ((0, 2), (0, 6), (2, 0), (2, 4), (2, 8), (4, 2), (4, 6), (5, 2), (5, 6), (7, 0), (7, 4), (7, 8), (9, 2), (9, 6)):
                if (i <= 4 and i >= 2 or i >= 7) and j >= 2:
                    action_to_action_index[(i, j, i-2, j-2)] = index
                    index += 1
                if (i <= 4 and i >= 2 or i >= 7) and j <= BOARD_WIDTH-3:
                    action_to_action_index[(i, j, i-2, j+2)] = index
                    index += 1
                if (i <= 2 or i >= 5 and i <= BOARD_HEIGHT-3) and j >= 2:
                    action_to_action_index[(i, j, i+2, j-2)] = index
                    index += 1
                if (i <= 2 or i >= 5 and i <= BOARD_HEIGHT-3) and j <= BOARD_WIDTH-3:
                    action_to_action_index[(i, j, i+2, j+2)] = index
                    index += 1
            # MA
            if i >= 2 and j >= 1:
                action_to_action_index[(i, j, i-2, j-1)] = index
                index += 1
            if i >= 2 and j <= BOARD_WIDTH-2:
                action_to_action_index[(i, j, i-2, j+1)] = index
                index += 1
            if i >= 1 and j >= 2:
                action_to_action_index[(i, j, i-1, j-2)] = index
                index += 1
            if i >= 1 and j <= BOARD_WIDTH-3:
                action_to_action_index[(i, j, i-1, j+2)] = index
                index += 1
            if i <= BOARD_HEIGHT-2 and j >= 2:
                action_to_action_index[(i, j, i+1, j-2)] = index
                index += 1
            if i <= BOARD_HEIGHT-2 and j <= BOARD_WIDTH-3:
                action_to_action_index[(i, j, i+1, j+2)] = index
                index += 1
            if i <= BOARD_HEIGHT-3 and j >= 1:
                action_to_action_index[(i, j, i+2, j-1)] = index
                index += 1
            if i <= BOARD_HEIGHT-3 and j <= BOARD_WIDTH-2:
                action_to_action_index[(i, j, i+2, j+1)] = index
                index += 1
            # JU
            for j1 in range(BOARD_WIDTH):
                if j1 != j:
                    action_to_action_index[(i, j, i, j1)] = index
                    index += 1
            for i1 in range(BOARD_HEIGHT):
                if i1 != i:
                    action_to_action_index[(i, j, i1, j)] = index
                    index += 1

    action_index_to_action = {index: action for action, index in action_to_action_index.items()}

    action_index_pairs = []
    for action, action_index in action_to_action_index.items():
        equivalent_action = (action[0], BOARD_WIDTH-1-action[1], action[2], BOARD_WIDTH-1-action[3])
        equivalent_action_index = action_to_action_index[equivalent_action]
        action_index_pairs.append((action_index, equivalent_action_index))
    action_index_pairs.sort()
    action_index_to_equivalent_action_index = [equivalent_action_index for action_index, equivalent_action_index in action_index_pairs]

    return action_to_action_index, action_index_to_action, action_index_to_equivalent_action_index

action_to_action_index_table, action_index_to_action_table, action_index_to_equivalent_action_index_table = get_action_and_action_index_mapping()
ACTION_DIM = len(action_to_action_index_table)

def append_legal_action_JIANG(legal_actions, board, i, j, player_id, sign):
    if (player_id == 1 and i >= 8 or player_id == 2 and i >= 1) and board[i-1][j]*sign <= NUL:
        legal_actions.append((i, j, i-1, j))
    if (player_id == 1 and i <= BOARD_HEIGHT-2 or player_id == 2 and i <= 1) and board[i+1][j]*sign <= NUL:
        legal_actions.append((i, j, i+1, j))
    if j >= 4 and board[i][j-1]*sign <= NUL:
        legal_actions.append((i, j, i, j-1))
    if j <= 4 and board[i][j+1]*sign <= NUL:
        legal_actions.append((i, j, i, j+1))
    if player_id == 1:
        i1 = 0
        while i1 <= 2 and board[i1][j] != B_JIANG:
            i1 += 1
        if i1 <= 2:
            i2 = i1+1
            while i2 != i and board[i2][j] == NUL:
                i2 += 1
            if i2 == i:
                legal_actions.append((i, j, i1, j))
    else:
        i1 = BOARD_HEIGHT-1
        while i1 >= 7 and board[i1][j] != R_JIANG:
            i1 -= 1
        if i1 >= 7:
            i2 = i1-1
            while i2 != i and board[i2][j] == NUL:
                i2 -= 1
            if i2 == i:
                legal_actions.append((i, j, i1, j))

def append_legal_action_SHI(legal_actions, board, i, j, player_id, sign):
    if player_id == 1 and i >= 8 or player_id == 2 and i >= 1:
        if j >= 4 and board[i-1][j-1]*sign <= NUL:
            legal_actions.append((i, j, i-1, j-1))
        if j <= 4 and board[i-1][j+1]*sign <= NUL:
            legal_actions.append((i, j, i-1, j+1))
    if player_id == 1 and i <= BOARD_HEIGHT-2 or player_id == 2 and i <= 1:
        if j >= 4 and board[i+1][j-1]*sign <= NUL:
            legal_actions.append((i, j, i+1, j-1))
        if j <= 4 and board[i+1][j+1]*sign <= NUL:
            legal_actions.append((i, j, i+1, j+1))

def append_legal_action_XIANG(legal_actions, board, i, j, player_id, sign):
    if player_id == 1 and i >= 7 or player_id == 2 and i >= 2:
        if j >= 2 and board[i-1][j-1] == NUL and board[i-2][j-2]*sign <= NUL:
            legal_actions.append((i, j, i-2, j-2))
        if j <= BOARD_WIDTH-3 and board[i-1][j+1] == NUL and board[i-2][j+2]*sign <= NUL:
            legal_actions.append((i, j, i-2, j+2))
    if player_id == 1 and i <= BOARD_HEIGHT-3 or player_id == 2 and i <= 2:
        if j >= 2 and board[i+1][j-1] == NUL and board[i+2][j-2]*sign <= NUL:
            legal_actions.append((i, j, i+2, j-2))
        if j <= BOARD_WIDTH-3 and board[i+1][j+1] == NUL and board[i+2][j+2]*sign <= NUL:
            legal_actions.append((i, j, i+2, j+2))

def append_legal_action_BING(legal_actions, board, i, j, player_id, sign):
    if (player_id == 1 and i >= 1 or player_id == 2 and i <= BOARD_HEIGHT-2) and board[i-sign][j]*sign <= NUL:
        legal_actions.append((i, j, i-sign, j))
    if player_id == 1 and i <= 4 or player_id == 2 and i >= 5:
        if j >= 1 and board[i][j-1]*sign <= NUL:
            legal_actions.append((i, j, i, j-1))
        if j <= BOARD_WIDTH-2 and board[i][j+1]*sign <= NUL:
            legal_actions.append((i, j, i, j+1))

def append_legal_action_PAO(legal_actions, board, i, j, sign):
    # up
    i1 = i-1
    while i1 >= 0 and board[i1][j] == NUL:
        legal_actions.append((i, j, i1, j))
        i1 -= 1
    i1 -= 1
    while i1 >= 0 and board[i1][j] == NUL:
        i1 -= 1
    if i1 >= 0 and board[i1][j]*sign <= NUL:
        legal_actions.append((i, j, i1, j))
    # down
    i1 = i+1
    while i1 <= BOARD_HEIGHT-1 and board[i1][j] == NUL:
        legal_actions.append((i, j, i1, j))
        i1 += 1
    i1 += 1
    while i1 <= BOARD_HEIGHT-1 and board[i1][j] == NUL:
        i1 += 1
    if i1 <= BOARD_HEIGHT-1 and board[i1][j]*sign <= NUL:
        legal_actions.append((i, j, i1, j))
    # left
    j1 = j-1
    while j1 >= 0 and board[i][j1] == NUL:
        legal_actions.append((i, j, i, j1))
        j1 -= 1
    j1 -= 1
    while j1 >= 0 and board[i][j1] == NUL:
        j1 -= 1
    if j1 >= 0 and board[i][j1]*sign <= NUL:
        legal_actions.append((i, j, i, j1))
    # right
    j1 = j+1
    while j1 <= BOARD_WIDTH-1 and board[i][j1] == NUL:
        legal_actions.append((i, j, i, j1))
        j1 += 1
    j1 += 1
    while j1 <= BOARD_WIDTH-1 and board[i][j1] == NUL:
        j1 += 1
    if j1 <= BOARD_WIDTH-1 and board[i][j1]*sign <= NUL:
        legal_actions.append((i, j, i, j1))

def append_legal_action_MA(legal_actions, board, i, j, sign):
    if i >= 2 and board[i-1][j] == NUL:
        if j >= 1 and board[i-2][j-1]*sign <= NUL:
            legal_actions.append((i, j, i-2, j-1))
        if j <= BOARD_WIDTH-2 and board[i-2][j+1]*sign <= NUL:
            legal_actions.append((i, j, i-2, j+1))
    if i <= BOARD_HEIGHT-3 and board[i+1][j] == NUL:
        if j >= 1 and board[i+2][j-1]*sign <= NUL:
            legal_actions.append((i, j, i+2, j-1))
        if j <= BOARD_WIDTH-2 and board[i+2][j+1]*sign <= NUL:
            legal_actions.append((i, j, i+2, j+1))
    if j >= 2 and board[i][j-1] == NUL:
        if i >= 1 and board[i-1][j-2]*sign <= NUL:
            legal_actions.append((i, j, i-1, j-2))
        if i <= BOARD_HEIGHT-2 and board[i+1][j-2]*sign <= NUL:
            legal_actions.append((i, j, i+1, j-2))
    if j <= BOARD_WIDTH-3 and board[i][j+1] == NUL:
        if i >= 1 and board[i-1][j+2]*sign <= NUL:
            legal_actions.append((i, j, i-1, j+2))
        if i <= BOARD_HEIGHT-2 and board[i+1][j+2]*sign <= NUL:
            legal_actions.append((i, j, i+1, j+2))

def append_legal_action_JU(legal_actions, board, i, j, sign):
    # up
    i1 = i-1
    while i1 >= 0:
        if board[i1][j]*sign <= NUL:
            legal_actions.append((i, j, i1, j))
        if board[i1][j]*sign != NUL:
            break
        i1 -= 1
    # down
    i1 = i+1
    while i1 <= BOARD_HEIGHT-1:
        if board[i1][j]*sign <= NUL:
            legal_actions.append((i, j, i1, j))
        if board[i1][j]*sign != NUL:
            break
        i1 += 1
    # left
    j1 = j-1
    while j1 >= 0:
        if board[i][j1]*sign <= NUL:
            legal_actions.append((i, j, i, j1))
        if board[i][j1]*sign != NUL:
            break
        j1 -= 1
    # right
    j1 = j+1
    while j1 <= BOARD_WIDTH-1:
        if board[i][j1]*sign <= NUL:
            legal_actions.append((i, j, i, j1))
        if board[i][j1]*sign != NUL:
            break
        j1 += 1

class CChessState:
    def __init__(self):
        self.board_shape = (BOARD_HEIGHT, BOARD_WIDTH)
        self.reset()

    def clone(self):
        return copy.deepcopy(self)

    def reset(self):
        self.board = [
                [B_JU  , B_MA , B_XIANG, B_SHI, B_JIANG, B_SHI, B_XIANG, B_MA , B_JU  ],
                [NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ],
                [NUL   , B_PAO, NUL    , NUL  , NUL    , NUL  , NUL    , B_PAO, NUL   ],
                [B_BING, NUL  , B_BING , NUL  , B_BING , NUL  , B_BING , NUL  , B_BING],
                [NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ],
                [NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ],
                [R_BING, NUL  , R_BING , NUL  , R_BING , NUL  , R_BING , NUL  , R_BING],
                [NUL   , R_PAO, NUL    , NUL  , NUL    , NUL  , NUL    , R_PAO, NUL   ],
                [NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ],
                [R_JU  , R_MA , R_XIANG, R_SHI, R_JIANG, R_SHI, R_XIANG, R_MA , R_JU  ],
            ]
        self.board_history = []
        self.cur_player_id = 1
        self.action_num = 0
        self.no_kill_action_num = 0

    def get_name(self):
        return 'cchess'

    def get_board_shape(self):
        return self.board_shape

    def get_board(self):
        return self.board

    def get_action_num(self):
        return self.action_num

    def picec_to_char(self, v):
        if v == 0:
            return ' -'
        else:
            return '{:+2d}'.format(v)

    def to_str(self):
        return '\n\n'.join(map(lambda row: '  '.join(map(self.picec_to_char, row)), self.board))

    def compact_str(self):
        return ''.join(map(lambda row: ''.join(map(self.picec_to_char, row)), self.board))

    def board_history_compact_str(self):
        return 'h' + ''.join(''.join(map(lambda row: ''.join(map(self.picec_to_char, row)), board)) for board in self.board_history)

    def get_cur_player_id(self):
        return self.cur_player_id

    def get_next_player_id(self, player_id):
        return 3 - player_id

    def get_legal_actions(self, player_id):
        assert player_id == self.cur_player_id
        legal_actions = []
        sign = 3 - self.cur_player_id * 2
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                p = self.board[i][j]
                if p == R_JIANG * sign:
                    append_legal_action_JIANG(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_SHI * sign:
                    append_legal_action_SHI(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_XIANG * sign:
                    append_legal_action_XIANG(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_BING * sign:
                    append_legal_action_BING(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_PAO * sign:
                    append_legal_action_PAO(legal_actions, self.board, i, j, sign)
                elif p == R_MA * sign:
                    append_legal_action_MA(legal_actions, self.board, i, j, sign)
                elif p == R_JU * sign:
                    append_legal_action_JU(legal_actions, self.board, i, j, sign)
        for i0, j0, i1, j1 in legal_actions:
            if self.cur_player_id == 1 and self.board[i1][j1] == B_JIANG or \
               self.cur_player_id == 2 and self.board[i1][j1] == R_JIANG:
                   return [(i0, j0, i1, j1)]

        return legal_actions

    def is_end(self, result=None):
        if result is None:
            result = self.get_result()
        return result >= 0

    def get_result(self):
        '''
        return result:
            -1 when if game doesn't end
            0 when if it is draw
            n when player n wins
        '''
        if self.cur_player_id == 1:
            if not any(self.board[i][j] == R_JIANG for i in (7, 8, 9) for j in (3, 4, 5)):
                return 2
        else:
            if not any(self.board[i][j] == B_JIANG for i in (0, 1, 2) for j in (3, 4, 5)):
                return 1
        if len(self.board_history) == 8 and \
           self.board == self.board_history[0] and \
           self.board_history[0] == self.board_history[4] and \
           self.board_history[1] == self.board_history[5] and \
           self.board_history[2] == self.board_history[6] and \
           self.board_history[3] == self.board_history[7]:
            return 0
        return 0 if (self.no_kill_action_num == MAX_NO_KILL_ACTION_NUM or self.action_num == MAX_ACTION_NUM) else -1

    def do_action(self, player_id, action):
        assert player_id == self.cur_player_id
        assert player_id == 1 and self.board[action[0]][action[1]] > NUL or \
               player_id == 2 and self.board[action[0]][action[1]] < NUL
        assert player_id == 1 and self.board[action[2]][action[3]] <= NUL or \
               player_id == 2 and self.board[action[2]][action[3]] >= NUL
        self.board_history.append(copy.deepcopy(self.board))
        if len(self.board_history) > 8:
            del self.board_history[0]
        if self.board[action[2]][action[3]] != NUL:
            self.no_kill_action_num = 0
        else:
            self.no_kill_action_num += 1
        self.board[action[2]][action[3]] = self.board[action[0]][action[1]]
        self.board[action[0]][action[1]] = NUL
        self.cur_player_id = self.get_next_player_id(self.cur_player_id)
        self.action_num += 1

    def swap_players(self):
        self.swap_board(self.board)
        for board in self.board_history:
            self.swap_board(board)
        self.cur_player_id = self.get_next_player_id(self.cur_player_id)

    def swap_board(self, board):
        for row in board:
            for i in range(len(row)):
                row[i] = -row[i]
        board.reverse()

    def swap_action(self, action):
        return BOARD_HEIGHT - 1 - action[0], action[1], BOARD_HEIGHT - 1 - action[2], action[3]

    def get_swapped_action_index_table(self):
        return [self.action_to_action_index(self.swap_action(self.action_index_to_action(action_index))) for action_index in range(ACTION_DIM)]

    def get_state_numpy_shape(self):
        return 1, 1, BOARD_HEIGHT, BOARD_WIDTH

    def to_state_numpy(self):
        return np.array(self.board, dtype=np.float32).reshape(1, 1, BOARD_HEIGHT, BOARD_WIDTH)

    def get_action_dim(self):
        return ACTION_DIM

    def action_to_action_index(self, action):
        return action_to_action_index_table[action]

    def action_index_to_action(self, action_index):
        return action_index_to_action_table[action_index]

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
        return 2

    def get_equivalent_state_numpy(self, state_numpy):
        state_numpy_flip_x = np.flip(state_numpy, axis=3)
        return np.concatenate(
            [
            state_numpy,
            state_numpy_flip_x,
            ],
            axis=0)

    def get_equivalent_action_numpy(self, action_numpy):
        equivalent_action_numpy = action_numpy.copy()
        equivalent_action_numpy[:,list(range(self.get_action_dim()))] = action_numpy[:,action_index_to_equivalent_action_index_table]
        return np.concatenate(
            [
            action_numpy,
            equivalent_action_numpy,
            ],
            axis=0)

def create_state():
    return CChessState()
