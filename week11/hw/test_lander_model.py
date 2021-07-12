import sys, math
import numpy as np

import Box2D
from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)
# new line
import gym
from gym import spaces
from gym.utils import seeding
import skvideo.io
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from collections import deque
from keras.activations import relu, linear
from keras.losses import mean_squared_error
from keras.optimizers import Adam
import random
import sys, getopt


#class DQN:

if __name__=="__main__":

    print("Starting Testing of the trained model...")

    # Run 100 episodes to generate the initial training data
    num_test_episode = 100

    # number of test runs with a satisfactory number of good landings
    high_score = 0

    # Create the OpenAI Gym Enironment with LunarLander-v2
    env = gym.make("LunarLander-v2")
    rewards_list = []

    model = load_model("mymodel.h5")
    done = False
    frames = []

    # Run some test episodes to see how well our model performs
    for test_episode in range(num_test_episode):
        current_state = env.reset()
        num_observation_space = env.observation_space.shape[0]
        current_state = np.reshape(current_state, [1, num_observation_space])
        reward_for_episode = 0
        done = False
        while not done:

            if test_episode % 50 == 0:
                frame = env.render(mode='rgb_array')
                frames.append(frame)

            selected_action = np.argmax(model.predict(current_state)[0])
            new_state, reward, done, info = env.step(selected_action)
            new_state = np.reshape(new_state, [1, num_observation_space])
            current_state = new_state
            reward_for_episode += reward
        rewards_list.append(reward_for_episode)
        print(test_episode, "\t: Episode || Reward: ", reward_for_episode)
        if reward_for_episode >= 200:
            high_score += 1
        if test_episode % 50 == 0:
            fname = "/tmp/videos/testing_run"+str(test_episode)+".mp4"
            skvideo.io.vwrite(fname, np.array(frames))
            del frames
            frames = []

    rewards_mean = np.mean(rewards_list[-100:])
    print("Average Reward: ", rewards_mean )
    print("Total tests above 200: ", high_score)
    
    
