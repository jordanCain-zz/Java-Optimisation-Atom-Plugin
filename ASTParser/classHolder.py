# Author: Jordan Cain, 2015-16

from packageHolder import Package

class Class:
    #SOURCE:: http://stackoverflow.com/questions/2164258/multiple-constructors-in-python
    def __init__(self, name, parent, scope, lineNo, debugObj, inheritance = ""):
        global debug
        debug = debugObj
        debug.writeTrace("Class Constructor")
        self.name = name.rstrip('\n')
        self.parent = parent
        self.variables = []
        self.children = []
        self.lineNo = lineNo
        self.inheritance = inheritance

    def getName(self):
        debug.writeTrace("Class Get Name")
        return self.name

    def getParent(self):
        debug.writeTrace("Class Get Parent")
        return self.parent

    def getChildren(self):
        debug.writeTrace("Class Get Child")
        return self.children

    def addChild(self, child):
        debug.writeTrace("Class Add child")
        self.children.append(child)

    def addVariable(self, variable):
        debug.writeTrace("Class Add Variable")
        self.variables.append(variable)

    def printNode(self):
        debug.writeTrace("Class Print Node")
        print (self.name)
        for currentMethod in self.children:
            currentMethod.printNode()
        print ("}")

    def toString(self):
        print ("I'm a class")
        print ("My parent is: ")

class Attribute:
    def __init__(self, parent, name, scope, dataType, value = ""):
        debug.writeTrace("Class Attribute Constructor")
        self.parent = parent
        self.name = name
        self.scope = scope
        self.value = value
        self.type = dataType

    def getName(self):
        debug.writeTrace("Class Attribute get name")
        return self.name

    def printNode(slef):
        debug.writeTrace("Class Attribute Print Node")
        if self.value is "":
            print (self.scope + self.type + self.name + ";")
        else:
            print (self.scope + self.type + self.name + " = " + self.value + ";")
