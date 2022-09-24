from PolicyEvalStay import Policy, PolicyEvaluation
import traceback


def main():
    print('Iniciando')
    try:
        policyStay = Policy()
        PE = PolicyEvaluation()
        val = PE.pol_eval(policyStay)

        print(f"El valor de la policy stay es {val}.")

        policyQuit = Policy()
        policyQuit.type = 'quit'
        val = PE.pol_eval_sin_env(policyQuit)

        print(f"El valor de la policy quit es {val}.")
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())

if __name__ == "__main__":
    main()