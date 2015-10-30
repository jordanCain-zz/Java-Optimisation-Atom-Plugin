from packageHolder import Package

class Class:
    #SOURCE:: http://stackoverflow.com/questions/2164258/multiple-constructors-in-python
    def __init__(self, name, parent, scope="public", lineNo=0):
        self.name = name
        self.parent = parent
        self.variables = []
        self.children = []
        self.lineNo = lineNo

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def addChild(self, child):
        self.children.extend(child)

    def addVariable(self, variable):
        self.variables.extend(variable)

    def toString(self):
        print ("I'm a class")
        print ("My parent is: ")
