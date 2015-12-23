from methodHolder import Method
from statementHolder import Statement

#class to hold the instance of a recursion
class Recursion():
    def __init__(self, statement, method):
        self.statement = statement
        self.method = method

    def getStatement(self):
        return self.statement

    def getMethod(self):
        return self.method

    def toString(self):
        print (self.method.toString())
        print (self.statement.getName())

class LoopToUnroll():
    def __init__(self, loop):
        self.loop = loop
