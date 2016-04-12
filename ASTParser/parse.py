# Author: Jordan Cain, 2015-16

from packageHolder import Package
from classHolder import Class
from classHolder import Attribute
from methodHolder import Method
from statementHolder import Statement
from conditionHolder import Condition
from loopHolder import Loop
from tryCatchHolder import TryCatch
from debugUtil import Trace
import re

#Function to read in and print the file
def read(fileName, debugObj):
    global debug
    debug = debugObj
    debug.writeTrace("Starting scan")
    fileContents = readFile(fileName)
    parent = analyseFile(fileContents)
    return parent

#Function to read in the contents of a file line by line and load into a list
def readFile(fname):
    debug.writeTrace("Read File")
    with open(fname) as fil:
        content = fil.readlines()
    return content

#Function to iterate over all the lines of a file
def analyseFile(content):
    debug.writeTrace("Analyse file")
    #we use an iterator so we can track the line number
    currentParent = Package("SuperParent", 0, debug)
    for i, line in enumerate(content):
        currentParent = analyseLine(line.rstrip('\n'), currentParent, i)
    return currentParent

#Function called to analyse an individual line
#SOURCE:: https://docs.python.org/2/tutorial/controlflow.html
#SOURCE:: http://www.tutorialspoint.com/python/python_if_else.htm ---elif
#SOURCE:: https://docs.python.org/2/tutorial/introduction.html#strings ---for slicing strings
#SOURCE:: https://docs.python.org/2/library/re.html ---regex
#SOuRCE:: http://www.regexr.com/ ---more regex
#SOURCE:: http://stackoverflow.com/questions/2405292/how-to-check-if-text-is-empty-spaces-tabs-newlines-in-python ---empty line
def analyseLine(line, parent, lineNo):
    debug.writeTrace("AnalyseLine: " + line + "\nCurrent parent: " + parent.getName())
    if re.search("(package)\s.+(;)", line):
        #regex: package, whitespace, one or more chars, finally semi-colon
        parent = packageFound(line, lineNo)
        return parent
    elif re.search("(import)\s\w+.*(;)", line):
        importFound(line, parent, lineNo)
    elif re.search("\w+\s(class)\s\w+\s(\{)", line):
        #regex: one or more words, whitespace, "class", whitespace, one or more words, {
        parent = classFound(line, parent, lineNo)
        return parent
    elif re.search("((public)|(private))\s.*(\().*(\))", line):
        #regex: public or private, whitespace, any number of chars, "(", any number of chars, finally ")"
        parent = methodFound(line, parent, lineNo)
        return parent
    elif re.search("((private)|(public))\s((static)\s)?[A-z]*\s[A-z0-9]+\s*((\;)|(\=.*\;))", line):
        #regex: public or private, whitespace, possible static, word, whitespace,word,possible whitespace, semicolon or = plus chars semicolon
        classAtributeFound(line, parent, lineNo)
    elif re.search("((if)|(else if)|(switch))\s?(\()[0-9A-z\-\=\&\|\!\^\>\<\[\]\s\(\)\.\"\'\,\+]+(\))|(else)", line):
        #regex: condition with conditional, 1 or 0 whitespace, "(", any condition, ")" or "else"
        parent = conditionFound(line, parent, lineNo)
        return parent
    elif re.search("((for)\s*(\().+(\)))|((while)\s*(\().*(\)))[^;]|(do)\s*\{", line):
        parent = loopFound(line, parent, lineNo)
        return parent
    elif re.search("(try\s*\{)", line):
        parent = tryFound(line, parent, lineNo)
        return parent
    elif re.search("(catch\s*\([A-z0-9]+\s+[A-z0-9]+\))", line):
        catchFound(line, parent, lineNo)
    elif ("}" in line) and (not "{" in line) and (not re.search("(catch\s*\([A-z0-9]+\s+[A-z0-9]+\))", line)):
        # '}' denotes we have left a block and need to go up a parent except for in the case of a try catch
        parent = parent.getParent()
    else:
        if line.isspace() == False:
            statementFound(line, parent, lineNo)
    return parent

#Function called when a new package is found
def packageFound(line, lineNo):
    debug.writeTrace("found package: " + line[8:-1])
    newPackage = Package(line[8:-1], lineNo, debug)
    return newPackage

def importFound(line, parent, lineNo):
    debug.writeTrace("found import: " + line[7:-1])
    #Adds the import to an attribute of a package
    parent.addImport(line[7:-1])

#Function called when a new class is found
def classFound(line, parent, lineNo):
    debug.writeTrace("found class: " + line)
    startIndex = (line.index("class") + 6)
    newClass = Class(line[startIndex:-2], parent, getScope(line), lineNo, debug)
    parent.addChild(newClass)
    return newClass

