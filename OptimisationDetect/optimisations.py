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
        print ("Possible Inefficient Recursion: ")
        print ("\tRecursive Method:")
        print ("\t\t",self.method.toString())
        print ("\t\tLine: ", self.method.getLineNo())
        print ("\tRecursive call:")
        print ("\t\t",self.statement.getName().lstrip())
        print ("\t\t Line: ", self.statement.getLineNo())

class LoopToUnroll():
    def __init__(self, loop, iterator, initTo):
        self.loop = loop
        self.iterator = iterator
        self.initTo = initTo

    def getLoop(self):
        return self.loop

    def getIterator(self):
        return self.iterator

    def getInitto(self):
        return self.initTo

    def toString(self):
        print ("Unrollable For Loop:")
        print ("\t",self.loop.getName().lstrip())
        print ("\t Line:   ", self.loop.getLineNo())
        print ("\t Method: ", self.loop.getParent().toString())
