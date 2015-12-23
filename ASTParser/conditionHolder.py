from statementHolder import Statement

#Condition inheites statement
class Condition(Statement):
    #Condtions can be if, switch...
    def __init__(self, name, parent, conditionType, lineNo, debugObj):
        global debug
        debug = debugObj
        debug.writeTrace("Condition Constructor")
        Statement.__init__(self, name, parent, lineNo, debug)
        self.conditionType = conditionType
        self.children = []

    def addChild(self, child):
        debug.writeTrace("Condition Add Child")
        self.children.append(child)

    def getChildren(self):
        debug.writeTrace("Condition Get Children")
        return self.children

    #Override
    def printNode(self):
        debug.writeTrace("Condition PrintNode")
        print (self.name)
        for currentStatement in self.children:
            currentStatement.printNode()
        print ("}")
