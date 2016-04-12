# Author: Jordan Cain, 2015-16

import sys
import re
import parse
from debugUtil import Trace
from classHolder import Class
from methodHolder import Method
from statementHolder import Statement
from loopHolder import Loop
from conditionHolder import Condition

#Function that will return a list of all classes in the tree
#Params: parent is the highest level of the tree
def getClasses(parent, debug):
    debug.writeTrace("Get Classes")
    parent.getChildren()

#Function that will return a list of all methods in the tree
#Params: parent is the highest level of the tree, debug will add extra output to console
def getMethods(parent, debug):
    debug.writeTrace("getMethods, parent: " + parent.getName())
    #get children of the package, get the class(s)
    classes = parent.getChildren()
    classMethods = []
    for currentClass in classes:
        if type(currentClass) is Class:
            classMethods.append(currentClass.getChildren())
        else:
            debug.writeTrace("\tfound not a class" + currentClass.getName())
    #Calling get parent on the top level (the package) returns a list of objects which we append to a list
    #If we have multiple classes in a file we get a list with multiple lists(each list would be a class)
    #We need to filter out any objects that arent of type Method
    #SOURCE:: http://stackoverflow.com/questions/2225038/determine-the-type-of-an-object
    finalMethods = []
    for classMethod in classMethods:
        for method in classMethod:
            if type(method) is Method:
                finalMethods.append(method)
                debug.writeTrace("\tFound a method: " + method.getName())
            else:
                debug.writeTrace("\tFound not method" + method.getName())
    return finalMethods

def getForLoops(parent, debug):
    debug.writeTrace("Get For Loops, parent: " + parent.getName())
    methods = getMethods(parent, debug)
    forLoops = []
    for method in methods:
        statements = method.getChildren()
        for statement in statements:
            if type(statement) is Loop:
                if statement.getLoopType() == "for":
                    forLoops.append(statement)
    return forLoops

def checkIfCStyleLoop(loop, debug):
    debug.writeTrace("Check if C style for loop, returns boolean");
    #C style for loop will have two semicolons with any characters between them
    if re.search("\;.+\;", loop.getName()):
        return True
    else:
        return False


#Function that can be used to recursivly go through a tree and return all statements
#parent must be a method object
def getStatements(parent, debug):
    debug.writeTrace("Get Statements, parent: " + parent.getName())
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

#Helper method for testing all nodes are present
def getNodeCount(parent):
    print(countChildren(parent, 0))

#Recursive method for getting node count
def countChildren(parent, count):
    if type(parent) is not Statement:
        for child in parent.getChildren():
            count += countChildren(child, 1)
    return count
