import gym
import numpy as np

class TranviaMagico(gym.Env) :
    
    def __init__(self) :
        self.action_space = ['walk', 'tranvia']
        self.observation_space = ['s1', 's2', 's3', 's4']
        self.state = ''
        # Rewards
        self.R = { 's1' : { 'walk' : { 's2' : -1 }, 
                            'tranvia' : {'s2': -2, 's1':-2 } },
                   's2' : { 'walk' : { 's3' : -1 }, 
                            'tranvia' : {'s2': -2, 's4':-2 } },
                   's3' : { 'walk' : { 's4' : -1 }, 
                            'tranvia' : {'s3': -2, 's4':-2 } } }
        # Probabilities
        self.P = { 's1' : { 'walk' : { 's2' : 1 }, 
                            'tranvia' : { 's1' : 1/2, 's2': 1/2 } },
                   's2' : { 'walk' : { 's3' : 1 }, 
                            'tranvia' : { 's2' : 1/2, 's4': 1/2 } },
                   's3' : { 'walk' : { 's4' : 1 }, 
                            'tranvia' : { 's3' : 1/2, 's4': 1/2 } } }

    def reset(self) :
        self.state = 's1'
        return self.state
        
    def step(self, action) :  
        if self.state == 's4' : 
            raise Exception('Llegue')
            
        _state = self.state

        if action == 'walk' : 
            if self.state == 's1' :
                self.state = 's2'
            elif self.state == 's2' :
                self.state = 's3'
            else:
                self.state = 's4'
        else :
            success = np.random.binomial(1, 1/2)
            if success : 
                if self.state == 's1' :
                    self.state = 's2'
                elif self.state == 's2' :
                    self.state = 's4'
                else:
                    self.state = 's4'
        
        done = self.state == 's4'
        
        reward = self.R[_state][action][self.state]
            
        return self.state, reward, done, {}
        
    def render(self, mode = 'human', close = False) :
        if not(close) :
            print('state:', self.state, 'done:', self.state == 's4')

    