from statementHolder import Statement

#loop inherits statement
class TryCatch(Statement):
    #tryCatch has two sets of children, the try statements and the catch statements
    def __init__(self, name, parent, lineNo):
        Statement.__init__(self, name, parent, lineNo)
        self.tryChildren = []
        self.catchChildren = []

    def addCatchStatement(self, catch, lineNo):
        self.catchStatement = catch
        self.catchLineNo = lineNo

    def addTryChild(self, child):
        self.tryChildren.append(child)

    def addCatchChild(self, child):
        self.catchChildren.append(child)

    def getCatchStatement(self):
        return self.catchStatement

    def getChildren(self):
        return (self.tryChildren + self.catchChildren)

    def getTryChildren(self):
        return self.tryChildren

    def getCatchChildren(self):
        return self.catchChildren

    #Override
    def printNode(self):
        print (self.name)
        for currentStatement in self.tryChildren:
            currentStatement.printNode()
        for currentStatement in self.catchChildren:
            currentStatement.printNode()
        print ("}")

    def getLoopType(self):
        return self.loopType
