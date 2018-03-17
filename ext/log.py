# -*- coding: utf-8 -*-

from Tkinter import *

def log(fileName, it, agents):
    """
    Logs data
    :param agents: List of agents
    :return:
    """
    f = open(fileName, 'w+')

    # TODO : complete log
    f.write(str(it) + ',' + str(agents[0].score) + ',' + str(agents[1].score) + '\n')

    f.close()

if __name__ == '__main__':
    log()