from packageHolder import Package

class Class:
    #SOURCE:: http://stackoverflow.com/questions/2164258/multiple-constructors-in-python
    #TODO:: pass line number in
    def __init__(self, name, parent, scope, inheritance = "", lineNo=0):
        self.name = name
        self.parent = parent
        self.variables = []
        self.children = []
        self.lineNo = lineNo
        self.inheritance = inheritance

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def addChild(self, child):
        self.children.append(child)

    def addVariable(self, variable):
        self.variables.append(variable)

    def printNode(self):
        print (self.name)
        for currentMethod in self.children:
            currentMethod.printNode()
        print ("}")

    def toString(self):
        print ("I'm a class")
        print ("My parent is: ")

class Attribute:
    def __init__(self, parent, name, scope, dataType, value = ""):
        self.parent = parent
        self.name = name
        self.scope = scope
        self.value = value
        self.type = dataType

    def getName(self):
        return self.name

    def printNode(slef):
        if self.value is "":
            print (self.scope + self.type + self.name + ";")
        else:
            print (self.scope + self.type + self.name + " = " + self.value + ";")
