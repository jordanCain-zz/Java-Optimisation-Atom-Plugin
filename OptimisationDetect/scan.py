import re
import sys
import time
#SOURCE:: http://stackoverflow.com/questions/4383571/importing-files-from-different-folder-in-python
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTWalker')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser')
import parse
import walker
from debugUtil import Trace
from methodHolder import Method
from classHolder import Class
from optimisations import Recursion
from optimisations import LoopToUnroll

def detect(parent, debugObj):
    global debug
    debug = debugObj
    debug.writeTrace("Detecting Optimisations, parent: " + parent.getName())
    recursions = recursionDetect(parent)
    return recursions

#Function to print all of the optimisations
def output(recursions):
    debug.writeTrace("Output optimisations")
    for recursion in recursions:
        recursion.toString()

#Function that will find any occourences of a for loop that can be unrolled
def forLoopUnrollDetect(parent):
    if debug == 2:
        debugUtil.stackTrace()
    if debug == 1:
        debugUtil.userTrace("Detect for loops to unroll")

#Function that will find any occorunces of recursion in a method
#Params: parent is the highest level of the tree, debug will add extra output to console
def recursionDetect(parent):
    debug.writeTrace("Recursion Detect")
    #Initialise our return array which will hold recursion objects
    recursions = []
    #Get all the methods in the tree
    methods = walker.getMethods(parent, debug)
    time1 = time.time()
    for method in methods:
        #For each method we need to analyse the statements inside it
        statements = walker.getStatements(method, debug)
        #TODO:: Oppurtunity to implement threading here
        for statement in statements:
            debug.writeTrace("\tstatement: " + statement.getName() + " #### parent: " + statement.getParent().getName())
            if method.getName() in statement.getName():
                debug.writeTrace(statement.getName() + "\tin method: " + method.getName() + "Line: " + str(method.getLineNo()))
                statementName = statement.getName()
                methodName = method.getName()
                #Create a substring of the method call and parameters
                statementName = statementName[statementName.index(methodName):]
                #TODO:: if a param is a function call this will break
                statementName = statementName[:statementName.index(')')+1]
                #Get the params of the statement and method
                params = method.getParams()
                methodParamTypes = getMethodParamTypes(params)
                params = parse.getParams(statementName)
                statementParamTypes = getStatementParamTypes(params, method)

                #If paramater types match it's a recurisve call
                if statementParamTypes == methodParamTypes:
                    recursions.append(Recursion(statement, method))
                    debug.writeTrace("We found an actual recursion")
                    debug.writeTrace("Method:    " + method.toString() + " | line: " + str(method.getLineNo()))
                    debug.writeTrace("Statement: " + statement.getName().lstrip() + " | line: " + str(statement.getLineNo()))
                else:
                    debug.writeTrace("Not a recursive call")
                debug.writeTrace("Method param types: " + str(methodParamTypes))
                debug.writeTrace("Statement param types: " + str(statementParamTypes))
        time2 = time.time()
        print ("time taken: " + str(time2 - time1))
    return recursions

def getMethodParamTypes(params):
    debug.writeTrace("Method params: " + str(params))
    paramTypes = []
    for param in params:
        #SOURCE:: http://stackoverflow.com/questions/959215/removing-starting-spaces-in-python
        param = param.lstrip()
        param = param.split(' ')
        paramTypes.append(param[0])
    return paramTypes

def getStatementParamTypes(params, method):
    debug.writeTrace("Statement params: " + str(params))
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
            paramTypes.append(findVariable(param.lstrip(), method))
        else:
            paramTypes.append(cleanParam(param.lstrip()))
        if debug == 1:
            print ("ParamTypes: " + str(paramTypes))
    return paramTypes

def cleanParam(param):
    debug.writeTrace("Cleaning param: " + param)
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
    param = getType(left, right)

    debug.writeTrace("left of op: " + left + " right of op: " + right)
    debug.writeTrace("Returning: " + param)
    return param

def getType(left, right):
    debug.writeTrace("Get type: left: " + left + " right: " + right)
    if left.isdigit() or right.isdigit():
        debug.writeTrace("Returning int")
        return "int"
    if re.match("\d+\.\d+(f)", left) or re.match("\d+\.\d+(f)", right):
        debug.writeTrace("Returning float")
        return "float"

def findVariable(variable, method):
    debug.writeTrace("Find Variable: " + variable)
    #Get a list of all statements in the class to check variable against
    statements = walker.getStatements(method, debug)
    for statement in statements:
        if '=' in statement.getName() and variable in statement.getName():
            debug.writeTrace("Found assignment: " + statement.getName())
            return getVariableType(statement.getName())
    return "ERROR: UNABLE TO DETERMINE VARIABLE TYPE"

#Function is a helper method for findVariable()
#Takes a line as parameter and returns the type
def getVariableType(line):
    debug.writeTrace("Get variable type: " + line)
    line = line.lstrip()
    line = line[:line.index(' ')]
    return line




#line ender
