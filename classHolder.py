from packageHolder import Package

class Class:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def addChild(self, child):
        self.children.extend(child)

    def toString(self):
        print ("I'm a class")
        print ("My parent is: ")
