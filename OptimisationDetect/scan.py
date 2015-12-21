import re
import sys
#SOURCE:: http://stackoverflow.com/questions/4383571/importing-files-from-different-folder-in-python
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTWalker')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser')
import parse
import walker
import debugUtil
from methodHolder import Method
from classHolder import Class
from optimisations import Recursion
from optimisations import LoopToUnroll

def detect(parent, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Detecting Optimisations, parent: ", end='')
        print (parent.getName())
    recursions = recursionDetect(parent, debug)
    return recursions

def output(recursions, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Output optimisations")
    for recursion in recursions:
        recursion.toString()

#Function that will find any occorunces of recursion in a method
#Params: parent is the highest level of the tree, debug will add extra output to console
def recursionDetect(parent, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Recursion Detect")
    #Initialise our return array which will hold recursion objects
    recursions = []
    #Get all the methods in the tree
    methods = walker.getMethods(parent, debug)
    for method in methods:
        #For each method we need to analyse the statements inside it
        statements = walker.getStatements(method, debug)
        #TODO:: Oppurtunity to implement threading here
        for statement in statements:
            if debug == 1:
                print("\tstatement: " + statement.getName() + " #### parent: " + statement.getParent().getName())
            if method.getName() in statement.getName():
                if debug == 1:
                    print ("found a possible recursion: ", end='')
                    print (statement.getName() + "\tin method: " + method.getName() + "Line: " + str(method.getLineNo()))
                statementName = statement.getName()
                methodName = method.getName()
                #Create a substring of the method call and parameters
                statementName = statementName[statementName.index(methodName):]
                #TODO:: if a param is a function call this will break
                statementName = statementName[:statementName.index(')')+1]
                #Get the params of the statement and method
                params = method.getParams()
                methodParamTypes = getMethodParamTypes(params, debug)
                params = parse.getParams(statementName, debug)
                statementParamTypes = getStatementParamTypes(params, method, debug)

                #If paramater types match it's a recurisve call
                if statementParamTypes == methodParamTypes:
                    recursions.append(Recursion(statement, method))
                    if debug == 1:
                        print ("We found an actual recursion")
                        print ("Method:    " + method.toString() + " | line: " + str(method.getLineNo()))
                        print ("Statement: " + statement.getName().lstrip() + " | line: " + str(statement.getLineNo()))
                else:
                    if debug == 1:
                        print ("Not a recursive call")
                if debug == 1:
                    print ("Method param types: " + str(methodParamTypes))
                    print ("Statement param types: " + str(statementParamTypes))
    return recursions

def getMethodParamTypes(params, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Method params: ", end='')
        print (str(params))
    paramTypes = []
    for param in params:
        #SOURCE:: http://stackoverflow.com/questions/959215/removing-starting-spaces-in-python
        param = param.lstrip()
        param = param.split(' ')
        paramTypes.append(param[0])
    return paramTypes

def getStatementParamTypes(params, method, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Statement params: ", end='')
        print (str(params))
    paramTypes = []
    for param in params:
        #Check for literals?
        if '(' in param and ')' in param:
            print ("found a function call")
            #walk the tree to find the return type
        elif param.isdigit():
            paramTypes.append("int")
        elif re.match("\d+\.\d+(f)", param):
            paramTypes.append("float")
        elif '"' in param or "'" in param:
            paramTypes.append("String")
        elif param.lstrip().isalpha():
            #parameter is just a variable
            #Find the type of the variable
            paramTypes.append(findVariable(param.lstrip(), method, debug))
        else:
            paramTypes.append(cleanParam(param.lstrip(), debug))
        if debug == 1:
            print ("ParamTypes: " + str(paramTypes))
    return paramTypes

def cleanParam(param, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Cleaning param: " + param)
    #Lets check if param is a number
    if '-' in param:
        operatorIndex = param.index('-')
    elif '+' in param:
        operatorIndex = param.index('+')
    elif '/' in param:
        operatorIndex = param.index('/')
    elif '*' in param:
        operatorIndex = param.index('*')

    left = param[:operatorIndex]
    right = param[operatorIndex+1:]
    param = getType(left, right, debug)

    if debug == 1:
        print ("left of op: " + left + " right of op: " + right)
        print ("Returning: " + param)
    return param

def getType(left, right, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Get type: left: " + left + " right: " + right)
    if left.isdigit() or right.isdigit():
        if debug == 1:
            print ("Returning int")
        return "int"
    if re.match("\d+\.\d+(f)", left) or re.match("\d+\.\d+(f)", right):
        if debug == 1:
            print ("Returning float")
        return "float"

def findVariable(variable, method, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Find Variable: " + variable)
    #Get a list of all statements in the class to check variable against
    statements = walker.getStatements(method, debug)
    for statement in statements:
        if '=' in statement.getName() and variable in statement.getName():
            if debug == 1:
                print ("Found assignment: ", end='')
                print (statement.getName())
            return getVariableType(statement.getName(), debug)
    return "ERROR: UNABLE TO DETERMINE VARIABLE TYPE"

#Function is a helper method for findVariable()
#Takes a line as parameter and returns the type
def getVariableType(line, debug):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        print ("Get variable type: " + line)
    line = line.lstrip()
    line = line[:line.index(' ')]
    return line




#line ender
