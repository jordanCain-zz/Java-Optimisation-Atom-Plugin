from methodHolder import Method

class Statement:
    def __init__(self, name, parent, lineNo):
        self.name = name.rstrip('\n')
        self.parent = parent
        self.lineNo = lineNo

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def getLineNo(self):
        return self.lineNo

    def addParameter(self, param):
        self.parameters.add(param)

    def printNode(self):
        print (self.name)
