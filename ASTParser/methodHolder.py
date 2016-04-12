# Author: Jordan Cain, 2015-16

from classHolder import Class

class Method:
    def __init__(self, name, parent, scope, static, lineNo, debugObj, returnType = "void"):
        global debug
        debug = debugObj
        debug.writeTrace("Method Constructor")
        self.name = name.rstrip('\n')
        self.parent = parent
        self.children = []
        self.parameters = []
        self.scope = scope
        self.static = static
        self.returnType = returnType
        self.lineNo = lineNo

    def getName(self):
        debug.writeTrace("Method Get Name")
        return self.name

    def getChildren(self):
        debug.writeTrace("Method Get Children")
        return self.children

    def getParent(self):
        debug.writeTrace("Method Get Parent")
        return self.parent

    def getLineNo(self):
        debug.writeTrace("Method Get LineNo")
        return self.lineNo

    def addChild(self, child):
        debug.writeTrace("Method Add Child")
        self.children.append(child)

    def addParameter(self, parameter):
        debug.writeTrace("Method Add Parameter")
        self.parameters.append(parameter)

    def setType(self, returnType):
        debug.writeTrace("Method Set Type")
        self.returnType = returnType

    def setParams(self, parameters):
        debug.writeTrace("Method Set Params")
        self.parameters = parameters

    def getParams(self):
        debug.writeTrace("Method Get Params")
        return self.parameters

    #Print the method and all children
    def printNode(self):
        debug.writeTrace("Method PrintNode")
        output = self.scope
        if self.static:
            output = output + " static"
        output = output + self.returnType +self.name +'('
        for param in self.parameters:
            output = output + param + ','
        print (output[0:-1], ") {")
        #Statements inside of method
        for currentStatement in self.children:
            currentStatement.printNode()
        print ("}")

    #Function to print just the name of the method, scope and parameters
    def toString(self):
        debug.writeTrace("Method ToString")
        output = self.scope.lstrip()
        if self.static:
            output = output + " static"
        output = output + self.returnType +self.name +'('
        for param in self.parameters:
            output = output + param + ','
        return (output[0:-1] + ")")
