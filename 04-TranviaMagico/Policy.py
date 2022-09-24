from TranviaMagicoEnv import TranviaMagico

class Policy():
    def __init__(self) :
        self.state = ['s1', 's2', 's3', 's4']
        self.actions = []
        self.TMGame = TranviaMagico()
        self.defautlAction = ''
        self.turn = 0
        self.initialState = 's1'

    def action(self):
        if len(self.actions) > self.turn:
            return self.actions[self.turn]
        return self.defautlAction
        
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