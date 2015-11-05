from packageHolder import Package
from classHolder import Class
from methodHolder import Method
from statementHolder import Statement
from conditionHolder import Condition
from loopHolder import Loop

#Function to read in the contents of a file line by line and load into a list
#SOURCE:: http://stackoverflow.com/questions/18084554/why-do-i-get-a-syntaxerror-for-a-unicode-escape-in-my-file-path ---raw file path
def readFile():
    fname = r"C:\Users\jordan\Documents\GitHub\javaParser\SampleJavaFiles\ADSWeek3.java"
    with open(fname) as fil:
        content = fil.readlines()
    return content

#Function to iterate over all the lines of a file
def analyseFile(content):
    print ("analyseFileContents")
    #we use an iterator so we can track the line number
    currentParent = Package("SuperParent")
    for i, line in enumerate(content):
        currentParent = analyseLine(line, currentParent)
    print (currentParent.toString())
    return currentParent

#Function called to analyse an individual line
#SOURCE:: https://docs.python.org/2/tutorial/controlflow.html
#SOURCE:: http://www.tutorialspoint.com/python/python_if_else.htm ---elif
#SOURCE:: https://docs.python.org/2/tutorial/introduction.html#strings ---for slicing strings
def analyseLine(line, parent):
    #List with all basic return types for checking a method decleration
    returnTypes = ["void", "boolean", "String", "char", "byte", "short", "int", "long", "float", "double"]
    #TODO:: covert decision branch to use regex
    if "package" in line[0:7]:
        parent = packageFound(line)
        return parent
    elif "import" in line[0:6]:
        importFound(line, parent)
    elif "class" in line:
        parent = classFound(line, parent)
        return parent
    elif ("public" in line) or ("private" in line):
        #TODO:: This method detection will not work, it will detect class attributes as methods
        parent = methodFound(line, parent)
        return parent
    elif ("if" in line) or ("else" in line) or ("switch" in line):
        #TODO:: Improve condition detection (check it's surrounded in parenthesis?)
        parent = conditionFound(line, parent)
        return parent
    elif ("for" in line) and ("{" in line):
        #TODO:: Improve loop detection (Check it's surrounded in parenthesis?)
        #TODO:: Needs to detect while, do-while
        parent = loopFound(line, parent)
        return parent
    elif ("}" in line) and (not "{" in line):
        # '}' denotes we have left a block and need to go up a parent
        #print ("moving up parent from: ", parent.getName(), " to: ", parent.getParent().getName())
        parent = parent.getParent()
    else:
        #SOURCE:: http://stackoverflow.com/questions/2405292/how-to-check-if-text-is-empty-spaces-tabs-newlines-in-python
        if line.isspace() == False:
            statementFound(line, parent)
    return parent

#Function called when a new package is found
def packageFound(line):
    print ("found package: " + line[8:-2])
    newPackage = Package(line[8:-2])
    return newPackage

def importFound(line, parent):
    print ("found import: " + line[7:-1])
    #Adds the import to an attribute of a package
    parent.addImport(line[7:-1])

#Function called when a new class is found
def classFound(line, parent):
    print ("found class: " + line)
    startIndex = (line.index("class") + 6)
    newClass = Class(line[startIndex:-3], parent)
    parent.addChild(newClass)
    return newClass

#Function called when a new method is found
def methodFound(line, parent):
    print ("found method: " + line)
    #Get the method name
    endIndex = line.index('(')
    startIndex = endIndex
    while (line[startIndex] != ' '):
        startIndex -= 1
    newMethod = Method(line[startIndex:endIndex], parent)
    getMethodParams(line, newMethod)
    parent.addChild(newMethod)
    return newMethod

def getMethodParams(line, method):
    startIndex = line.index('(')+1
    endIndex = line.index(')')
    line = line[startIndex:endIndex]
    line = line.split(',')
    for param in line:
        print ("adding param: ", param)
        method.addParameter(param)

#Function called when a new statement is found
def statementFound(line, parent):
    print ("Found statement: " + line)
    newStatement = Statement(line, parent)
    parent.addChild(newStatement)

#Function called when a new condition is found
def conditionFound(line, parent):
    print ("Found condition: " + line)
    newCondition = Condition(line, parent, "if")
    parent.addChild(newCondition)
    return newCondition

#Function called when a new loop is found
def loopFound(line, parent):
    print ("Found loop: " + line)
    newLoop = Loop(line, parent, "for")
    parent.addChild(newLoop)
    return newLoop

#Function to print a simple tree to console
def printTree(parent):
    print ("Start node: ", parent.getName())
    print ("###############################")
    parent.printNode()


################################################################################
#Start code
fileContents = readFile()
parent = analyseFile(fileContents)
printTree(parent)
