class Package:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.imports = []

    def getName(self):
        return self.name

    def addChild(self, child):
        self.children.extend(child)

    def toString(self):
        print ("I'm a package")

    def addImport(self, importIn):
        self.imports.extend(importIn)
