from input_functions import validate, convert_to_rpn, find_minterms
from Quine_McCluskey import minimize


def main():
    while True:
        print("\nOperators:\n and: &\n or: |\n xor: ^\n not: ~\n implication: >\n equivalence: =\n")
        print("Use: ( x | y ) > ( ~ a ) & b\nor: Me&You > You&(~Him)|(Him^You)\n")
        sentence = input("Input:\n")

        if validate(sentence):
            minterms = []
            rpn, variables = convert_to_rpn(sentence)
            print("\tRPN:\t", rpn)
            print("\tVariables:\t", variables)
            answers = find_minterms(rpn,variables)
            for i in range(len(answers)):
                if answers[i]: minterms.append(i)
            print("\tMinterms: ", minterms)
            minimize(variables, minterms)
        else:
            print("Wrong sentence, try again")

        if input("\nWant to continue? press [y]\nDon't want to continue? press [anything else]\n") == 'y':
            continue
        else:
            return


if __name__ == "__main__":
    main()

