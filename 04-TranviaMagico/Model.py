from TranviaMagicoEnv import TranviaMagico
from collections import defaultdict

class Model():
    def __init__(self) :
        self.state = ['s1', 's2', 's3', 's4']
        self.TMGame = TranviaMagico()
        self.defautlAction = ''
        self.actions = defaultdict(lambda: self.defautlAction)
        self.initialState = 's1'

    def action(self, state):
        return self.actions[state]
        
    def estados_posibles(self, state, action):
        if state == 's1':
            if action == 'walk':
                return ['s2']
            else:
                return ['s1', 's2']
        elif state == 's2':
            if action == 'walk':
                return ['s3']
            else:
                return ['s4', 's2']
        elif state == 's3':
            if action == 'walk':
                return ['s4']
            else:
                return ['s4', 's3']
        else:
            return []
    
    def get_probability(self, state_1, action, state_2):
        return self.TMGame.P[state_1][action][state_2]

    def get_reward(self, state_1, action, state_2):
        return self.TMGame.R[state_1][action][state_2]