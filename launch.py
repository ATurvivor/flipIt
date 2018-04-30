#!/usr/bin/env python

import sys
from os import getcwd
sys.path.append(getcwd())

from Tkinter import *
from ui.mainWindow import MainWindow

from run import *
from agents.agent import *
from config.properties import *

def launch():
    """
    Run game
    :return:
    """
    setProperties(readProperties('config/test.properties'))
    agent_params=[(1,.005),(1,.01),(2,(.005,.005)),(2,(.0025,.0025)),(0,.005),(0,.01)]

    if globals.gEnvironment:
        root = Tk()
        root.resizable(width=300, height=300)

        main_window = MainWindow(root, agents)
        main_window.pack()

        root.mainloop()

    else:
        if globals.gGrid:
            globals.gScoresGrid=np.zeros([len(agent_params),len(agent_params)])
            print(globals.gScoresGrid)
            for ii in range(len(agent_params)):
                for jj in range(len(agent_params)):
                    print(ii,jj)
                    ij_score=0.0
                    ji_score=0.0
                    i=agent_params[ii]
                    j=agent_params[jj]
                    agent_pair=[Agent(strategy=i[0],strategyParam=i[1]),Agent(strategy=j[0],strategyParam=j[1])]
                    globals.gCurrentOwner = agent_pair[0]
                    run(agent_pair)
                    ij_score+=agent_pair[0].score/(2.0*globals.gLastIteration)
                    ji_score += agent_pair[1].score/(2.0*globals.gLastIteration)
                    setProperties(readProperties('config/test.properties'))
                    globals.gAgentStartId=0
                    agent_pair=[Agent(strategy=j[0],strategyParam=j[1]),Agent(strategy=i[0],strategyParam=i[1])]
                    globals.gCurrentOwner = agent_pair[0]
                    run(agent_pair)
                    ij_score+=agent_pair[1].score/(2.0*globals.gLastIteration)
                    ji_score += agent_pair[0].score/(2.0*globals.gLastIteration)
                    setProperties(readProperties('config/test.properties'))
                    globals.gAgentStartId = 0

                    globals.gScoresGrid[ii, jj] = ij_score
                    globals.gScoresGrid[jj, ii] = ji_score

            print(globals.gScoresGrid)

        else:
            agents = [Agent(strategy=agent_params[idx][0], strategyParam=agent_params[idx][1]) for idx in
                      range(globals.gNbAgents)]
            globals.gCurrentOwner = agents[0]
            run(agents)
            print(agents[1].score)
if __name__ == '__main__':
    launch()