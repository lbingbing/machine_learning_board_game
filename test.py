import os
import platform
import subprocess

os.chdir('machine_learning_board_game_release')

def run(cmd, timeout=None):
    if platform.system() in ('Linux', 'Darwin'):
        os.environ['PATH'] = os.environ.get('PATH', '') + ':.'
    print(' '.join(cmd))
    res = subprocess.run(cmd, timeout=timeout)
    return res.returncode == 0

assert run(['python', '-m', 'board_game.players.model.create_train_flag_file', 'train_stop'])

def test_tictactoe_game_regression():
    assert run(['python', '-m', 'board_game.games.tictactoe_game_regression', 'random', 'random', '100'])

def test_gomoku_game_regression():
    assert run(['python', '-m', 'board_game.games.gomoku_game_regression', 'random', 'random', '100'])

def test_othello_game_regression():
    assert run(['python', '-m', 'board_game.games.othello_game_regression', 'random', 'random', '100'])

def test_cchess_game_regression():
    assert run(['python', '-m', 'board_game.games.cchess_game_regression', 'random', 'random', '100'])

def test_tictactoe_gmcc_table_train():
    assert run(['python', '-m', 'board_game.players.gmcc.tictactoe_gmcc_table_train'])

def test_tictactoe_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.tictactoe_gmcc_torch_nn_train'])

def test_gomoku_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.gomoku_gmcc_torch_nn_train'])

def test_othello_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.othello_gmcc_torch_nn_train'])

def test_cchess_gmcc_torch_nn_train():
    assert run(['python', '-m', 'board_game.players.gmcc.cchess_gmcc_torch_nn_train'])
