from agents.agent import *
from run import *
from config.properties import *

import matplotlib.pyplot as plt

debug = False

def plot_results():
    """

    :return:
    """

    # PARAMETERS

    strategies = {(0,0) : 'Periodic', (1,0) : 'Uniform', (2,1) : 'Delayed Uniform (0.0025)', (2,2) : 'Delayed Uniform (0.005)',\
                  (3,0) : 'Exponential', (4,1) : 'Delayed Exponential (0.0025)', (4,2) : 'Delayed Exponential (0.005)'}
    move_rate = [mr/2000 for mr in range(1, 100)]
    delays = [0.0025, 0.005]
    nb_simulations = 10

    final_scores = {0 : {}, 1 : {}}

    # for each strategy
    for st, delay in strategies:
        strategy_score = {}
        if debug:
            print('Testing Agent 0 (Periodic) vs. Agent 1 (' + str(strategies[(st, delay)]) + ')')

        for param1 in move_rate:
            param2 = param1

            if debug:
                print('\t- Move Rate : ' + str(param2))

            if delay: # delayed strategies, add delay parameter
                param2 = (param2,delays[delay-1])
                if debug:
                    print('\t  Delay : ' + str(param2[1]))

            average_scores = {0 : 0, 1 : 0}

            # run simulation
            for _ in range(nb_simulations):
                setProperties(readProperties('../config/parameters/exp.properties'))
                agents = [Agent(strategy=0, strategyParam=param1), Agent(strategy=st, strategyParam=param2)]
                agents[0].setAgentId(0)
                agents[1].setAgentId(1)

                if debug:
                    print('\t  Simulation ' + str(_))
                new_scores = run(agents)


                # add scores
                for idx, score in new_scores.items():
                    average_scores[idx] += score


            if debug:
                print()

            # after simulations, get average
            for idx in average_scores.keys():
                if idx not in strategy_score:
                    strategy_score[idx] = [average_scores[idx]/nb_simulations]
                else:
                    strategy_score[idx] += [average_scores[idx]/nb_simulations]

        for idx in strategy_score:
            final_scores[idx][strategies[(st, delay)]] = strategy_score[idx]

    for agent in final_scores:
        print('Agent ' + str(agent) + ' score :')
        for st, average_scores in final_scores[agent].items():
            print('\t\t ' + str(st) + ' : ' + str(average_scores))
    print()

    plt.subplot(331)
    plt.plot(move_rate, final_scores[0]['Periodic'], 'blue')
    plt.plot(move_rate, final_scores[1]['Periodic'], 'orange')
    plt.xlabel('Move Rate')
    plt.ylabel('Scores')
    plt.title('Periodic vs. Periodic')

    plt.subplot(334)
    plt.plot(move_rate, final_scores[0]['Uniform'], 'blue')
    plt.plot(move_rate, final_scores[1]['Uniform'], 'orange')
    plt.xlabel('Move Rate')
    plt.ylabel('Scores')
    plt.title('Periodic vs. Uniform')

    plt.subplot(335)
    plt.plot(move_rate, final_scores[0]['Delayed Uniform (0.0025)'], 'blue')
    plt.plot(move_rate, final_scores[1]['Delayed Uniform (0.0025)'], 'orange')
    plt.xlabel('Move Rate')
    plt.ylabel('Scores')
    plt.title('Periodic vs. Delayed Uniform (0.0025)')

    plt.subplot(336)
    plt.plot(move_rate, final_scores[0]['Delayed Uniform (0.005)'], 'blue')
    plt.plot(move_rate, final_scores[1]['Delayed Uniform (0.005)'], 'orange')
    plt.xlabel('Move Rate')
    plt.ylabel('Scores')
    plt.title('Periodic vs. Delayed Uniform (0.005)')

    plt.subplot(337)
    plt.plot(move_rate, final_scores[0]['Exponential'], 'blue')
    plt.plot(move_rate, final_scores[1]['Exponential'], 'orange')
    plt.xlabel('Move Rate')
    plt.ylabel('Scores')
    plt.title('Periodic vs. Exponential')

    plt.subplot(338)
    plt.plot(move_rate, final_scores[0]['Delayed Exponential (0.0025)'], 'blue')
    plt.plot(move_rate, final_scores[1]['Delayed Exponential (0.0025)'], 'orange')
    plt.xlabel('Move Rate')
    plt.ylabel('Scores')
    plt.title('Periodic vs. Delayed Exponential (0.0025)')

    plt.subplot(339)
    plt.plot(move_rate, final_scores[0]['Delayed Exponential (0.005)'], 'blue')
    plt.plot(move_rate, final_scores[1]['Delayed Exponential (0.005)'], 'orange')
    plt.xlabel('Move Rate')
    plt.ylabel('Scores')
    plt.title('Periodic vs. Delayed Exponential (0.005)')

    plt.show()


if __name__ == '__main__':
    plot_results()