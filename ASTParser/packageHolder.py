# Author: Jordan Cain, 2015-16

class Package:
    def __init__(self, name, lineNo, debugObj):
        global debug
        debug = debugObj
        debug.writeTrace("Package Constructor")
        self.name = name.rstrip('\n')
        self.children = []
        self.imports = []
        self.lineNo = lineNo

    def getName(self):
        debug.writeTrace("Package GetName")
        return self.name

    def getChildren(self):
        debug.writeTrace("Package Get Children")
        return self.children

    def addChild(self, child):
        debug.writeTrace("Package Add child")
        self.children.append(child)

    def addImport(self, importIn):
        debug.writeTrace("Package Add Import")
        self.imports.append(importIn)

    def toString(self):
        debug.writeTrace("Package toString")
        print ("I'm a package with name: ", self.name)

    def printNode(self):
        debug.writeTrace("Package PrintNode")
        print (self.name,"\n")
        for currentImport in self.imports:
            print ("import ",currentImport)
        for currentClass in self.children:
            currentClass.printNode()
