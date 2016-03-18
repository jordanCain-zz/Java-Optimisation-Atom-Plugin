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
    unrollables = forLoopUnrollDetect(parent)
    return recursions, unrollables


#Function to print all of the optimisations
def output(recursions, loops):
    debug.writeTrace("Output optimisations")
    for recursion in recursions:
        recursion.toString()
    print("The JVM struggles to optimise recurssion, consider iterative conversion")
    print("\n###################################\n")
    for loop in loops:
        loop.toString()
        unrollLoop(loop)

#Function that will find any occourences of a for loop that can be unrolled
def forLoopUnrollDetect(parent):
    debug.writeTrace("Detect for loops to unroll")
    loops = walker.getForLoops(parent, debug)
    unrollableLoops = []
    #Check if loops use a constant number for the upper range
    #E.g for(int i=0; i<=5; i++)
    for loop in loops:
        if walker.checkIfCStyleLoop(loop, debug):
            condition = loop.getName()[loop.getName().find(';')+1:loop.getName().rfind(';')].lstrip()
            condLeft, condRight = splitCondition(condition)
            iterator, initTo = getConditionIterator(loop.getName())
            #If the iterator is a digit we may be able to unroll
            if initTo.isdigit():
                #If the iterator is used in the condition its more likely
                if iterator in condition:
                    if condLeft.lstrip().isdigit() or condRight.lstrip().isdigit():
                        unrollableLoops.append(LoopToUnroll(loop, iterator, initTo, condRight))
    return unrollableLoops

def unrollLoop(loop):
    loopObject = loop.getLoop() #Get the actual loop object
    if len(loopObject.getChildren()) < 4:
        print("Unrolling loop, Replace current for loop with: ")
        i = 0;
        while i < int(loop.getCondRight()) - int(loop.getInitto()):
            for statement in loopObject.getChildren():
                statement.printNode();
            i += 1
    else:
        print("Loop too long to unroll, \nconsider manually unrolling")

#Function that will find any occorunces of recursion in a method
#Params: parent is the highest level of the tree, debug will add extra output to console
def recursionDetect(parent):
    debug.writeTrace("Recursion Detect")
    #Initialise our return array which will hold recursion objects
    recursions = []
    #Get all the methods in the tree
    methods = walker.getMethods(parent, debug)
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
    return recursions

#Function to help for loop unroll, splits a condition at the operator index
#Param: Loop condition as a string
def splitCondition(condition):
    debug.writeTrace("Split condition: " + condition)
    if '>' in condition:
        condLeft = condition[0:condition.find('>')].lstrip()
        condRight = condition[condition.find('>')+1:].lstrip()
    elif '<' in condition:
        condLeft = condition[0:condition.find('<')].lstrip()
        condRight = condition[condition.find('<')+1:].lstrip()
    elif '=' in condition:
        condLeft = condition[0:condition.find('=')].lstrip()
        condRight = condition[condition.find('=')+1:].lstrip()
    #if we had <= or == we have to trim an extra character off
    if '=' in condRight:
        condRight = condRight.replace('=','').lstrip()
    return condLeft, condRight

#Fucntion to get the iterator variable name and the intialised value
#Param: loop decleration as string
#TODO:: Function will fail if the iterator name contains a number
def getConditionIterator(loop):
    debug.writeTrace("getConditionIterator: " + loop)
    iterator = loop[loop.find('(')+1:loop.find(';')]
    #Strip the type off, E.g int
    iterator = iterator[iterator.find(' '):].lstrip()
    return iterator[:iterator.find(' ')], re.findall(r'\d+', iterator)[0]



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
        debug.writeTrace("Current param: " + param)
        #Check for literals?
        if '(' in param and ')' in param:
            debug.writeTrace("found a function call")
            #TODO::walk the tree to find the return type
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
        debug.writeTrace("ParamTypes: " + str(paramTypes))
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
    else:
        return "Unable To Clean Param"

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
