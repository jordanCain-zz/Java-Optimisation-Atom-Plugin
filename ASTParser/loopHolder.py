from statementHolder import Statement

#loop inherits statement
class Loop(Statement):
    #Loop has a special attribute, looptype(For, while, do)
    def __init__(self, name, parent, loopType, lineNo, debugObj):
        global debug
        debug = debugObj
        debug.writeTrace("Loop Constructor")
        Statement.__init__(self, name, parent, lineNo, debug)
        self.loopType = loopType
        self.children = []

    def addChild(self, child):
        debug.writeTrace("Loop Add Child")
        self.children.append(child)

    def getChildren(self):
        debug.writeTrace("Loop Get Child")
        return self.children

    #Override
    def printNode(self):
        debug.writeTrace("Loop PrintNode")
        print (self.name)
        for currentStatement in self.children:
            currentStatement.printNode()
        print ("}")

    def getLoopType(self):
        debug.writeTrace("Loop Get Loop Type")
        return self.loopType
