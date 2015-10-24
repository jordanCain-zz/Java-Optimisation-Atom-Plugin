class Package:
    def __init__(self, name):
        self.name = name
        self.children = []

    def getName(self):
        return self.name

    def addChild(self, child):
        self.children.extend(child)

    def toString(self):
        print ("I'm a package")
