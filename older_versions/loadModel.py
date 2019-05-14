from baselines import deepq
from older_versions import flipItEnv
from agents.agent import *
from config.properties import setProperties, readProperties

def run():
    setProperties(readProperties('../config/parameters/dqn.properties'))

    DQNAgent = Agent(strategy=-1, type='LM')
    DQNAgent.setCurrentOwner()
    oppAgent = Agent(strategy=0, strategyParam=0.05)
    agents = [DQNAgent, oppAgent]

    env = flipItEnv(agents)
    act = deepq.learn(env,
                      network='mlp',
                      lr=0.001,
                      total_timesteps=20000,
                      buffer_size=5000,
                      exploration_fraction=0.1,
                      exploration_final_eps=0.002,
                      batch_size=32,
                      print_freq=10,
                      gamma=1,
                      prioritized_replay=True,
                      load_path='models/flipIt_model.pkl')

    while True:
        obs, done = env.reset(), False
        episode_rew = 0
        while not done:
            env.render()
            obs, rew, done, _ = env.step(act(obs[None][0]))
            episode_rew += rew
        print('Episode reward', episode_rew)


if __name__ == '__main__':
    run()