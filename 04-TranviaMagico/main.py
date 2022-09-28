from PolicyEval import Policy, PolicyEvaluation
from Model import Model
import traceback


def main():
    print('Iniciando')
    try:
        model = Model()
        model.defautlAction = 'walk'
        policyWalk = Policy(model)
        PE = PolicyEvaluation()
        val = PE.pol_eval(policyWalk)

        print(f"El valor de la policy walk es {val}.")

        model = Model()
        model.defautlAction = 'tranvia'
        policyTranvia = Policy(model)
        val = PE.pol_eval(policyTranvia)

        print(f"El valor de la policy tranvia es {val}.")

        model = Model()
        model.defautlAction = 'walk'
        model.actions['s1'] = 'tranvia'
        policyWT1 = Policy(model)
        val = PE.pol_eval(policyWT1)

        print(f"El valor de la policy tranvia es {val}.")

        model = Model()
        model.defautlAction = 'walk'
        model.actions['s2'] = 'tranvia'
        policyWT2 = Policy(model)
        val = PE.pol_eval(policyWT2)

        print(f"El valor de la policy tranvia es {val}.")
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())

if __name__ == "__main__":
    main()