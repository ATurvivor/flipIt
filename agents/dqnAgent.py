import torch
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random
from collections import deque, namedtuple
from env.model import DQN
from agents.agent import Agent

BUFFER_SIZE = 5000
BATCH_SIZE = 16
GAMMA = 1            # discount factor
TAU = 1e-3              # for soft update of target parameters
LR = 1e-4               # learning rate
UPDATE_EVERY = 10        # how often to update the network

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

class dqnAgent(Agent):
    def __init__(self, state_size, action_size, seed):
        super().__init__(strategy=-1, type='LM')
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)

        # deep q-network
        self.dqn_local = DQN(state_size, action_size, seed).to(device)
        self.dqn_target = DQN(state_size, action_size, seed).to(device)
        self.optimizer = optim.Adam(self.dqn_local.parameters(), lr=LR)

        # replay memory
        self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)
        # Initialize time step (for updating every UPDATE_EVERY steps)
        self.t_step = 0

    def step(self, state, action, reward, next_state, done):
        # Save experience in replay memory
        self.memory.add(state, action, reward, next_state, done)

        # Learn every UPDATE_EVERY time steps.
        self.t_step = (self.t_step + 1) % UPDATE_EVERY
        if self.t_step == 0:
            # If enough samples are available in memory, get random subset and learn
            if len(self.memory) > BATCH_SIZE:
                experiences = self.memory.sample()
                self.learn(experiences, GAMMA)

    def act(self, state, eps=0.):
        """
        Returns actions for given state as per current policy.
        :param state: current state
        :param eps: current epsilon value
        :return:
        """
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        self.dqn_local.eval()
        with torch.no_grad():
            action_values = self.dqn_local(state)
        self.dqn_local.train()

        # epsilon-greedy action selection
        if random.random() > eps:
            return np.argmax(action_values.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_size))

    def learn(self, experiences, gamma):
        """
        Update value parameters using given batch of experience tuples.
        :param experiences: n-tuple
        :param gamma: discount factor
        :return:
        """
        states, actions, rewards, next_states, dones = experiences

        # get max predicted Q values (for next states) from target model
        Q_targets_next = self.dqn_target(next_states).detach().max(1)[0].unsqueeze(1)
        # Compute Q targets for current states
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))

        # get expected Q values from local model
        Q_expected = self.dqn_local(states).gather(1, actions)

        # compute loss
        loss = F.mse_loss(Q_expected, Q_targets)

        # minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # update target network
        self.soft_update(self.dqn_local, self.dqn_target, TAU)

    def soft_update(self, local_model, target_model, tau):
        """
        Sofr update model parameters.
        :param local_model: weights will be copied from
        :param target_model: weights will be copied to
        :param tau: interpolation parameter
        :return:
        """
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau * local_param.data + (1.0 - tau) * target_param.data)


class ReplayBuffer:
    def __init__(self, action_size, buffer_size, batch_size, seed):
        """
        Initialize a fixed sided replay buffer object
        :param action_size:
        :param buffer_size:
        :param batch_size:
        :param seed:
        """
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(seed)

    def add(self, state, action, reward, next_state, done):
        """
        Add a new experience to memory.
        :param state: 
        :param action: 
        :param reward: 
        :param next_state: 
        :param done: 
        :return: 
        """
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)

    def sample(self):
        """
        Randomly sample a batch of experiences from memory.
        :return: 
        """
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)

        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """
        Return the current size of internal memory.
        :return: 
        """
        return len(self.memory)
