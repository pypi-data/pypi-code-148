from rocketgym.environment import Environment
import random

env = Environment()
observation = env.reset()
done = False

while not done:
    observation, reward, done, info = env.step(random.randint(0, 3))
    env.render()
