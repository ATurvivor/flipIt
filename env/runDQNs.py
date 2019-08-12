# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 04:45:00 2019

@author: admin
"""

import sys
from os import getcwd

#sys.path.append(getcwd())
sys.path.append('C:/Users/admin/Desktop/Research/LISP Research/FlipIt/flipIt-master/')

import torch
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from gym import Env, spaces
from datetime import datetime

from agents.agent import Agent
from agents.dqnAgent import dqnAgent

from config.properties import readProperties, setProperties
from config import globals

class flipIts(Env):
    """
    Define multiplayer flipIt Environment
    """
    
    def __init__(self):
        self.__version__ = "0.2.0"
        print("Multiplayer FlipIt Environment Version {}".format(self.__version__))
        
        # set general variables defining the enviornment
        self.done = False
        self.currStep = -1
        self.steps = globals.gGameLength
        self.flipCost = globals.gFlipCost
        self.flipReward = globals.gFlipReward
        self.nbrAgents = globals.gNbAgents
        self.agentsType = [-1, -1, -1, -1, 0]
        
        # obs/action space
        low = np.array([0 for idx in range(globals.gNbAgents)])
        high = np.array([self.steps + 1 for idx in range(globals.gNbAgents)])
        self.observation_space = spaces.Box(low, high, dtype=np.int32)
        self.action_space = spaces.Discrete(2)
            # defines what the agent can do, i.e. actions (flip, don't flip)

        self.state_size = self.observation_space.shape[0]
        self.action_size = self.action_space.n
        
        # agents
        idx_id = 0
        self.agents = []
        for i in self.agentsType:
            if i == -1:
                self.agents.append(dqnAgent(action_size=self.action_size, state_size=self.state_size, seed=0))  
                # adaptive agent
            else:
                self.agents.append(Agent(strategy=i, strategyParam=0.05))
                # non-adaptive agent
            self.agents[idx_id].setId(idx_id)
            idx_id = idx_id + 1
         
        self.flips = {idx : [] for idx in range(globals.gNbAgents)} 
    
    def step(self, actions):
        """
        Multiplayer Step in the environment
        :param actions[agent.id]: agent_id's action to take at this step
        :return:
        """
        if self.done:
            raise RuntimeError("End Of the Game")
        
        self.currStep = self.currStep + 1
        
        #print(actions)
        rewards = self._take_actions(actions)
        ob = self._get_state()
        # print(ob)
        # print(globals.gNbAgents)
        
        return ob, rewards, self.done, {}
    
    def _take_actions(self, actions):
        """
        
        """
        flipped = {}
        actionRewards = []
        for agent in self.agents:
            if agent.strategy == -1:
                flipped[agent] = actions[agent.id]
                if flipped[agent]:
                    # print(agent.id)
                    agent.lastFlipTime = self.currStep
                    self.flips[agent.id].append(self.currStep)
            else:
                # print(agent.id)
                globals.gIteration = self.currStep
                agent.flipDecision()
                flipped[agent] = agent.flip
                if agent.flip:
                    agent.lastFlipTime = self.currStep
                    self.flips[agent.id].append(self.currStep)
            
            score = agent.isCurrentOwner() * self.flipReward - flipped[agent] * self.flipCost
            agent.score += score
            if agent.strategy == -1:
                actionRewards.append(score)
                
        if any(flipped.values()):
            flippedAgents = [agent for agent in flipped.keys() if flipped[agent]]
            
            for agent in flippedAgents:
                globals.gGameFlips[agent.id].append(self.currStep)
                
            for agent in flippedAgents:
                agent.updateKnowledge()
                
            flippedAgents[0].setCurrentOwner()
            
        if self.currStep >= self.steps:
            self.done = True
            
        return actionRewards
    
    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.
        :return:
        """

        globals.gGameFlips = {idx: [] for idx in range(globals.gNbAgents)}

        self.flips = {idx: [] for idx in range(globals.gNbAgents)}
        
        self.currStep = -1  # reset step counter
        for agent in self.agents:
            agent.reset()
            
        self.agents[0].setCurrentOwner()
        self.done = False  # reset end of game

        return self._get_state()  # get current state of game
    
    def _get_state(self):
        """
        Get observation
        """
        ob = {idx : [] for idx in range(globals.gNbAgents)}
        
        for idx in range(globals.gNbAgents):
            if self.agents[idx].strategy == -1:
                for idx_oppo in range(globals.gNbAgents):
                    """
                    if idx == idx_oppo:
                        if self.agents[idx].lastFlipTime:
                            ob[idx].append(self.currStep - self.agents[idx].lastFlipTime)
                        else:
                            ob[idx].append(self.currStep)
                        continue
                    """
                    opponentFlipTime = self.agents[idx].knowledge[idx_oppo]
                    if opponentFlipTime:
                        ob[idx].append(self.currStep - opponentFlipTime)
                    else:
                        ob[idx].append(self.currStep)
                        
            
        return ob
            
    def train(self, eps_start = 1, eps_end = 0.01, eps_decay = 0.995):
        """
        """
        
        scores= {idx : [] for idx in range(globals.gNbAgents)} 
        av_scores = {idx : [] for idx in range(globals.gNbAgents)} 
        # scores_window = deque(maxlen=100)
        eps = eps_start
        ep = -1
        
        while ep < 5000:
            ep += 1
            state = self.reset()
            for t in range(globals.gGameLength + 1):
                i = 0
                actions = []
                for agent in self.agents:
                    if agent.strategy == -1: 
                        # print('Size of state: ',len(state[i]))
                        actions.append(agent.act(np.array(state[i]), eps)) 
                        i = i + 1
                next_state, rewards, done, _ = self.step(actions)
                i = 0
                for agent in self.agents:
                    if agent.strategy == -1: 
                        agent.step(np.array(state[i]), actions[i], rewards[i], np.array(next_state[i]), done)
                    i = i + 1
                state = next_state
                if done:
                    break
            
            for agent in self.agents:
                scores[agent.id].append(agent.score)
            
            eps = max(eps_end, eps_decay*eps)
            
            if ep % 500 == 0:
                print('\rEpisode {}\tEpsilon: {}'.format(ep, eps))
                for agent in self.agents:
                    av_scores[agent.id].append(np.mean(scores[agent.id][-100:]))
                    if agent.strategy == -1:
                        print('Agent {}, adaptive agent, score = {}'.format(agent.id, av_scores[agent.id][-1]))
                    else:
                        print('Agent {}, non-adaptive agent, score = {}'.format(agent.id, av_scores[agent.id][-1]))
        
        
        for agent in self.agents:
            if agent.strategy == -1:
                torch.save(agent.dqn_local.state_dict(), 'results/checkpoint'+str(agent.id)+'.pth')   
                              
        return scores, av_scores
                            
if __name__  == '__main__':
    setProperties(readProperties('../config/parameters/multiplayer.properties'))
    env = flipIts()
    print('State shape: ', env.state_size)
    print('Number of actions: ', env.action_size)
    print('\n')
                              
    scores, av_scores = env.train()
    
        
        
        
        
        
