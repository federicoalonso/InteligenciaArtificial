from DiceGameEnv import DiceGame
from collections import defaultdict

class Policy():
    def __init__(self) :
        self.state = ['in', 'end']
        self.actions = []
        self.DiceGame = DiceGame()

    def action(self, state):
        if state == 'in':
            return 'stay'
        else:
            return 'quit'
        
    def estados_posibles(self, state, action):
        if state == 'in':
            if action == 'stay':
                return ['in', 'end']
            else:
                return ['end']
        else:
            return []
    
    def get_probability(self, state_1, action, state_2):
        return self.DiceGame.P[state_1][action][state_2]
        #      self.DiceGame.P['in'][policy.type]['in']

    def get_reward(self, state_1, action, state_2):
        return self.DiceGame.R[state_1][action][state_2]

class PolicyEvaluation():

    def pol_eval(self, pi: Policy):
        # aca va truqito, el defaultdict, en caso de no conocer la llave, siempre retorno lo que le pases
        # en este caso value[chorizo] = 0
        value = defaultdict(lambda: 0)
        #value = 0
        # ahora en vez de hacer el while entre value y prev_value, necesitamos conocer la diferencia mas grande que hubo para todos los estados
        max_diff = 1
        while(max_diff > 0.05):
            prev_value = value
            #qures que value empiece en 0, porque va a valer la suma de los siguientes estados, que ahora son mas de uno
            #value = defaultdict(self.def_value)
            value = defaultdict(lambda: 0)
            #value = 0
            # para cada estado
            for s in pi.state: 
                # le pedimos la accion a la policy
                a = pi.action(s) 
                # para cada estado que podemos llegar desde s con la accion a
                for s_2 in pi.estados_posibles(s, a): 
                # lo mismo que pusiste vos, pero ahora le sumamos todos los estados posibles a los que llegamos
                    
                    value[s] += pi.get_probability(s, a, s_2) * (pi.get_reward(s, a, s_2) + prev_value[s_2]) # prev_value[s_2])

                    ##### Esto o los P y R deben estar en las politica, o en un juego que se debe recibir por parametro???????
            max_diff = value['in'] - prev_value['in']
        for i in value:
            print(f"El valor de la policy {i} es {value[i]}.")
        return value['in']

    def def_value(self, args):
        return 0

    def pol_eval_sin_env(self, policy: Policy):
        value = 0
        if(policy.type == 'stay'):
            prev_val = -1
            while(value - prev_val > 0.1):
                prev_val = value
                value = self.DiceGame.P['in'][policy.type]['in'] * (self.DiceGame.R['in'][policy.type]['in'] + value)
            value += 4
        else:
            value = self.DiceGame.P['in'][policy.type]['end'] * (self.DiceGame.R['in'][policy.type]['end'] + value)
        return value
