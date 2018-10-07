from agents.agent import Agent
from collections import deque

from keras.models import Sequential
from keras.layers import Dense

#import tensorflow as tf

class DQNAgent(Agent):
    def __init__(self, stateSize, actionSize=2):
        self. stateSize = stateSize
        self.actionSize = actionSize
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95 # discount rate

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim = self.stateSize, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.actionSize, activation='linear'))
        #model.compile(loss=)