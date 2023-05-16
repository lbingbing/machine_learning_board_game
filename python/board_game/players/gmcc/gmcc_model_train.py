import argparse
import random
import itertools

from ..utils import train_utils
from ..utils import replay_memory
from ..utils import train_flags

def sample(state, model, rmemory, configs):
    episode_num_per_iteration = configs['episode_num_per_iteration']
    dynamic_epsilon = configs['dynamic_epsilon']
    discount = configs['discount']

    scores = [0] * 3
    action_nums = []
    for episode_id in range(episode_num_per_iteration):
        samples = []
        state.reset()
        for t, player_id in zip(itertools.count(), itertools.cycle((1, 2))):
            epsilon = train_utils.get_dynamic_epsilon(t, dynamic_epsilon)
            if random.random() > epsilon:
                action = model.get_opt_action(state)
            else:
                legal_actions = state.get_legal_actions(player_id)
                action = random.choice(legal_actions)
            samples.append((state.clone(), action))
            state.do_action(player_id, action)
            result = state.get_result()
            is_end = state.is_end(result)
            if is_end:
                break
        scores[result] += 1
        action_nums.append(state.get_action_num())
        if result > 0:
            Gs = (1, -1)
        else:
            Gs = (0, 0)
        G_discount = 1
        for index, ((S, A), G) in enumerate(zip(reversed(samples), itertools.cycle(Gs))):
            rmemory.record((S, A, G * G_discount))
            if index % 2 == 1:
                G_discount *= discount
    return scores, action_nums

def train(model, rmemory, configs, iteration_id):
    batch_num_per_iteration = configs['batch_num_per_iteration']
    batch_size = configs['batch_size']
    learning_rate = train_utils.get_dynamic_learning_rate(iteration_id, configs['dynamic_learning_rate'])

    losses = []
    for i in range(batch_num_per_iteration):
        batch = rmemory.sample(batch_size)
        loss = model.train(batch, learning_rate)
        losses.append(loss)
    return losses

def main(state, model, configs):
    parser = argparse.ArgumentParser('train {} gmcc model'.format(state.get_name()))
    args = parser.parse_args()

    if not train_flags.check_and_update_train_configs(model.get_model_path(), configs):
        print('train configs:')
        for k, v in configs.items():
            print('{}: {}'.format(k, v))

    check_interval = configs['check_interval']
    save_model_interval = configs['save_model_interval']

    if model.exists():
        model.load()
        print('model {} loaded'.format(model.get_model_path()))
    else:
        model.initialize()
        print('model {} created'.format(model.get_model_path()))
    print('use {} device'.format(model.get_device()))
    model.set_training(True)

    rmemory = replay_memory.ReplayMemory(configs['replay_memory_size'])

    losses = []
    scores = [0, 0, 0]
    action_nums = []
    for iteration_id in itertools.count(1):
        scores1, action_nums1 = sample(state, model, rmemory, configs)
        losses1 = train(model, rmemory, configs, iteration_id)
        losses += losses1
        for i, e in enumerate(scores1):
            scores[i] += e
        action_nums += action_nums1
        need_check = iteration_id % check_interval == 0
        if need_check:
            state.reset()
            max_Q1 = model.get_max_Q(state)
            action = model.get_opt_action(state)
            state.do_action(1, action)
            max_Q2 = model.get_max_Q(state)
            avg_loss = sum(losses) / len(losses)
            avg_action_num = sum(action_nums) / len(action_nums)
            print('{} iteration: {} avg_loss: {:.8f} max_Q1: {:.8f} max_Q2: {:.8f} p1/p2/draw: {}/{}/{} avg_action_num: {}'.format(train_utils.get_current_time_str(), iteration_id, avg_loss, max_Q1, max_Q2, scores[1], scores[2], scores[0], avg_action_num))
            losses.clear()
            scores = [0, 0, 0]
            action_nums.clear()
            train_flags.check_and_update_train_configs(model.get_model_path(), configs)
        if iteration_id % save_model_interval == 0 or (need_check and train_flags.check_and_clear_save_model_flag_file(model.get_model_path())):
            model.save()
            print('model {} saved'.format(model.get_model_path()))
        if need_check and train_flags.check_and_clear_stop_train_flag_file(model.get_model_path()):
            print('stopped')
            break
