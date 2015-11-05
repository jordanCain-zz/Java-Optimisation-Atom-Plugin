from statementHolder import Statement

#Condition inheites statement
class Condition(Statement):
    #Condtions can be if, switch...
    def __init__(self, name, parent, conditionType, lineNo = 0):
        Statement.__init__(self, name, parent, lineNo)
        self.conditionType = conditionType
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    #Override
    def printNode(self):
        print (self.name)
        for currentStatement in self.children:
            currentStatement.printNode()
        print ("}")

    def getLoopType(self):
        return self.loopType
