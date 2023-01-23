from rocketgym.environment import *

import random

env = Environment()
observation = env.reset()
done = False

while not done:
    observation, reward, done = env.step(random.randint(0, 3))
    env.render()
