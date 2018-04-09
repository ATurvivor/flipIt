#!/usr/bin/env python

global gIteration

# Data
global gLogFileName
global gLogData # boolean

global gDebug

# Agents
global gNbAgents
global gAgentStartId
global gFlipCost
global gFlipReward
global gRandomSeeds

# Game globals
global gEnvironment
global gCurrentTime
global gEndGameProbability # [0,1]
global gEndGame # boolean
global gCurrentOwner
global gGameType
global gTime
global gGameFlips #Game history of player flips, first index agent id
global gGameEnd #Time of game end
global gFlipped #Stores next flip times, only used for continuous game type