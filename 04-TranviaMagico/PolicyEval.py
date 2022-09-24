from Policy import Policy
from collections import defaultdict

class PolicyEvaluation():

    def pol_eval(self, pi: Policy):
        # aca va truqito, el defaultdict, en caso de no conocer la llave, siempre retorno lo que le pases
        # en este caso value[chorizo] = 0
        value = defaultdict(lambda: 0)
        #value = 0
        # ahora en vez de hacer el while entre value y prev_value, necesitamos conocer la diferencia mas grande que hubo para todos los estados
        max_diff = 1
        while(abs(max_diff) > 0.05):
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
                    
                    value[s] += pi.get_probability(s, a, s_2) * (pi.get_reward(s, a, s_2) + prev_value[s_2])

                    ##### Esto o los P y R deben estar en las politica, o en un juego que se debe recibir por parametro???????
            max_diff = value[pi.initialState] - prev_value[pi.initialState]
        return value[pi.initialState]
