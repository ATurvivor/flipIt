# path
import sys
from os import getcwd

sys.path.append(getcwd())

import random
import numpy as np
from agents.agent import Agent
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

class dqnAgent(Agent):
    def __init__(self, action_size, state_size):
        super().__init__(strategy=-1, type='LM')
        self.action_size = action_size
        self.state_size = state_size
        self.memory = deque(maxlen=2000)
        self.gamma = 1  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.002
        self.epsilon_decay = 0.9999
        self.lr = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(32, input_dim=self.state_size, activation='tanh'))
        model.add(Dense(32, activation='tanh'))
        model.add(Dense(self.action_size))
        model.compile(loss='mse', optimizer=Adam(lr=self.lr))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon: # exploration
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        #print(act_values)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)