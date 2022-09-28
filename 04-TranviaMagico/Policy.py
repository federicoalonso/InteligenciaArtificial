from Model import Model

class Policy():
    def __init__(self, model: Model) :
        self.state = model.state
        self.Model = model
        self.actions = model.actions
        self.initialState = model.initialState

    def action(self, state):
        return self.actions[state]
        
    def estados_posibles(self, state, action):
        return self.Model.estados_posibles(state, action)
    
    def get_probability(self, state_1, action, state_2):
        return self.Model.get_probability(state_1, action, state_2)

    def get_reward(self, state_1, action, state_2):
        return self.Model.get_reward(state_1, action, state_2)