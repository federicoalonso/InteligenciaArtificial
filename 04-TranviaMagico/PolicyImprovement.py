from PolicyEval import Policy, PolicyEvaluation
from collections import defaultdict

class PolicyImprovement():
    def __init__(self) :
        self.Policy = Policy()
        self.Policy.defautlAction = 'walk'

    def policyImprovement(self):
        value = 0
        max_diff = 1
        while(abs(max_diff) > 0.05):
            turn = 0
