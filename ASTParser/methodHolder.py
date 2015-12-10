from classHolder import Class

class Method:
    def __init__(self, name, parent, scope, static, lineNo, returnType = "void"):
        self.name = name.rstrip('\n')
        self.parent = parent
        self.children = []
        self.parameters = []
        self.scope = scope
        self.static = static
        self.returnType = returnType
        self.lineNo = lineNo

    def getName(self):
        return self.name

    def getChildren(self):
        return self.children

    def getParent(self):
        return self.parent

    def getLineNo(self):
        return self.lineNo

    def addChild(self, child):
        self.children.append(child)

    def addParameter(self, parameter):
        self.parameters.append(parameter)

    def setType(self, returnType):
        self.returnType = returnType

    def setParams(self, parameters):
        self.parameters = parameters

    def getParams(self):
        return self.parameters

    def printNode(self):
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

    def toString(self):
        print ("Method: " + self.name)
