from AI.ReinforcedLearning import DeepQNetwork
from game.blackjack import *
import numpy as np
import matplotlib.pyplot as plt




def run_game(env, RL):
    winRate = np.array([])
    step = 0
    for episode in range(10000):
        # initial observation
        try:
            observation = env.new_round()
        except DeckEmptyError:
            winRate = np.append(winRate, env.shuffle())
            observation = env.new_round()

        while True:

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            try:
                observation_, reward, done = env.step(action)
            except DeckEmptyError:
                winRate = np.append(winRate, env.shuffle())
                break
            RL.store_transition(observation, action, reward, observation_)
            if (step > 1000 and (step % 5 == 0)):
                #print(step)
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

    # end of game
    print('game over')
    return winRate


if __name__ == "__main__":
    # maze game
    env = Game()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=2000,
                      memory_size=100000,
                      #output_graph=True
                      )
    winRate = run_game(env, RL)
    # RL.plot_cost()
    print(winRate)
    print(np.mean(winRate[-500:]))
    plt.plot(winRate)
    plt.show()
