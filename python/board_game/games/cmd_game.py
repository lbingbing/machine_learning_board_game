import argparse
import itertools

from ..players import player
from ..players.transcript import transcript_player
from . import utils

def main(state, create_player):
    parser = argparse.ArgumentParser('{} cmd game'.format(state.get_name()))
    player.add_player_options(parser)
    utils.add_game_options(parser)
    args = parser.parse_args()

    p1 = create_player(state, args.player_type1, 1)
    p2 = create_player(state, args.player_type2, 2)

    for game_id in itertools.count():
        state.reset()
        print(state.to_str())
        actions = []
        for step_id, p in enumerate(itertools.cycle((p1, p2))):
            print('[{}][{}] {} {} action:'.format(game_id, step_id, p.get_type(), p.get_player_id()), end='', flush=True)
            action = p.get_action(state)
            state.do_action(p.get_player_id(), action)
            actions.append(action)
            if not player.is_human(p):
                print(action)
            print(state.to_str())
            result = state.get_result()
            if result > 0:
                print('player {} wins'.format(result))
            elif result == 0:
                print('draw')
            input('pause')
            if result >= 0:
                if args.save_transcript:
                    transcript_player.save_transcript('{}.{}.trans'.format(state.get_name(), game_id), actions)
                break
