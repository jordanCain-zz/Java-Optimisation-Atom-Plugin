# Author: Jordan Cain, 2015-16

from statementHolder import Statement

#loop inherits statement
class TryCatch(Statement):
    #tryCatch has two sets of children, the try statements and the catch statements
    def __init__(self, name, parent, lineNo, debugObj):
        global debug
        debug = debugObj
        debug.writeTrace("TryCatch Constructor")
        Statement.__init__(self, name, parent, lineNo, debugObj)
        self.tryChildren = []
        self.catchChildren = []

    def addCatchStatement(self, catch, lineNo):
        debug.writeTrace("TryCatch Add Catch Statement")
        self.catchStatement = catch
        self.catchLineNo = lineNo

    def addTryChild(self, child):
        debug.writeTrace("TryCatch Add Try child")
        self.tryChildren.append(child)

    def addCatchChild(self, child):
        debug.writeTrace("TryCatch Add Catch Child")
        self.catchChildren.append(child)

    def addChild(self, child):
        debug.writeTrace("TryCath Add child")
        if self.getCatchStatement:
            self.addCatchChild(child)
        else:
            self.addTryChild(child)

    def getName(self):
        debug.writeTrace("TryCatch Get Name")
        return self.name

    def getCatchStatement(self):
        debug.writeTrace("TryCatch Get Catch Statement")
        return self.catchStatement

    def getChildren(self):
        debug.writeTrace("TryCatch Get cildren")
        return (self.tryChildren + self.catchChildren)

    def getTryChildren(self):
        debug.writeTrace("TryCatch Get Try children")
        return self.tryChildren

    def getCatchChildren(self):
        debug.writeTrace("TryCatch Get Catch Children")
        return self.catchChildren

    def getParent(self):
        debug.writeTrace("TryCatch Get Parent")
        return self.parent

    #Override
    def printNode(self):
        debug.writeTrace("TryCatch Print Node")
        print (self.name)
        for currentStatement in self.tryChildren:
            currentStatement.printNode()
        for currentStatement in self.catchChildren:
            currentStatement.printNode()
        print ("}")
