from DiceGameEnv import DiceGame

class Policy():
    def __init__(self) :
        self.type = 'stay'

class PolicyEvaluation():
    def __init__(self) -> None:
        self.DiceGame = DiceGame()


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

    def pol_eval_sin_env(self, policy: Policy):
        value = 0
        if(policy.type == 'stay'):
            prev_val = -1
            value = 4
            while(value - prev_val > 0.1):
                prev_val = value
                value = self.DiceGame.P['in'][policy.type]['in'] * (self.DiceGame.R['in'][policy.type]['in'] + value)
        else:
            value = self.DiceGame.P['in'][policy.type]['end'] * (self.DiceGame.R['in'][policy.type]['end'] + value)
        return value
