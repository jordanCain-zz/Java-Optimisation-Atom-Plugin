class Package:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.imports = []

    def getName(self):
        return self.name

    def addChild(self, child):
        self.children.append(child)

    def addImport(self, importIn):
        self.imports.append(importIn)

    def toString(self):
        print ("I'm a package with name: ", self.name)

    def printNode(self):
        print (self.name,"\n")
        for currentImport in self.imports:
            print ("import ",currentImport)
        for currentClass in self.children:
            currentClass.printNode()
