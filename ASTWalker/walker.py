import sys
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
import parse
import inspect
from classHolder import Class
from methodHolder import Method
from statementHolder import Statement
from loopHolder import Loop
from conditionHolder import Condition

def stackTrace():
    formatStackTrace(len(inspect.stack())-2)
    print (inspect.stack()[1][3] + " ", end="")
    formatStackTrace(len(inspect.stack())-2)
    print (" " + inspect.stack()[1][1] + " : " + str(inspect.stack()[1][2]-2))

def formatStackTrace(count):
    while count > 0:
        print("  ", end="")
        count -= 1

#Function that will return a list of all classes in the tree
#Params: parent is the highest level of the tree
def getClasses(parent):
    if debug == 2:
        stackTrace()
    parent.getChildren()

#Function that will return a list of all methods in the tree
#Params: parent is the highest level of the tree, debug will add extra output to console
def getMethods(parent, debug):
    if debug == 2:
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

#Function that can be used to recursivly go through a tree and return all statements
def getStatements(parent, debug):
    if debug == 2:
        stackTrace()
    if debug == 1:
        print ("Get Statements: " + parent.getName())
    statements = []
    if type(parent) is Statement:
        return statements.extend(parent)
    else:
        for statement in parent.getChildren():
            if type(statement) is Statement:
                statements.append(statement)
            else:
                statements.append(statement)
                statements.extend(getStatements(statement, debug))
    return statements






#line ender
