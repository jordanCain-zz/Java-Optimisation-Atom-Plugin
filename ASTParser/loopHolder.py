from statementHolder import Statement

#loop inherits statement
class loop(Statement):
    #Loop has a special attribute, looptype(For, while, do)
    def __init__(self, loopType):
        self.loopType = loopType

    def getLoopType(self):
        return self.loopType
