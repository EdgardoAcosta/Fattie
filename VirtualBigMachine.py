from fattie.belly.fluffyvariable import *
import ast

quadruples = list()

def bigMachine():

    print("--->Fattie Rolling<---")

    #funcion que lee los cuadruplos y los guarda
    filepath = "fat.txt"
    with open(filepath) as fp:
        line = fp.readline()
        count = 1
        while line:
            quadruples.append(ast.literal_eval(line))
            line = fp.readline()
            count += 1


if __name__ == '__main__':
    bigMachine()
    for val in quadruples:
        print(val)