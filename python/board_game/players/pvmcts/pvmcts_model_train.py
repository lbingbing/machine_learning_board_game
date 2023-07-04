import argparse
import itertools

from . import pvmcts
from ..utils import train_utils
from ..utils import state_memory
from ..utils import replay_memory
from ..utils import train_flags
from ..utils import train_monitor

def get_default_configs():
    return {
        'episode_num_per_iteration': 1,
        'exploring_starts': [0, 0],
        'state_memory_size': 4096,
        'sim_num': 1000,
        'dirichlet_factor': 0.25,
        'dirichlet_alpha': 0.03,
        'replay_memory_size': 4096,
        'batch_num_per_iteration': 1,
        'batch_size': 32,
        'dynamic_learning_rate': 0.001,
        'vloss_factor': 1,
        }

def sample(state, model, smemory, rmemory, configs, monitor):
    model.set_training(False)

    episode_num_per_iteration = configs['episode_num_per_iteration']
    exploring_starts = configs['exploring_starts']
    sim_num = configs['sim_num']
    dirichlet_factor = configs['dirichlet_factor']
    dirichlet_alpha = configs['dirichlet_alpha']

    smemory.resize(configs['state_memory_size'])
    rmemory.resize(configs['replay_memory_size'])

    scores = [0] * 3
    action_nums = []
    for episode_id in range(episode_num_per_iteration):
        samples = []
        is_exploring_starts, start_state = train_utils.get_exploring_starts(exploring_starts, smemory)
        if is_exploring_starts:
            state = start_state
        else:
            state.reset()
        if monitor:
            monitor.send_state(state.clone())
        cur_player_id = state.get_cur_player_id()
        next_player_id = state.get_next_player_id(cur_player_id)
        pvmcts_tree = pvmcts.PVMctsTree(model, state, cur_player_id, sim_num, is_training=True, dirichlet_factor=dirichlet_factor, dirichlet_alpha=dirichlet_alpha)
        for t, player_id in zip(itertools.count(state.get_action_num()), itertools.cycle((cur_player_id, next_player_id))):
            state1 = state.clone()
            smemory.record(state1)
            action, P = pvmcts_tree.get_action(state, player_id)
            state.do_action(player_id, action)
            samples.append((state1, P))
            if monitor:
                monitor.send_state(state.clone())
            result = state.get_result()
            if state.is_end(result):
                break
        if not is_exploring_starts:
            scores[result] += 1
            action_nums.append(state.get_action_num())
        if result == 1:
            Vs = (1, -1)
        elif result == 2:
            Vs = (-1, 1)
        else:
            Vs = (0, 0)
        for (S, P), V in zip(samples, itertools.cycle(Vs)):
            rmemory.record((S, P, 1, V))
    return scores, action_nums

def train(model, rmemory, configs, iteration_id):
    model.set_training(True)

    batch_num_per_iteration = configs['batch_num_per_iteration']
    batch_size = configs['batch_size']
    learning_rate = train_utils.get_dynamic_learning_rate(iteration_id, configs['dynamic_learning_rate'])
    vloss_factor = configs['vloss_factor']

    plosses = []
    vlosses = []
    for i in range(batch_num_per_iteration):
        batch = rmemory.sample(batch_size)
        ploss, vloss = model.train(batch, learning_rate, vloss_factor)
        plosses.append(ploss)
        vlosses.append(vloss)
    return plosses, vlosses

def main(state, model, configs):
    parser = argparse.ArgumentParser('train {} pvmcts model'.format(state.get_name()))
    train_utils.add_train_arguments(parser)
    args = parser.parse_args()

    train_utils.init_training(model, args.device)

    training_context = train_utils.create_training_context(model.get_model_dir_path(), configs)
    start_iteration_id = training_context['done_iteration_num'] + 1
    configs = training_context['configs']

    smemory = state_memory.StateMemory(configs['state_memory_size'])
    rmemory = replay_memory.ReplayMemory(configs['replay_memory_size'])

    plosses = []
    vlosses = []
    scores = [0, 0, 0]
    action_nums = []

    def check_fn(iteration_id):
        state.reset()
        model.set_training(False)
        V1 = model.get_V(state)
        legal_P_logit_range1 = model.get_legal_P_logit_range(state)
        legal_P_range1 = model.get_legal_P_range(state)
        action = model.get_action(state)
        state.do_action(1, action)
        V2 = model.get_V(state)
        legal_P_logit_range2 = model.get_legal_P_logit_range(state)
        legal_P_range2 = model.get_legal_P_range(state)
        avg_ploss = sum(plosses) / len(plosses)
        avg_vloss = sum(vlosses) / len(vlosses)
        avg_action_num = sum(action_nums) / len(action_nums)
        train_utils.log('{} iter: {} ploss: {:.2f} vloss: {:.2f} Vs: {:.2f} {:.2f} P_logit_ranges: [{:.2f}, {:.2f}] [{:.2f}, {:.2f}] P_ranges: [{:.2f}, {:.2f}] [{:.2f}, {:.2f}] p1/p2/draw: {}/{}/{} action_num: {:.2f}'.format(train_utils.get_current_time_str(), iteration_id, avg_ploss, avg_vloss, V1, V2, *legal_P_logit_range1, *legal_P_logit_range2, *legal_P_range1, *legal_P_range2, scores[1], scores[2], scores[0], avg_action_num))
        plosses.clear()
        vlosses.clear()
        for i in range(len(scores)):
            scores[i] = 0
        action_nums.clear()

    with train_monitor.create_training_monitor(args.monitor_port) as monitor:
        for iteration_id in itertools.count(start_iteration_id):
            if iteration_id % args.check_interval == 1:
                train_flags.check_and_update_train_configs(model.get_model_dir_path(), configs)
            scores1, action_nums1 = sample(state, model, smemory, rmemory, configs, monitor)
            plosses1, vlosses1 = train(model, rmemory, configs, iteration_id)
            plosses += plosses1
            vlosses += vlosses1
            for i, e in enumerate(scores1):
                scores[i] += e
            action_nums += action_nums1
            stop = train_utils.post_iteration(iteration_id, args.iteration_num, args.check_interval, args.save_model_interval, args.checkpoint_interval, model, training_context, check_fn)
            if stop:
                break
