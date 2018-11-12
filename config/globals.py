#!/usr/bin/env python

# Data
global gLogFileName
global gLogData # boolean

global gDebug

# Game globals
global gIteration
global gEnvironment
global gInteractive
global gCurrentOwnerId
global gCurrentOwner

# Agents
global gAgentStartId
global gNbAgents
global gFlipCost
global gFlipReward
global gRandomSeeds

# Variations of the Game
global gFiniteTime
global gContinuous

global gEndGameProbability # [0,1]
global gEndGame # boolean
global gGameLength # length of game, discrete mode
global gLastIteration # last iteration
global gPrec # precision

global gGameFlips #Game history of player flips, first index agent id
global gFlipped #Stores next flip times, only used for continuous game type