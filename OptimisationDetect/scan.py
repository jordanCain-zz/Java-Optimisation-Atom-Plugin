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

def scan():
    debug = False
    parent = parse.read(debug)
    #print ("top level" + parent.getName())
    recursionDetect(parent, debug)

#Function that will find any occorunces of recursion in a method
#Params: parent is the highest level of the tree, debug will add extra output to console
def recursionDetect(parent, debug):
    if debug:
        #Stack trace experimentation
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print ("Caller name: ", calframe[1][3])
        #######################################
        print ("Stack trace: ")
        for line in traceback.format_stack():
            print("\t" + line.strip())
        #End of stack trace experimentation
        print ("Recursion Detection")
    #Get all the methods in the tree
    methods = getMethods(parent, debug)
    for method in methods:
        #For each method we need to analyse the statements inside it
        statements = method.getChildren()
        for statement in statements:
            if debug :
                print("\tstatement: " + statement.getName() + " #### parent: " + statement.getParent().getName())
            if method.getName() in statement.getName():
                if True:#debug:
                    print ("found a possible recursion")
                    print (statement.getName() + "\tin method: " + method.getName())
                #We now need to ensure the function call is to the method we're in
                #It could be a function with the same name but different list of Params
                params = parse.getParams(statement.getName())
                print (params)

#Function that will return a list of all classes in the tree
#Params: parent is the highest level of the tree
def getClasses(parent):
    parent.getChildren()

#Function that will return a list of all methods in the tree
#Params: parent is the highest level of the tree, debug will add extra output to console
def getMethods(parent, debug):
    if debug:
        print("getMethods")
    #get children of the package, get the class(s)
    classes = parent.getChildren()
    classMethods = []
    for currentClass in classes:
        if type(currentClass) is Class:
            classMethods.append(currentClass.getChildren())
        elif debug:
            print ("\tfound not a class")
    #Calling get parent on the top level (the package) returns a list of objects which we append to a list
    #If we have multiple classes in a file we get a list with multiple lists(each list would be a class)
    #We need to filter out any objects that arent of type Method
    #SOURCE:: http://stackoverflow.com/questions/2225038/determine-the-type-of-an-object
    finalMethods = []
    for classMethod in classMethods:
        for method in classMethod:
            if type(method) is Method:
                finalMethods.append(method)
                if debug:
                    print ("\tFound a method: " + method.getName())
            elif debug:
                print ("\tFound not method")
    return finalMethods

scan()
