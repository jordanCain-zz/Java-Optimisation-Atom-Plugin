import sys
#SOURCE:: http://stackoverflow.com/questions/4383571/importing-files-from-different-folder-in-python
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
import parse
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
    #Get all the methods in the tree
    methods = getMethods(parent, debug)
    for method in methods:
        #For each method we need to analyse the statements inside it
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

                params = parse.getParams(statementName, debug)
                if debug == 0:
                    print ("calling get params: " + statementName)
                    print ("statement params: " + str(params))
                methodParamTypes = getMethodParamTypes(method, debug)

#Function that will return a list of all classes in the tree
#Params: parent is the highest level of the tree
def getClasses(parent):
    if debug >= 2:
        stackTrace()
    parent.getChildren()

#Function that will return a list of all methods in the tree
#Params: parent is the highest level of the tree, debug will add extra output to console
def getMethods(parent, debug):
    if debug >= 2:
        stackTrace()
    if debug == 1:
        print("getMethods")
    #get children of the package, get the class(s)
    classes = parent.getChildren()
    classMethods = []
    for currentClass in classes:
        if type(currentClass) is Class:
            classMethods.append(currentClass.getChildren())
        elif debug == 1:
            print ("\tfound not a class" + currentClass.getName())
    #Calling get parent on the top level (the package) returns a list of objects which we append to a list
    #If we have multiple classes in a file we get a list with multiple lists(each list would be a class)
    #We need to filter out any objects that arent of type Method
    #SOURCE:: http://stackoverflow.com/questions/2225038/determine-the-type-of-an-object
    finalMethods = []
    for classMethod in classMethods:
        for method in classMethod:
            if type(method) is Method:
                finalMethods.append(method)
                if debug == 1:
                    print ("\tFound a method: " + method.getName())
            elif debug == 1:
                print ("\tFound not method" + method.getName())
    return finalMethods

def getMethodParamTypes(method, debug):
    params = method.getParams()
    if debug == 0:
        print ("method params: ", end='')
        print (str(params))
    paramTypes = []
    for param in params:
        #SOURCE:: http://stackoverflow.com/questions/959215/removing-starting-spaces-in-python
        param = param.lstrip()
        param = param.split(' ')
        paramTypes.append(param[0])
    return paramTypes