#Function called when a class atribute is found
#TODO:: Improve the detection of differnt elements by using split(' ')
#TODO:: Ensure we can pick up static attributes
def classAtributeFound(line, parent, lineNo):
    debug.writeTrace("found classAtrribute: " + line)
    scope = getScope(line)
    if scope is "public":
        startIndex = 9
    elif scope is "private":
        startIndex = 10
    if re.search("\s(static)\s", line):
        startIndex += 7
    endIndex = startIndex
    while (line[endIndex] != ' '):
        endIndex += 1
    dataType = line[startIndex:endIndex]
    endIndex += 1
    startIndex = endIndex
    while ((line[endIndex] != ' ') and (line[endIndex] != ';') and (line[endIndex] != '=')):
        endIndex += 1
    name = line[startIndex:endIndex]
    if '=' not in line:
        newAttribute = Attribute(parent, name, scope, dataType)
    else:
        newAttribute = Attribute(parent, name, scope, dataType, line[line.index('=')+2:-2])


#Function called when a new method is found
def methodFound(line, parent, lineNo):
    debug.writeTrace("found method: " + line)
    #Get the method name
    endIndex = line.index('(')
    startIndex = endIndex
    while (line[startIndex] != ' '):
        startIndex -= 1
    newMethod = Method(line[startIndex:endIndex], parent, getScope(line), isStatic(line), lineNo, debug)
    newMethod.setParams(getParams(line))
    newMethod.setType(getType(line, newMethod))
    parent.addChild(newMethod)
    return newMethod

#Function called when a new statement is found
def statementFound(line, parent, lineNo):
    debug.writeTrace("Found statement: " + line)
    newStatement = Statement(line, parent, lineNo, debug)
    if type(parent) is TryCatch:
        if not parent.getCatchStatement:
            parent.addTryChild(newStatement)
        else:
            parent.addCatchChild(newStatement)
    else:
        parent.addChild(newStatement)

#Function called when a new condition is found
#Returns the condition object as a new parent
def conditionFound(line, parent, lineNo):
    debug.writeTrace("Found condition: " + line)
    #TODO:: Detect switch statements
    newCondition = Condition(line, parent, "if", lineNo, debug)
    parent.addChild(newCondition)
    return newCondition

#Function called when a new loop is found
#Returns the loop object as a new parent
def loopFound(line, parent, lineNo):
    debug.writeTrace("Found loop: " + line)
    if re.search("((for)\s*(\().+(\)))", line):
        newLoop = Loop(line, parent, "for", lineNo, debug)
    if re.search("((while)\s*(\().*(\)))[^;]", line):
        newLoop = Loop(line, parent, "while", lineNo, debug)
    if re.search("(do)\s*\{", line):
        newLoop = Loop(line, parent, "do", lineNo, debug)
    parent.addChild(newLoop)
    return newLoop

def tryFound(line, parent, lineNo):
    debug.writeTrace("Found try statement: " + line)
    newTryCatch = TryCatch(line, parent, lineNo, debug)
    parent.addChild(newTryCatch)
    return newTryCatch

def catchFound(line, parent, lineNo):
    debug.writeTrace("Found catch statement: " + line)
    parent.addCatchStatement(line, lineNo)

#Function to determine whether a method is public or private and return it
def getScope(line):
    debug.writeTrace("Get scope: " + line)
    #regex is slow, so use "in"
    #SOURCE:: http://stackoverflow.com/questions/4901523/whats-a-faster-operation-re-match-search-or-str-find
    if "public" in line:
        return "public"
    elif "private" in line:
        return "private"
    return "NULL"

#Function to determine whether a class attribute/method is static
def isStatic(line):
    debug.writeTrace("Is static: " + line)
    if "static" in line:
        return True
    return False

#Function to get the return type of a method
def getType(line, newMethod):
    debug.writeTrace("Get type: " + line)
    endIndex = line.index(newMethod.getName())
    startIndex = endIndex - 1
    while (line[startIndex] != ' '):
        startIndex -= 1
    return line[startIndex:endIndex]

def getParams(line):
    debug.writeTrace("Get params: " + line)
    startIndex = line.index('(')+1
    endIndex = line.rindex(')')
    line = line[startIndex:endIndex]
    line = line.split(',')
    parameters = []
    for param in line:
        parameters.append(param)
    return parameters

#Function to print a simple tree to console
def printTree(parent):
    debug.writeTrace("Start node: " + parent.getName())
    parent.printNode()
