from classHolder import Class

class Method:
    def __init__(self, name, parent, scope = "public", returnType = "void", lineNo = 0):
        self.name = name
        self.parent = parent
        self.children = []
        self.parameters = []
        self.scope = scope
        self.returnType = returnType
        self.lineNo = lineNo

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def addChild(self, child):
        self.children.append(child)

    def addParameter(self, parameter):
        self.parameters.append(parameter)

    def printNode(self):
        #Method name
        #print (self.name, "(", end="")
        output = self.name + "("
        #Method params
        for param in self.parameters:
            output = output + param + ','
        print (output[0:-1], ") {")
        #Statements inside of method
        for currentStatement in self.children:
            currentStatement.printNode()
        print ("}")

    def toString(self):
        print ("I'm a method")
