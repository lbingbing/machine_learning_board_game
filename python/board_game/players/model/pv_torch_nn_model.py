import numpy as np
import torch

from . import torch_nn_model
from . import pv_model

class PVTorchNNModel(torch_nn_model.TorchNNModel, pv_model.PVModel):
    def get_softmax_temperature(self):
        raise NotImplementedError()

    def train(self, batch, learning_rate, vloss_factor):
        states = []
        actions = []
        target_Vs = []
        factors = []
        for state, action, target_V, factor in batch:
            states.append(state)
            actions.append(action)
            target_Vs.append(target_V)
            factors.append(factor)
        state_m = np.concatenate([state.get_equivalent_state_numpy(state.to_state_numpy()) for state in states], axis=0)
        action_m = np.concatenate([state.get_equivalent_action_numpy(state.action_to_action_numpy(action)).astype(dtype=np.float32) for action in actions], axis=0)
        target_V_m = np.concatenate([np.full((state.get_equivalent_num(), 1), target_V, dtype=np.float32) for target_V in target_Vs], axis=0)
        factor_m = np.concatenate([np.full((state.get_equivalent_num(), 1), factor, dtype=np.float32) for factor in factors], axis=0)
        state_t = torch.tensor(state_m).to(self.device)
        action_t = torch.tensor(action_m).to(self.device)
        target_V_t = torch.tensor(target_V_m).to(self.device)
        factor_t = torch.tensor(factor_m).to(self.device)
        P_logits_t, V_t = self.network(state_t)
        vloss_fn = torch.nn.MSELoss()
        vloss = vloss_fn(V_t, target_V_t) * vloss_factor
        P_t = torch.nn.Softmax(dim=1)(P_logits_t / self.get_softmax_temperature())
        ploss = torch.mean(torch.sum(-factor_t * (action_t * torch.pow(1 - P_t, 2) * torch.log(P_t + 1e-6) + (1 - action_t) * torch.pow(P_t, 2) * torch.log(1 - P_t + 1e-6)), dim=1))
        loss = vloss + ploss
        optimizer = torch.optim.SGD(self.network.parameters(), learning_rate)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        return vloss.item(), ploss.item()

    def get_V(self, state):
        state_m = state.to_state_numpy()
        state_t = torch.tensor(state_m).to(self.device)
        P_logits_t, V_t = self.network(state_t)
        return V_t.item()

    def get_P_logits_t(self, state):
        state_m = state.to_state_numpy()
        state_t = torch.tensor(state_m).to(self.device)
        P_logits_t, V_t = self.network(state_t)
        return P_logits_t

    def get_P_logit_range(self, state):
        P_logits_t = self.get_P_logits_t(state)
        return torch.min(P_logits_t).item(), torch.max(P_logits_t).item()

    def get_P_t(self, state):
        P_logits_t = self.get_P_logits_t(state)
        P_t = torch.nn.Softmax(dim=1)(P_logits_t / self.get_softmax_temperature())
        return P_t

    def get_legal_P_t(self, state):
        P_t = self.get_P_t(state)
        legal_action_mask_m = state.get_legal_action_mask_numpy()
        legal_action_mask_t = torch.tensor(legal_action_mask_m).to(self.device)
        legal_P_t = torch.where(legal_action_mask_t, P_t, 0)
        legal_P_t /= torch.sum(legal_P_t)
        return legal_P_t

    def get_P_range(self, state):
        legal_P_t = self.get_legal_P_t(state)
        return torch.min(legal_P_t).item(), torch.max(legal_P_t).item()

    def get_action(self, state):
        legal_P_m = self.get_legal_P_t(state).cpu().detach().numpy().reshape(-1)
        action_index = np.random.choice(state.get_action_dim(), p=legal_P_m)
        action = state.action_index_to_action(action_index)
        return action
