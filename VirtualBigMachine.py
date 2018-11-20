import ast

# stack with the quadruples
quadruples = list()

# definition of the memory
# Memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,const 500000 - 600000
fatMemory = 600000 * [""]

# definition of the globalmemory
# Global memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,const 500000 - 600000
fatGlobalMemory = 600000 * [""]


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


def getValue_FatMemory(position):
    result = fatMemory[position]
    return result


def insertInFatGlobalMemory(position, value):
    fatGlobalMemory[position] = value


def getValue_FatGlobalMemory(position):
    result = fatGlobalMemory[position]
    return result


# just for test porpuses
def printLocalValue(position):
    print("local:{}=>{}".format(position, fatMemory[position]))


def printGlobalValue(position):
    print("global:{}=>{}".format(position, fatGlobalMemory[position]))


def bigMachine():
    init()

    print("--->Fattie Rolling<---")

    # Resolve the quadruples given
    for quadruple in quadruples:

        # assignation of constants
        if quadruple['operator'] == 'CONST':
            l_val = quadruple['l_value']['addr']
            result = quadruple['result']['addr']

            insertInFatMemory(result, l_val)
            printLocalValue(result)

        # asignation of any variable
        elif quadruple['operator'] == 'EQUAL':
            l_val = quadruple['l_value']['addr']
            result = quadruple['result']['addr']

            # verify if is going to assign to a global variable
            if result / 1000000 >= 1:
                result = result - 1000000
                insertInFatGlobalMemory(result, l_val)
                printGlobalValue(result)
            else:
                printLocalValue(result)

        # add of two variables
        elif quadruple['operator'] == 'PLUS':

            l_val = quadruple['l_value']['addr']
            r_val = quadruple['r_value']['addr']
            result = quadruple['result']['addr']

            # verify if is going to stract l_val from a global variable
            if l_val / 1000000 >= 1:
                l_val = l_val - 1000000

                # verify if l_val is indirect o direct reference

                if getValue_FatGlobalMemory(l_val) >= 500000:
                    l_operand = getValue_FatMemory(getValue_FatGlobalMemory(l_val))
                else:
                    l_operand = getValue_FatGlobalMemory(l_val)

            else:
                # verify if l_val is indirect o direct reference
                if getValue_FatMemory(l_val) >= 500000:
                    l_operand = getValue_FatMemory(getValue_FatMemory(l_val))
                else:
                    l_operand = getValue_FatMemory(l_val)

            # verify if is going to stract r_val from a global variable
            if r_val / 1000000 >= 1:
                r_val = r_val - 1000000

                # verify if l_val is indirect o direct reference
                if getValue_FatGlobalMemory(r_val) >= 500000:
                    r_operand = getValue_FatMemory(getValue_FatGlobalMemory(r_val))
                else:
                    r_operand = getValue_FatGlobalMemory(r_val)

            else:
                # verify if l_val is indirect o direct reference
                if getValue_FatMemory(r_val) >= 500000:
                    r_operand = getValue_FatMemory(getValue_FatMemory(r_val))
                else:
                    r_operand = getValue_FatMemory(r_val)

            # verify if si goign to assign to a global variable
            if result / 1000000 >= 1:
                result = result - 1000000
                evaluation = l_operand + r_operand
                insertInFatGlobalMemory(result, evaluation)
                printGlobalValue(result)

            else:
                evaluation = l_operand + r_operand
                insertInFatMemory(result, evaluation)
                printLocalValue(result)

            # #verify if l_val is indirect o direct reference
            # if getValue_FatMemory(l_val) >= 500000:
            #     l_operand = getValue_FatMemory(getValue_FatMemory(l_val))
            # else:
            #     l_operand = getValue_FatMemory(l_val)
            #
            # # verify if l_val is indirect o direct reference
            # if getValue_FatMemory(r_val) >= 500000:
            #     r_operand = getValue_FatMemory(getValue_FatMemory(r_val))
            # else:
            #     r_operand = getValue_FatMemory(r_val)
            #
            # evaluation = l_operand + r_operand
            # insertInFatMemory(result,evaluation)
            # printLocalValue(result)

            # TODO: Checar el UMINUS PORQUE NO SABES QUE PEDO

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
        # elif quadruple['operator'] == 'EQUALS':
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

        elif quadruple['operator'] == 'INPUT':

            result = quadruple['result']
            aux = input("> ")

            # insertInFatMemory(,aux)
            print(result)
            # if result['type']:
            #     pass
        elif quadruple['operator'] == 'PRINT':

            result = quadruple['result']
            if result['addr'] / 1000000 >= 1:
                result = result - 1000000
                aux = getValue_FatGlobalMemory(result)
            else:
                print(result['addr'])
                print(fatMemory[1] is '')
                # print(fatMemory[])
                aux = getValue_FatMemory(result['addr'])

            print(aux)


if __name__ == '__main__':
    bigMachine()
