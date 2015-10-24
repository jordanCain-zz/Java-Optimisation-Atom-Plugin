from methodHolder import Method

class Statement:
    def __init__(self, name, parent, lineNo):
        self.name = name
        self.parent = parent
        self.parameters = []
        self.lineNo = lineNo

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def addParameter(self, param):
        self.parameters.add(param)

    def toString(self):
        print ("I'm a statement")
