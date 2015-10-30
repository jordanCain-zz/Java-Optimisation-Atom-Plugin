from packageHolder import Package
from classHolder import Class
from methodHolder import Method
from statementHolder import Statement

def testData():
    newPackage = Package("package")
    print ("Get name of package: " + newPackage.getName())

    newClass = Class("class", newPackage)
    print ("Get name of class: " + newClass.getName())
    print ("Get parent of class: " + newClass.getParent().getName())

    newMethod = Method("method", newClass, "scope", "return type")
    print ("Get name of method: " + newMethod.getName())
    print ("Get parent of method: " + newMethod.getParent().getName())
    print ("Get parent of parent method: " + newMethod.getParent().getParent().getName())

    newStatement = Statement("statement", newMethod)
    print ("Get name of statement: " + newStatement.getName())
    print ("Get parent of statement: " + newStatement.getParent().getName())
    print ("Get parent of parent statement: " + newStatement.getParent().getParent().getName())
    print ("Get parent of parent of parent statement: " + newStatement.getParent().getParent().getParent().getName())

#Function to read in the contents of a file line by line and load into a list
#SOURCE:: http://stackoverflow.com/questions/18084554/why-do-i-get-a-syntaxerror-for-a-unicode-escape-in-my-file-path ---raw file path
def readFile():
    fname = r"C:\Users\jordan\Documents\GitHub\javaParser\SampleJavaFiles\HelloWorld.java"
    with open(fname) as f:
        content = f.readlines()
    return content

#Function to iterate over all the lines of a file
def analyseFile(content):
    print ("analyseFileContents")
    #we use an iterator so we can track the line number
    currentParent = Package("SuperParent")
    for i, line in enumerate(content):
        currentParent = analyseLine(line, currentParent)
        print ("current parent: " + currentParent.name)

#Function called to analyse an individual line
#SOURCE:: https://docs.python.org/2/tutorial/controlflow.html
#SOURCE:: http://www.tutorialspoint.com/python/python_if_else.htm ---elif
#SOURCE:: https://docs.python.org/2/tutorial/introduction.html#strings ---for slicing strings
def analyseLine(line, parent):
    #List with all basic return types for checking a method decleration
    returnTypes = ["void", "boolean", "String", "char", "byte", "short", "int", "long", "float", "double"]
    if "package" in line[0:7]:
        parent = packageFound(line)
        return parent
    elif "import" in line[0:6]:
        importFound(line, parent)
    elif "class" in line:
        parent = classFound(line, parent)
        return parent
    #TODO:: This method detection will not work, it will detect class attributes as methods
    elif ("public" in line) or ("private" in line):
        methodFound(line)
    return parent

#Function called when a new package is found
def packageFound(line):
    print ("found package: " + line[8:-2])
    newPackage = Package(line[8:-2])
    return newPackage

def importFond(line, parent):
    print ("found import: " + line[7:-1])
    parent.addImport(line[7:-1])

#Function called when a new class is found
def classFound(line, parent):
    print ("found class: " + line)
    startIndex = (line.index("class") + 6)
    newClass = Class(line[startIndex:-3], parent)
    return newClass

#Function called when a new method is found
#SOURCE:: http://stackoverflow.com/questions/7961499/best-way-to-loop-over-a-python-string-backwards
def methodFound(line):
    print ("found method: " + line)
    endIndex = line.index('(')

################################################################################
#Start code
fileContents = readFile()
analyseFile(fileContents)
