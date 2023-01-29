import sympy
import dimod
import dwavebinarycsp
import yaml
import ast
from sympy.logic.boolalg import to_cnf
import sys

class ConstraintSatisfactionProblem:
    '''
    This class allows for mapping constraints from a csp onto a binary quadratic model:
     - constraints are specified as satisfiability problem sentences, where the configuration of the variables that satisfies the constraint makes the sentence evaluate to true
     - constraints can contain 3 types of variables:
        1. Binary variables (b)
        2. Real 16 bit floats (f)
        3. Complex 32 bit floats (j) 
     - the constraints can contain boolean operators (and, or, not), as well as any polynomial expressions made up of floats variables
    '''

    sys.setrecursionlimit(10000)

    # dictionaries to map the variable names to the expression specifying the float structures
    __f = dict()
    __j = dict()

    # dictionaries to map the variable names to the binary variable names
    __b = dict()

    # list to store all of the polynomial constraints
    __polyConstraints = []
    # list to store all of the boolean constraints
    __boolConstraints = []

    # the classwide csp that cnf decomposed boolean constraints are added to
    __csp = dwavebinarycsp.ConstraintSatisfactionProblem('BINARY')

    # the classwide bqm that polynomial constraints are added directly to
    __bqm = ""


    def __str__(self):
        return("ConstraintSatisfactionProblem object: total_constraints=" + str(len(self.__polyConstraints) + len(self.__boolConstraints)))


    def __addBinary(self, name):
        '''
        This function is used to add new binary variables to the __b dictionary
        Example:
            >>> self.addBinary("newBinary")
            >>> print(self.__b)
            '{"newBinary": "b0"}'
        '''

        # now find the number of existing binary variables so that the index can be found to add more
        nextBitIndex = len(self.__b)

        # add the new binary variable
        self.__b.update({name: ("b" + str(nextBitIndex))})


    def __addFloat(self, name):
        '''
        This function is used to add 16 bit float variables by defining them based on 16 new binary variables:
         - the variables are not technically floats, because they must be defined as polynomial functions of binary variables
         - instead, they are an approximation of the form:
             - v0: (f0 * -1) * (f1 * 2**0 + f2 * 2**1 + f3 * 2**2 + f4 * 2**3 + f5 * 2**4 + f6 * 2**5 + f7 * 2**6 + f8 * 2**7) * (f9*100 + f10*10 + f11 + f12*0.1 + f13*0.01 + f14*0.001 + f15*0.0001)
         - where f0 through f15 are binary variables in __b
        Example:
            >>> self.__addFloat("newFloat")
            >>> print(self.__f)
            '{"newFloat": "(f0 * -1) * (f1 * 2**0 + f2 * 2**1 + f3 * 2**2 + f4 * 2**3 + f5 * 2**4 + f6 * 2**5 + f7 * 2**6 + f8 * 2**7) * (f9*100 + f10*10 + f11 + f12*0.1 + f13*0.01 + f14*0.001 + f15*0.0001)"}
            >>> print(self.__b)
            '{"f0": "b0", "f1": "b1", "f2": "b2", "f3": "b3", "f4": "b4", "f5": "b5", "f6": "b6", "f7": "b7", "f8": "b8", "f9": "b9", "f10": "b10", "f11": "b11", "f12": "b12", "f13": "b13", "f14": "b14", "f15": "b15"}
        '''

        # the name of the float can not follow the pattern 'f[int]'
        # if it does, raise an exception
        if name[1:].isnumeric and name[0] == 'f':
            raise KeyError("The variable name: " + name + " is of the form 'f[int]', which is not permitted as it will cause the parser to fail")

        # start by figuring out how many floats have already been added and multiply it by 16 to get the index of the next float bit that can be used
        nextFloatBitIndex = len(self.__f) * 16
        n = nextFloatBitIndex
        
        # define the expression form of the float\
        expression = "(f"+str(n+0)+" * -1) * (f"+str(n+1)+" * 2**0 + f"+str(n+2)+" * 2**1 + f"+str(n+3)+" * 2**2 + f"+str(n+4)+" * 2**3 + f"+str(n+5)+" * 2**4 + f"+str(n+6)+" * 2**5 + f"+str(n+7)+" * 2**6 + f"+str(n+8)+" * 2**7) * (f"+str(n+9)+"*100 + f"+str(n+10)+"*10 + f"+str(n+11)+" + f"+str(n+12)+"*0.1 + f"+str(n+13)+"*0.01 + f"+str(n+14)+"*0.001 + f"+str(n+15)+"*0.0001)"

        # now find the number of existing binary variables so that the index can be found to add more
        nextBitIndex = len(self.__b)

        # add the new binary variables to the __b dictionary
        for index in range(16):
            fName = "f" + str(nextFloatBitIndex+index)
            bName = "b" + str(nextBitIndex+index)
            self.__b.update({fName: bName})

        # add the new float definition to the __f dictionary
        self.__f.update({name: expression})


    def __addComplex(self, name):
        '''
        This function is used to add 32 bit complex float variables by defining them based on 32 new binary variables:
         - the variables are defined in terms of the sum of 2 float values, one of which is multiplied by the imaginary unit
         - the term with the imaginary unit is treated as real in the __parseConstraint function, as it does not change how the expression is minimized/maximized
        '''

        # the name of the float can not follow the pattern 'j[int]'
        # if it does, raise an exception
        if name[1:].isnumeric and name[0] == 'j':
            raise KeyError("The variable name: " + name + " is of the form 'j[int]', which is not permitted as it will cause the parser to fail")

        # start by figuring out how many complex floats have already been added and multiply it by 32 to get the index of the next complex float bit that can be used
        nextComplexFloatBitIndex = len(self.__j) * 32
        nextFloatBitIndex = len(self.__f) * 16

        n = nextComplexFloatBitIndex
        
        # define the expression form of the complex float
        realTerm = "(f"+str(n+0)+" * -1) * (f"+str(n+1)+" * 2**0 + f"+str(n+2)+" * 2**1 + f"+str(n+3)+" * 2**2 + f"+str(n+4)+" * 2**3 + f"+str(n+5)+" * 2**4 + f"+str(n+6)+" * 2**5 + f"+str(n+7)+" * 2**6 + f"+str(n+8)+" * 2**7) * (f"+str(n+9)+"*100 + f"+str(n+10)+"*10 + f"+str(n+11)+" + f"+str(n+12)+"*0.1 + f"+str(n+13)+"*0.01 + f"+str(n+14)+"*0.001 + f"+str(n+15)+"*0.0001)"
        imaginaryTerm = "1j * ((f"+str(n+16)+" * -1) * (f"+str(n+17)+" * 2**0 + f"+str(n+18)+" * 2**1 + f"+str(n+19)+" * 2**2 + f"+str(n+20)+" * 2**3 + f"+str(n+21)+" * 2**4 + f"+str(n+22)+" * 2**5 + f"+str(n+23)+" * 2**6 + f"+str(n+24)+" * 2**7) * (f"+str(n+25)+"*100 + f"+str(n+26)+"*10 + f"+str(n+27)+" + f"+str(n+28)+"*0.1 + f"+str(n+29)+"*0.01 + f"+str(n+30)+"*0.001 + f"+str(n+31)+"*0.0001))"
        expression = realTerm + " + " + imaginaryTerm

        # now find the number of existing binary variables so that the index can be found to add more
        nextBitIndex = len(self.__b)

        # add the new binary variables to the __b dictionary
        for index in range(32):
            fName = "f" + str(nextFloatBitIndex+index)
            bName = "b" + str(nextBitIndex+index)
            self.__b.update({fName: bName})

        # add the new complex float definition to the __j dictionary
        self.__f.update({name: expression})

    
    def __getConstraintType(self, constraint):
        '''
        This function parses the constraint to determine if it constrains any polynomial expressions
        Examples:
            >>> self.__getConstraintType("v0 and v1 or v2") # where v0, v1, and v2 are all binary variables
            'boolean'
            >>> self.__getConstraintType("v0 * v1^2 == 10 or v2") # where v0 and v1 are 16 bit float variables and v2 is binary
            'polynomial'
        '''

        boolean = True # set to False if the expression is a polynomial constraint

        # check to see if any of the float variables stored in __f or __j are in this constraint
        for variable in self.__f.keys():
            if variable in constraint:
                boolean = False
                break
        for variable in self.__b.keys():
            if variable in constraint:
                boolean = False
                break

        # if the constraint contains only binary variables, determine if it contains any arithmetical operators
        arithmeticalOperators = ["==", "!=", ">", ">=", "<", "<=", "*", "-", "+"]
        for operator in arithmeticalOperators:
            if operator in constraint:
                boolean = False
                break
        
        # return 'boolean' if boolean is still True, and 'polynomial' otherwise
        if boolean:
            return 'boolean'
        else:
            return 'polynomial'

    
    def __translate(self, expr): 
        '''
        This is a method to convert python syntax boolean to sympy syntax:
         - 'and' -> '&'
         - 'or' -> '|'
         - 'not' -> '~'
        Example:
            >>> self.__translate("v0 and v1 or v2")
            'v0 & v1 | v2'
        '''
        e = list(expr)
        res = [' ' for i in range(len(e))]
        for start in range(len(e)):
            if expr[start: start+3] == 'not':
                res[start] = '~'
                res[start+1] = ''
                res[start+2] = ''
            elif expr[start: start+3] == 'and':
                res[start] = '&'
                res[start+1] = ''
                res[start+2] = ''
            else:
                if res[start] == ' ':
                    res[start] = e[start]

        expr = ''.join(res)         
        e = list(expr)
        res = [' ' for i in range(len(e))]
        for start in range(len(e)):
            if expr[start: start+2] == 'or':
                res[start] = '|'
                res[start+1] = ''
            else:
                if res[start] == ' ':
                    res[start] = e[start]

        res = [elt for elt in res if elt != ' ' or elt != '']
        return ''.join(res)

    
    def __parseConstraint(self, constraint):
        '''
        This function takes a constraint as input, and returns either:
         - the boolean sentence are converted into conjugative normal form and divided into separate constraints along each of the clauses
         - the constraints containing polynomial expressions are converted into a single simplified binary polynomial expression that is returned, along with a string saying if the constraint is a polynomial or a boolean
        Examples:
            >>> self.__b = {"v0": "b0", "v1": "b1", "v2": "b2"}
            >>> self.__parseConstraint("v0 and v1 or v2") # where v0, v1, and v2 are all binary variables
            'b0 & b1 | b2', 'boolean'
            >>> self.__b = {"v2": "b0", "f0": "b1", "f1": "b2", "f2": "b3", "f3": "b4", "f4": "b5", "f5": "b6", "f6": "b7", "f7": "b8", "f8": "b9", "f9": "b10", "f10": "b11", 
              ↪ "f11": "b12", "f12": "b13", "f13": "b14", "f14": "b15", "f15": "b16", "f17": "b18", "f18": "b19", "f19": "b20", "f20": "b21", "f21": "b22", "f22": "b23", 
              ↪ "f23": "b24", "f24": "b25", "f25": "b26", "f26": "b27", "f27": "b28", "f28": "b29", "f29": "b30", "f30": "b31", "f31": "b32"} # adding the binary variables used to declare the float variables
            >>> self.__f = {
              ↪ "v0": "(f0 * -1) * (f1 * 2**0 + f2 * 2**1 + f3 * 2**2 + f4 * 2**3 + f5 * 2**4 + f6 * 2**5 + f7 * 2**6 + f8 * 2**7) * (f9*100 + f10*10 + f11 + f12*0.1 + f13*0.01 + f14*0.001 + f15*0.0001)", 
              ↪ "v1": "(f16 * -1) * (f17 * 2**0 + f18 * 2**1 + f19 * 2**2 + f20 * 2**3 + f21 * 2**4 + f22 * 2**5 + f23 * 2**6 + f24 * 2**7) * (f25*100 + f26*10 + f27 + f28*0.1 + f29*0.01 + f30*0.001 + f31*0.0001)
              ↪ "} # add the float variables and their declaration polynomial expressions to the __f dictionary
            >>> self.__parseConstraint("v0 * v1**2 == 10 or v2")
            '1638400000000*b1**2*b10**2*b18**2*b26**2*b9**2*f16**2 - 256000000*b1**2*b10**2*b18*b2*b26*b9*f16 - ... + 0.256*b25*b32**2*f16 + v2 + 100', 'polynomial' # snipped for brevity
        '''

        constraintType = 'boolean' # will be set to 'polynomial' if the sentence is a polynomial

        # determine if the constraint is boolean or polynomial
        if (self.__getConstraintType(constraint) == 'boolean'):
            # add it to __boolConstraints
            self.__boolConstraints.append(constraint)

            # if it is a boolean, convert the constraint into cnf form

            # simplify the binary sentence using sympy and convert it to conjunctive normal form
            constraint = str(to_cnf(self.__translate(constraint), simplify=True, force=True))

            # once in this form, the sentence can be split up along the and operators into many separate constraints

            constraint.replace(" ", "") # remove spaces
            constraint.replace("|", " | ") # place spaces in between the or keyword
            constraint.replace("~", " ~ ") # place spaces in between the not keyword
            constraint.replace("(", "")
            constraint.replace(")", "") # remove the parentheses


        else:
            constraintType = 'polynomial'

            # add to __polyConstraints
            self.__polyConstraints.append(constraint)
            
            '''
            If it is a polynomial, begin by converting comparative operators into expressions to be minimized:
             - exp1 == expr2 -> min((exp1 - exp2)**2)
             - exp1 != expr2 -> max((exp1 * exp2)**2) = min(-1 * (exp1 * exp2)**2)
             - exp1 < exp2 or exp1 <= exp2 -> max(exp2 - exp1) = min(exp1 - exp2)
             - exp1 > exp2 or exp1 >= exp2 -> max(exp1 - exp2) = min(exp2 - exp1)
            '''

            # remove spaces
            constraint = constraint.replace(" ", "")
            # convert the logical operators into single character forms
            constraint = constraint.replace("and", "&")
            constraint = constraint.replace("or", "|") # because or is equivalent to and using this method
            constraint = constraint.replace("not", "~")
            
            startBounds = ["&", "|", "~"] # list storing the possible operators that exist on the edge of an expression to help find the bounds of the expressions
            endBounds = ["&", "|", "~"]
            startIndex = 0 # variables to store the index of the start and end of expressions being acted on by some operator
            endIndex = 0

            # handle ==
            index = constraint.find("==")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "(((" + operation.replace("==", ")-(") + "))**2)"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("==")

            # handle !=
            index = constraint.find("!=")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "(-1*((" + operation.replace("!=", ")-(") + "))**2)"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("!=")

            # handle <=
            index = constraint.find("<=")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.replace("<=", ")-(") + "))"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("<=")

            # handle <
            index = constraint.find("<")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.replace("<", ")-(") + "))"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("<")

            # handle >=
            index = constraint.find(">=")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.split(">=")[1] + ")-(" + operation.split(">=")[0] + "))"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find(">=")

            # handle >
            index = constraint.find(">")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.split(">")[1] + ")-(" + operation.split(">")[0] + "))"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find(">")

            '''
            Now expand the constraint by converting the logical operator into expressions:
             - exp1 and exp2 -> min(exp1 + exp2)
             - exp1 or exp2 = not(not(exp1) and not(exp2)) -> -1 * min(-1*exp1 + -1*exp2) = min(exp1 + exp2))
             - Therefore, using this method of combining the polynomial expressions, or is equivalent to and
             - not(exp1) = -1 * exp1
            '''

            # handle 'not'
            index = constraint.find("~")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                startIndex = index
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds) and not(i == 0):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "(" + operation.replace("~", "-1 * ") + ")"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("~")
            
            # handle 'or'
            constraint = constraint.replace("|", "-")

            # handle 'and'
            constraint = constraint.replace("&", "-")

            constraint = constraint.replace("(", "( ").replace(")", " )").replace("**", "^").replace("+", " + ").replace("*", " * ").replace("^", " ** ")

            # now substitute in the binary forms of each of the variables
            for var in self.__f.keys():
                index = constraint.find(var)
                lenDif = 0

                while not(index == lenDif-1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    subsLen = 0
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back

                            # verified that this is not a substring
                            if postIndex == 0:
                                subs = str(sympy.expand(self.__f[var]))
                                subsLen = len(subs)
                                constraint = constraint[0:index] + subs
                            else:
                                subs = str(sympy.expand(self.__f[var]))
                                subsLen = len(subs)
                                constraint = constraint[0:index] + subs + constraint[index+len(var):]

                    unchecked = constraint[index+subsLen+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

            constraint = constraint.replace("(", "( ").replace(")", " )").replace("**", "^").replace("+", " + ").replace("*", " * ").replace("^", " ** ")
            
            for var in self.__j.keys():
                index = constraint.find(var)
                lenDif = 0

                while not(index == lenDif-1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                subs = str(sympy.expand(self.__j[var].replace("1j * ", "")))
                                subsLen = len(subs)
                                constraint = constraint[0:index] + subs
                            else:
                                subs = str(sympy.expand(self.__f[var].replace("1j * ", "")))
                                subsLen = len(subs)
                                constraint = constraint[0:index] + subs + constraint[index+len(var):]

                    unchecked = constraint[index+subsLen+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked
            
            constraint = constraint.replace("(", "( ").replace(")", " )").replace("**", "^").replace("+", " + ").replace("*", " * ").replace("^", " ** ")
            
            # replace all of the binary variables with their names as stored in __b
            for var in self.__b.keys():
                index = constraint.find(var)
                lenDif = 0

                while not(index == lenDif-1):
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*", "/"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                constraint = constraint[0:index] + str(self.__b[var])
                            else:
                                constraint = constraint[0:index] + str(self.__b[var]) + constraint[index+len(var):]

                    unchecked = constraint[index+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

            constraint = constraint.replace("(", "( ").replace(")", " )").replace("**", "^").replace("+", " + ").replace("*", " * ").replace("^", " ** ")
            
            # commented out the line below because simplifying the constraint both here and in toQUBO is slow and redundant
            # constraint = str(sympy.expand(constraint, deep=True, modulus=None, power_base=True, power_exp=True, mul=True, log=False, multinomial=True, basic=True))

            ''' 
            The above operations yield a polynomial function that is returned.  To convert this into a bqm, do the following: 
                >>> polynomial, constType = self.__parseConstraint(constraint) # where constraint is a string storing the constraint
                >>> matrix = self.__solveMatrix(polynomial, inVars, True) # use the solveMatrix function to get the coefficients of the polynomial (which corresponds to the matrix in the QUBO formulation of bqms)
                >>> bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)  # QUBO
                >>> dimod.make_quadratic(test, 10.0, bqm = bqm) # define the BQM
            '''

        # return the formatted constraint and the constrain type
        return constraint, constraintType

    
    def __solveMatrix(self, eq, inVars, Max=False):
        '''
        This function is used to convert input binary polynomial into a bqm (and return the matrix), as accurately as possible
        Args:
         - eq (str): the input polynomial, formatted as a string
         - inVars (dict): a dictionary storing the names of all of the variables used (as strings)
         - Max (bool): a boolean value, which, if set to True, inverts the input function (can be used it you want to maximize the polynomial)
        Examples:
            >>> self.__solveMatrix("b0**2 + 5*b1**3 - 12*b0*b1", {"b0": "b0", "b1": "b1"})
            {('b0', 'b1'): -12.0, ('b0',): 1, ('b1',): 1}
        '''

        numOfVars = len(inVars)
        poly = "{"
        positive = []
        negative = []

        splitEq = eq.split("+") # split along the +
        for i in splitEq:
            spl = i.split("-") # split along the -
            for j in range(len(spl)):
                if (j != 0): # skip over the positive term
                    if (spl[j] == " "): # if there is a blank term
                        pass
                    else:
                        spl[j] = spl[j].replace("(", "")
                        spl[j] = spl[j].replace(")", "")
                        negative.append(spl[j].replace(" ", ""))
                else: # append the positive term
                    if (spl[j] == " "): # if there is a blank term
                        pass
                    else:
                        spl[0] = spl[0].replace("(", "")
                        spl[0] = spl[0].replace(")", "")
                        positive.append(spl[0].replace(" ", "")) 

        # swap the pos and neg if we want to max the function (this corresponds to multiplying the function by -1)
        if (Max):
            temp = positive
            positive = negative
            negative = temp

        for i in negative:

            # get rid of all exponents
            mult = i.split("**")
            mult[0] += "*"
            for m in range(len(mult)):
                if (m > 0):
                    product = ""
                    terms = mult[m].split("*")
                    for n in range(len(terms)):
                        if (n > 0):
                            product += terms[n] + "*"
                        else:
                            if "/" in terms[n]:
                                product += "/" + terms[n].split("/")[1] + "*"
                    mult[m] = product

            mul = ""
            for m in mult:
                mul += m
            mul = mul[:-1:]

            # now find the number that this term is multiplied by
            fac = 1
            divisor = "1"

            if ('/' in mul): # fractional coefficient
                mul, divisor = mul.split('/')

            for m in mul.split("*"):
                try:
                    fac = float(m)
                except:
                    if(fac == 1):
                        fac = 1

            '''
            Explanation for the divisor variable:
             - given an expression with a fractional coefficient, sympy will format it as
                "a*x/b" for the expression "a/b * x"
             - for this reason, we must check for both the fac (numerator of the fractional coefficient), and the divisor (denominator of the fractional coefficient)
            '''
            fac /= float(divisor)

            contained = []
            for j in inVars.keys():
                confined = i.split(inVars[j])
                if (len(confined)>1):
                    next = confined[1]
                    if (len(next) == 0): # if the var is actually contained (not in a substring)
                        contained.append(inVars[j])
                    elif (next[0] == "*" or next[0] == "/"):
                        contained.append(inVars[j]) # if the var is actually contained (not in a substring)

            if (len(contained) == 1): # if there is only one variable in the term
                # add polynomial to poly string
                key = "('" + contained[0] + "',):"
                if (key in poly): # if this key already has a value, just add the current value to the existing value
                    # find the value for the existing key
                    index = poly.find(key)+len(key)
                    value = ""
                    while (poly[index] != ","):
                        value += poly[index]
                        index += 1
                    # add the values
                    poly = poly.replace(key+value, key+str(float(value)-fac))

                else:
                    poly += key + " -" + str(fac) + ", " 

            elif (len(contained) > 1): # if there are several vars
                varList = ""
                for n in contained:
                    varList += "'" + n + "', "
                varList = varList[:-2:]
                
                key = "(" + varList + "):"
                if (key in poly): # if this key already has a value, just add the current value to the existing value
                    # find the value for the existing key
                    index = poly.find(key)+len(key)
                    value = ""
                    while (poly[index] != ","):
                        value += poly[index]
                        index += 1
                    # add the values
                    poly = poly.replace(key+value, key+str(float(value)-fac))
                else:
                    poly += key + " -" + str(fac) + ", "

        for i in positive: # now do the same thing but with the positives
        
            # get rid of all exponents
            mult = i.split("**")
            mult[0] += "*"
            for m in range(len(mult)):
                if (m > 0):
                    product = ""
                    terms = mult[m].split("*")
                    for n in range(len(terms)):
                        if (n > 0):
                            product += terms[n] + "*"
                        else:
                            if "/" in terms[n]:
                                product += "/" + terms[n].split("/")[1] + "*"
                    mult[m] = product

            mul = ""
            for m in mult:
                mul += m
            mul = mul[:-1:]

            # now find the number that this term is multiplied by
            fac = 1
            divisor = 1

            if ('/' in mul): # fractional coefficient
                mul, divisor = mul.split('/')

            for m in mul.split("*"):
                try:
                    fac = float(m)
                except:
                    if(fac == 1):
                        fac = 1

            '''
            Explanation for the divisor variable:
             - given an expression with a fractional coefficient, sympy will format it as
                "a*x/b" for the expression "a/b * x"
             - for this reason, we must check for both the fac (numerator of the fractional coefficient), and the divisor (denominator of the fractional coefficient)
            '''
            fac /= float(divisor)

            contained = []
            for j in inVars.keys():
                confined = i.split(inVars[j])
                if (len(confined)>1):
                    next = confined[1]
                    if (len(next) == 0): # if the var is actually contained (not in a substring)
                        contained.append(inVars[j])
                    elif (next[0] == "*" or next[0] == "/"):
                        contained.append(inVars[j]) # if the var is actually contained (not in a substring)
            
            if (len(contained) == 1): # if there is only one variable in the term
                # add polynomial to poly string
                key = "('" + contained[0] + "',):"
                if (key in poly): # if this key already has a value, just add the current value to the existing value
                    # find the value for the existing key
                    index = poly.find(key)+len(key)
                    value = ""
                    while (poly[index] != ","):
                        value += poly[index]
                        index += 1
                    # add the values
                    poly = poly.replace(key+value, key+" "+str(float(value)+fac))
                else:
                    poly += key + " " + str(fac) + ", "

            elif (len(contained) > 1): # if there are several vars
                varList = ""
                for n in contained:
                    varList += "'" + n + "', "
                varList = varList[:-2:]
                
                key = "(" + varList + "):"
                if (key in poly): # if this key already has a value, just add the current value to the existing value
                    # find the value for the existing key
                    index = poly.find(key)+len(key)
                    value = ""
                    while (poly[index] != ","):
                        value += poly[index]
                        index += 1
                    # add the values
                    poly = poly.replace(key+value, key+" "+str(float(value)+fac))
                else:
                    poly += key + " " + str(fac) + ", "

        # check to see if there are any terms that have been canceled out
        for j in inVars.keys():
            if not(inVars[j] + "'," in poly or inVars[j] + "')" in poly): # variable not in poly matrix keys
                poly += "('" + inVars[j] + "'): 0, "

        poly = poly[:-2:] + "}"

        try:
            poly = ast.literal_eval(poly) 
        except:
            raise KeyError("Could not recognize the variables in inVars")
        
        return poly # return the polynomial coefficients as a dictionary


    def fromStr(self, constraint, binary, real, complx):
        '''
        This is a function to add a constraint from a string
         - constraint is the constraint stored in a string
         - binary is a list of the binary variables used in the constraint
         - real is a list of the real variables used in the constraint
         - complx is a list of the complex variables used in the constraint
        Example:
            >>> self.fromString("a * b > c**2 or d", ["d"], ["a", "b"], ["c"])
        '''

        # begin by adding the variables if they do not already exist
        for variable in binary:
            if not(variable in self.__b.keys()):
                # this variable is new, so add it to __b
                self.__addBinary(variable)

        for variable in real:
            if not(variable in self.__f.keys()):
                # this variable is new, so add it to __f
                self.__addFloat(variable)

        for variable in complx:
            if not(variable in self.__j.keys()):
                # this variable is new, so add it to __j
                self.__addComplex(variable)

        parsedConstraint, constraintType = self.__parseConstraint(constraint) # parse the constraint

        if constraintType == 'boolean':
            # if the constraint is boolean
            constraint = constraint.replace("|", "or").replace("~", "not")
            constraints = constraint.split("&") # divide the constraint into all of the subconstraints along each of the clauses in cnf

            for subConstraint in constraints:
                # loop over each of the subconstraints

                variables = [] # get a list of all of the variables in this constraint
                for variable in binary.keys():
                    if variable in subConstraint and not(variable in variables):
                        # if this is a new variable
                        variables.append(variable)

                # define the function form of this subconstraints
                def func (*var_configuration, var=variables, constraint=subConstraint):
                    configuration = dict(zip(var, var_configuration))
                    apply_not = False
                    for term in constraint.split(' '):
                        if term == 'not':
                            if apply_not:
                                apply_not = False
                            else:
                                apply_not = True
                        if term in var:
                            if apply_not:
                                term = not(configuration[term])
                            else:
                                term = configuration[term]
                            if term: # if even one term is positive in cnf, then the whole subconstraint evaluates to true
                                return True
                    return False # all terms evaluated to false

                self.__csp.add_constraint(func, variables) 

        elif constraintType == 'polynomial':
            # if the constraint is polynomial
            if len(self.__bqm) == 0:
                # if this is the first polynomial constraint to be added
                self.__bqm = parsedConstraint
            else:
                # if this is not the first polynomial constraint to be added
                self.__bqm += " + " + parsedConstraint
                self.__bqm = str(sympy.expand(self.__bqm, simplify=True)) # add the constraint term to the bqm and expand it again


    def fromFile(self, filename):
        '''
        This is a function to open constraint(s) from a yaml file
         - the yaml file should contain constraints with keys of the form "constraint0", "constraint1", etc
         - the value of these keys should be the constraints as strings
         - there should also be 3 entries storing lists of variable names:
            - "binary" (stores the names of binary variables)
            - "real" (stores the names of the real variables)
            - "complx" (stores the names of the complex variables)
        Example:
            >>> self.fromFile("constraints.yaml")
        '''
        with open(filename) as file:
            dictionary = yaml.safe_load(file)

            constraints = []
            binary = []
            real = []
            complx = []

            # for each constraint, convert it into a set of vectors and append them to the constraints list
            for key, value in dictionary.items():
                if "constraint" in key:
                    # this element is a constraint
                    constraints.append(value)

                elif "binary" in key:
                    # this element is the binary variables list
                    binary = list(value)

                elif "real" in key:
                    # this element is the real variables list
                    real = list(value)

                elif "complx" in key:
                    # this element is the complex variables list
                    complx = list(value)

            # add each of the constraints
            for constraint in constraints:
                self.fromStr(constraint, binary, real, complx) # use the fromStr function to add this constraint


    def toQUBO(self): 
        '''
        This is a function that returns the constraints in the form of a quadratic unconstrained binary optimization problem (or QUBO)
         - returns: a tuple containing the biases as a dictionary, and the offset
        Example:
            >>> self.toQUBO()
            ({('b0', 'b1'): -3.9999999991051727, ('b0', 'b0'): 1.999999998686436, ('b1', 'b1'): 1.9999999986863806}, 8.661749095750793e-10)
        '''

        # start by converting the boolean constraints stored in the dwavebinarycsp object into a polynomial expression 
        boolCSP = dimod.AdjDictBQM(dwavebinarycsp.stitch(self.__csp)) # convert the csp into an AdjDictBQM
        boolQUBO = boolCSP.to_qubo()[0] # convert the AdjDictBQM object into a qubo dictionary

        boolExpr = ""

        # use the qubo dictionary to generate the corresponding polynomial expression
        for term in boolQUBO.keys():
            firstVar = term[0]
            secondVar = term[1] # get the variables that this coefficient belongs to

            boolExpr += str(boolQUBO[term]) + "*" + firstVar + "*" + secondVar + " + "

        # add the boolExpr to the polynomial constraints, which are already encoded in a bqm string
        expr = str(sympy.expand((boolExpr + self.__bqm), simplify=True))

        # calculate the offset, or the constant coefficient in the expression
        offsetStr = expr.split("+")[-1] 
        if ("b" in offsetStr):
            # if the last term is not constant, then the offset is 0
            offsetStr = "0"
        offset = float(offsetStr)

        # now convert the polynomial expression back into a qubo in the form of an AdjDictBQM object
        asMatrix = self.__solveMatrix(expr, self.__b)

        # before the new polynomial can be reduced to a quadratic, it needs to be reformatted such that the variable names are all single characters
        # this is done by casting the variable names to unicode characters using the chr function
        charMatrix = {}
        for key in asMatrix.keys():
            if (type(key) is tuple):
                newKey = ()
                for element in key:
                    newKey = newKey + (chr(int(element.replace("b", ""))+161),)
                charMatrix[newKey] = asMatrix[key]
            else:
                newKey = (chr(int(key.replace("b", ""))+161),)
                charMatrix[newKey] = asMatrix[key]

        # reduce the generated charMatrix QUBO to a polynomial that will optimize the same way by using dimod.higherorder.utils.make_quadratic
        charBQM = dimod.higherorder.utils.make_quadratic(charMatrix, 10000, 'BINARY')
        charQUBO = charBQM.to_qubo()[0]

        # convert the charQUBO variable names back into the proper format
        returnQUBO = {}
        for key in charQUBO.keys():
            if (type(key) is tuple):
                newKey = ()
                for element in key:
                    newKey = newKey + ("*".join(["b"+str(ord(e)-161) for e in element.split("*")]),)
                returnQUBO[newKey] = charQUBO[key]
                
            else:
                variable = "*".join(["b"+str(ord(e)-161) for e in key.split("*")])
                newKey = (variable, variable) # linear terms are on the diagonal of the QUBO matrix
                returnQUBO[newKey] = charQUBO[key]
        # return the QUBO
        return (returnQUBO, offset)


    def checkConfiguration(self, configuration, err=0.0):
        '''
        This function takes a dictionary of values of variables and returns the number of constraints satisfied by the configuration (within a margin of error specified in err)
        Example:
            >>> self.fromString('(a or b) and c', ['a', 'b', 'c'], [], [])
            >>> self.checkConfiguration({'a': 1, 'b': 0, 'c': 1}, 0.1) # should return that 1 constraint is satisfied by this configuration
            1
        '''

        # start by making a copy of __b, __f, and __j, as well as the constraint lists
        b = self.__b
        f = self.__f
        j = self.__j

        boolConstraints = self.__boolConstraints
        polyConstraints = self.__polyConstraints

        # now set all of the variables values based on the configuration dictionary
        for key in configuration.keys():
            if (key in b.keys()): # if this variable exists in b set its value 
                b[key] = configuration[key]

            elif (key in f.keys()): # if this variable exists in f set its value 
                f[key] = configuration[key]

            elif (key in j.keys()): # if this variable exists in b set its value 
                j[key] = configuration[key]

        startBounds = ["&", "|", "~"] # list storing the possible operators that exist on the edge of an expression to help find the bounds of the expressions
        endBounds = ["&", "|", "~"]

        # parse the constraints so that they apply within the error margin passed as an argument
        for constraint in polyConstraints:
            #handle ==
            index = constraint.find("==")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "(abs((" + operation.replace("==", ")-(") + ")) < " + str(err) + ")"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("==")

            # handle !=
            index = constraint.find("!=")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "(abs((" + operation.replace("!=", ")-(") + ")) > " + str(err) + ")"
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("!=")

            # handle <=
            index = constraint.find("<=")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.replace("<=", ")-(") + ")) <= " + str(err)
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("<=")

            # handle <
            index = constraint.find("<")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.replace("<", ")-(") + ")) < " + str(err)
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find("<")

            # handle >=
            index = constraint.find(">=")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.split(">=")[1] + ")-(" + operation.split(">=")[0] + ")) <= " + str(err)
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find(">=")

            # handle >
            index = constraint.find(">")
            while not(index == -1):
                # find the limits of the expressions that the operator is acting on
                for i in range(index): # beginning
                    if (i+1 == index):
                        # if index i is the start of the constraint
                        startIndex = 0
                    elif (constraint[index - (i+1)] in startBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        startIndex = (index - (i)) 
                        break
                for i in range(len(constraint) - index): # end
                    if (index+i) == (len(constraint)-1):
                        # if index i is the end of the constraint
                        endIndex = len(constraint)
                    elif (constraint[index + i] in endBounds):
                        # if i marks the index of the start of the expression being acted on by this operator
                        endIndex = index + i
                        break
                # get the expression that this operator acts on as a separate string
                operation = constraint[startIndex:endIndex]
                operationExp = "((" + operation.split(">")[1] + ")-(" + operation.split(">")[0] + ")) < " + str(err)
                constraint = constraint[0:startIndex] + operationExp + constraint[endIndex:len(constraint)]
                index = constraint.find(">")

        # now for each of the constraints, substitute the values in for the variables so that they can be evaluated
        for var in f.keys():
            for constraint in polyConstraints:
                index = constraint.find(var)
                while not(index == -1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                constraint = constraint[0:index] + str(f[var])
                            else:
                                constraint = constraint[0:index] + str(f[var]) + constraint[index+len(var):]

                    unchecked = constraint[index+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

        for var in j.keys():
            for constraint in polyConstraints:
                index = constraint.find(var)
                while not(index == -1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                constraint = constraint[0:index] + str(j[var])
                            else:
                                constraint = constraint[0:index] + str(j[var]) + constraint[index+len(var):]
                                
                    unchecked = constraint[index+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

        # substitute in any remaining binary representations
        for var in b.keys():
            for constraint in polyConstraints:
                index = constraint.find(var)
                while not(index == -1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                constraint = constraint[0:index] + str(b[var])
                            else:
                                constraint = constraint[0:index] + str(b[var]) + constraint[index+len(var):]
                                
                    unchecked = constraint[index+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

        # now for each of the constraints in boolConstraints, substitute the values in for the variables so that they can be evaluated
        for var in f.keys():
            for constraint in boolConstraints:
                index = constraint.find(var)
                while not(index == -1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                constraint = constraint[0:index] + str(f[var])
                            else:
                                constraint = constraint[0:index] + str(f[var]) + constraint[index+len(var):]

                    unchecked = constraint[index+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

        for var in j.keys():
            for constraint in boolConstraints:
                index = constraint.find(var)
                while not(index == -1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                constraint = constraint[0:index] + str(j[var])
                            else:
                                constraint = constraint[0:index] + str(j[var]) + constraint[index+len(var):]
                                
                    unchecked = constraint[index+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

        # substitute in any remaining binary representations
        for var in b.keys():
            for constraint in boolConstraints:
                index = constraint.find(var)
                while not(index == -1):
                    
                    if (index+len(var)-1) == len(constraint):
                        postIndex = 0 # index of the character after the variable name
                    else:
                        postIndex = index + len(var)
                    if index == 0:
                        preIndex = 0 # index of the character before the variable name
                    else:
                        preIndex = index - 1

                    # make sure that this instance of the variable is not a substring within another variable name
                    separators = [" ", "(", ")", "-", "+", "*"] # list of valid characters that can come before or after a variable name
                    if (preIndex == 0  or constraint[preIndex] in separators): # valid front
                        if (postIndex == 0 or constraint[postIndex] in separators): # valid back
                            # verified that this is not a substring
                            if postIndex == 0:
                                constraint = constraint[0:index] + str(b[var])
                            else:
                                constraint = constraint[0:index] + str(b[var]) + constraint[index+len(var):]
                                
                    unchecked = constraint[index+1:]
                    lenDif = len(constraint) - len(unchecked)
                    index = unchecked.find(var) + lenDif # get the index of the next instance of var that has not been checked

        # now go through each of the constraints and count how many evaluate to True
        constraintsMet = 0

        for constraint in polyConstraints:
            try:
                # try to evaluate the constraint
                if (eval(constraint)):
                    constraintsMet += 1
            except:
                # if the eval fails because not all of the variables were assigned a variable, do not update constraintsMet
                pass

        for constraint in boolConstraints:
            try:
                # try to evaluate the constraint
                if (eval(constraint)):
                    constraintsMet += 1
            except:
                # if the eval fails because not all of the variables were assigned a variable, do not update constraintsMet
                pass

        # return the number of constraints that are met
        return constraintsMet
