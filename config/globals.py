#!/usr/bin/env python

global gIteration

# Data
global gLogFileName
global gLogData # boolean

global gDebug

# Agents
global gAgentStartId
global gNbAgents
global gFlipCost
global gFlipReward
global gRandomSeeds

# Game globals
global gEnvironment
global gInteractive
global gCurrentOwner

global gCurrentTime
global gFiniteTime
global gGameType
global gLastIteration

global gEndGameProbability # [0,1]
global gEndGame # boolean

global gGameEnd #Time of game end
global gGameFlips #Game history of player flips, first index agent id
global gFlipped #Stores next flip times, only used for continuous game type