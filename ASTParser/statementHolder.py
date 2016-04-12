# Author: Jordan Cain, 2015-16

from methodHolder import Method

class Statement:
    def __init__(self, name, parent, lineNo, debugObj):
        global debug
        debug = debugObj
        debug.writeTrace("Statement Constructor")
        self.name = name.rstrip('\n')
        self.parent = parent
        self.lineNo = lineNo

    def getName(self):
        debug.writeTrace("Statement Get Name")
        return self.name

    def getParent(self):
        debug.writeTrace("Statement Get Parent")
        return self.parent

    def getLineNo(self):
        debug.writeTrace("Statement Get LineNo")
        return self.lineNo

    def addParameter(self, param):
        debug.writeTrace("Statement Add Parameter")
        self.parameters.add(param)

    def printNode(self):
        debug.writeTrace("Statement PrintNode")
        print (self.name)
