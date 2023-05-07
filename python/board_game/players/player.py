HUMAN_PLAYER         = 'human'
TRANSCRIPT_PLAYER    = 'transcript'
RANDOM_PLAYER        = 'random'
MCTS_PLAYER          = 'mcts'
GMCC_TABLE_PLAYER    = 'gmcc_table'
GMCC_TORCH_NN_PLAYER = 'gmcc_torch_nn'

PLAYER_TYPES = [
    HUMAN_PLAYER,
    TRANSCRIPT_PLAYER,
    RANDOM_PLAYER,
    MCTS_PLAYER,
    GMCC_TABLE_PLAYER,
    GMCC_TORCH_NN_PLAYER,
    ]

class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    def get_type(self):
        raise NotImplementedError()

    def get_player_id(self):
        return self.player_id

    def get_action(self, state):
        assert state.get_cur_player_id() == self.player_id

def is_human(player):
    return player.get_type() == HUMAN_PLAYER

def add_player_options(parser):
    parser.add_argument('player_type1', choices=PLAYER_TYPES, help='player1 type')
    parser.add_argument('player_type2', choices=PLAYER_TYPES, help='player2 type')
