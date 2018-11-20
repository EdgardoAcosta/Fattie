from fattie.belly.fluffyvariable import *
import ast

#stack with the quadruples
quadruples = list()

#definition of the memory
fatMemory = list()
fatMemory = 600000 * [""] #Memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,const 500000 - 600000

#definition of temporal memory
temporalMemory = list()
temporalMemory = 6000 * [""] #Temporal memory for variables


def init():

    # funcion que lee los cuadruplos y los guarda
    filepath = "fat.txt"
    with open(filepath) as fp:
        line = fp.readline()
        count = 1
        while line:
            quadruples.append(ast.literal_eval(line))
            line = fp.readline()
            count += 1

def insertInFatMemory(position, value):
    fatMemory[position] = value

def insertInTemporalMemory(position, value):
    temporalMemory[position] = value

#just for test porpuses
def printValue(position):
    print(position)
    print("=>")
    print(fatMemory[position])

def bigMachine():

    init()

    print("--->Fattie Rolling<---")

    #Resolve the quadruples given
    for quadruple in quadruples:
        if quadruple['operator'] == 'CONST':
            l_val = quadruple['l_value']['addr']
            result = quadruple['result']['addr']

            insertInFatMemory(result,l_val)
            printValue(result)

        elif quadruple['operator'] == 'EQUALS':
             l_val = quadruple['l_value']['addr']
             result = quadruple['result']['addr']

             insertInFatMemory(result,l_val)

        # elif quadruple['operator'] == 'PLUS':
        #
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #     print()

        # elif quadruple['operator'] == 'MINUS':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'TIMES':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'DIVIDE':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'LESS':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'GREATER':
        #      l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'NOTEQUAL':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'AND':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'OR':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'NOT':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'TRUE':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'FALSE':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'EQUAL':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'GOTO':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'GOTOF':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'GOSUB':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'UMINUS':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'CONST':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'ERA':
        #      l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'RETURN':
        #    l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'ENPROC':
        #      l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'END':
        #      l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'PARAM':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']
        #
        # elif quadruple['operator'] == 'GETRET':
        #     l_val = quadruple['l_value']['addr']
        #     r_val = quadruple['r_value']['addr']
        #     result = quadruple['result']['addr']




if __name__ == '__main__':
    bigMachine()