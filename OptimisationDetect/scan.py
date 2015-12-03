import re
import sys
#SOURCE:: http://stackoverflow.com/questions/4383571/importing-files-from-different-folder-in-python
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTWalker')
import parse
import walker
#SOURCE:: http://stackoverflow.com/questions/2654113/python-how-to-get-the-callers-method-name-in-the-called-method
import inspect
#SOURCE:: http://stackoverflow.com/questions/1156023/print-current-call-stack-from-a-method-in-python-code
import traceback
from methodHolder import Method
from classHolder import Class

def stackTrace():
    formatStackTrace(len(inspect.stack())-2)
    print (inspect.stack()[1][3] + " ", end="")
    formatStackTrace(len(inspect.stack())-2)
    print (" " + inspect.stack()[1][1] + " : " + str(inspect.stack()[1][2]-2))

def formatStackTrace(count):
    while count > 0:
        print("  ", end="")
        count -= 1

def detect(parent, debug):
    if debug == 2:
        stackTrace()
    if debug == 1:
        print ("Detecting Optimisations")
    recursionDetect(parent, debug)

#Function that will find any occorunces of recursion in a method
#Params: parent is the highest level of the tree, debug will add extra output to console
def recursionDetect(parent, debug):
    if debug >= 2:
        stackTrace()
    if debug == 1:
        print ("Recursion Detect")
    #Get all the methods in the tree
    methods = walker.getMethods(parent, debug)
    for method in methods:
        #For each method we need to analyse the statements inside it
        #TODO:: this get children also needs to check if the children have any children
        #i.e a condition statement will have children
        statements = method.getChildren()
        for statement in statements:
            if debug == 1:
                print("\tstatement: " + statement.getName() + " #### parent: " + statement.getParent().getName())
            if method.getName() in statement.getName():
                if debug == 0:
                    print ("found a possible recursion: ", end='')
                    print (statement.getName() + "\tin method: " + method.getName())
                #We now need to ensure the function call is to the method we're in
                #It could be a function with the same name but different list of Params
                #When comparing parameters we need to compare types not names!
                statementName = statement.getName()
                methodName = method.getName()
                #Create a substring of the method call and parameters
                statementName = statementName[statementName.index(methodName):]
                statementName = statementName[:statementName.index(')')+1]

                params = method.getParams()
                methodParamTypes = getMethodParamTypes(params, debug)

                params = parse.getParams(statementName, debug)
                statementParamTypes = getStatementParamTypes(params, method, debug)

                if statementParamTypes == methodParamTypes:
                    print ("We found an actual recursion!!!!")

                if debug == 1:
                    print ("Method param types: " + str(methodParamTypes))
                    print ("Statement param types: " + str(statementParamTypes))

def getMethodParamTypes(params, debug):
    if debug == 2:
        stackTrace()
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
        stackTrace()
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
        stackTrace()
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
        stackTrace()
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
        stackTrace()
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
        stackTrace()
    if debug == 1:
        print ("Get variable type: " + line)
    line = line.lstrip()
    line = line[:line.index(' ')]
    return line
















#line ender
