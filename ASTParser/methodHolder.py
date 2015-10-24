from classHolder import Class

class Method:
    def __init__(self, name, parent, scope, returnType, lineNo):
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
        self.children.extend(child)

    def addParameter(self, parameter):
        self.parameters.extend(parameter)

    def toString(self):
        print ("I'm a method")
