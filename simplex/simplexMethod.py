import re

def simplexMethod(objFunction: list, constraints: list, isMax : bool = True) -> list:
    """  
    Solves the linear programming problem using the Simplex method.

    Parameters:
    @param obj_function (list): The coefficients of the objective function.
    @param constraints (list): A list of constraints, where each constraint is a list containing the coefficients and the right-hand side value.

    Returns:
    list: The solution to the linear programming problem.
    """

    originalNum = len(constraints)
    internalCount = 0
    originalObj = objFunction.copy()
    
    for i in range(originalNum):
        objFunction.append(0)
        for j in range(originalNum):
            if internalCount%(len(constraints)+1) == 0:
                constraints[i][0].append(1)
            else:
                constraints[i][0].append(0)
            internalCount += 1
    result = []
    resultIndex = [-1 for i in range(len(constraints))]
    basis = [0 for i in range(len(constraints))]
    z_j = [sum(basis[j]*constraints[j][0][i] for j in range(len(constraints))) for i in range(len(constraints[0][0]))]

    c_j_minus_z_j = [objFunction[i] - z_j[i] for i in range(len(z_j))]

    while max(c_j_minus_z_j) > 0:  
        maxIndex = c_j_minus_z_j.index(max(c_j_minus_z_j))

        ratios = []
        for i in range(len(constraints)):
            if constraints[i][0][maxIndex] > 0:
                ratios.append((constraints[i][1]/constraints[i][0][maxIndex], i))
        
        if not ratios:
            return "Unbounded solution"
            
        minRatio, minIndex = min(ratios)

        basis[minIndex] = objFunction[maxIndex]
        resultIndex[minIndex] = maxIndex


        pivot = constraints[minIndex][0][maxIndex]

        old_row = constraints[minIndex].copy()

        constraints[minIndex][0] = [x/pivot for x in constraints[minIndex][0]]
        constraints[minIndex][1] = constraints[minIndex][1]/pivot

        for i in range(len(constraints)):
            if i != minIndex:
                multiplier = constraints[i][0][maxIndex]
                constraints[i][0] = [constraints[i][0][j] - multiplier*constraints[minIndex][0][j] 
                                   for j in range(len(constraints[0][0]))]
                constraints[i][1] = constraints[i][1] - multiplier*constraints[minIndex][1]
        
        z_j = [sum(basis[j]*constraints[j][0][i] for j in range(len(basis))) for i in range(len(constraints[0][0]))]
        c_j_minus_z_j = [objFunction[i] - z_j[i] for i in range(len(z_j))]

    for i in range(len(originalObj)):
        if i in resultIndex:
            result.append(constraints[resultIndex.index(i)][1])
        else:
            result.append(0)
    objFunction = []
    constraints = []
    return result

def parseInputConstrict(input_string: str, objVariables: list[str]) -> tuple:
    """
    Parses a linear equation input string and extracts the coefficients and the result.\n
    Args:\n
        input_string (str): The input string representing a linear equation. \n
                            The equation should be in the form of 'ax + by + cz = d' \n
                            where a, b, c, and d are numbers, and x, y, z are variables.\n
    Returns:\n
        tuple: A tuple containing two elements:\n
            - A list of coefficients (float) for each variable in the equation.\n
            - A float representing the result of the equation.
    """

    

    input_string = input_string.replace(" ", "")
    terms = re.findall(r'([+-]?\d*\.?\d*)([a-zA-Z]+)', input_string)
    coefficients = []
    for var in objVariables:
        coefficient = 0
        for term in terms:
            if term[1] == var:
                coefficient = term[0]
                if coefficient in ['+', '-'] or coefficient == '':
                    coefficient += '1'
                coefficient = float(coefficient)
                break
        coefficients.append(coefficient)
    result = input_string.split('=')[-1]
    return [coefficients, float(result)]

def parseInputObj(input_string: str) -> tuple:
    """
    Parses a linear equation input string and extracts the coefficients and the result.\n
    Args:\n
        input_string (str): The input string representing a linear equation. \n
                            The equation should be in the form of 'ax + by + cz = d' \n
                            where a, b, c, and d are numbers, and x, y, z are variables.\n
    Returns:\n
        tuple: A tuple containing two elements:\n
            - A list of coefficients (float) for each variable in the equation.\n
            - A float representing the result of the equation.
    """
    input_string = input_string.replace(" ", "")
    terms = re.findall(r'([+-]?\d*\.?\d*)([a-zA-Z]+)', input_string)
    coefficients = []
    variables = []
    for term in terms:
        coefficient = term[0]
        variable = term[1]
        if coefficient in ['+', '-'] or coefficient == '':
            coefficient += '1'
        coefficients.append(float(coefficient))
        variables.append(variable)
    return coefficients, variables

def simplexFunction(obj:list, constrict:list[list,int]) -> list:
    """
    Applies the simplex method to solve a linear programming problem.\n
    Parameters:\n
    obj (list): A list representing the objective function coefficients.\n
    constrict (list[list, int]): A list of constraints, where each constraint is represented 
                                 as a list containing the coefficients and the right-hand side value.\n
    Returns:\n
    list: The solution to the linear programming problem, typically including the optimal values 
          of the decision variables and the optimal value of the objective function.
    """

    obj = parseInputObj(obj)
    return simplexMethod(obj[0], [parseInputConstrict(constraint, obj[1]) for constraint in constrict])

