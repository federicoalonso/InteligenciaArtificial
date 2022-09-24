from PolicyEval import Policy, PolicyEvaluation
import traceback


def main():
    print('Iniciando')
    try:
        policyWalk = Policy()
        PE = PolicyEvaluation()
        policyWalk.defautlAction = 'walk'
        val = PE.pol_eval(policyWalk)

        print(f"El valor de la policy walk es {val}.")

        policyTranvia = Policy()
        policyTranvia.defautlAction = 'tranvia'
        val = PE.pol_eval(policyTranvia)

        print(f"El valor de la policy tranvia es {val}.")
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())

if __name__ == "__main__":
    main()