from urllib.request import AbstractDigestAuthHandler
from DiceGameEnv import DiceGame
import gym

class Policy(gym.Env):
    def __init__(self) :
        self.type = ['stay', 'quit']

def pol_eval(pi):
    v = 0
    dg = DiceGame
    dg.reset()
    for i in range(len(pi)):
        state, reward, done = dg.step(pi[i])
        if(done):
            i = len(pi)
        else:
            v += reward
    return v

def pol_eval_sin_env(policy):
    if(policy.type == 'stay'):
        return True
    else:
        return True
