#!/usr/bin/env python

import numpy as np


def randomStrategy(agent):
    if (np.random.uniform(0,1) < agent.randomSeed):
        agent.flip()
