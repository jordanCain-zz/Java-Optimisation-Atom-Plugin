import inspect

class Trace():
    def __init__(self, debug):
        self.debugLevel = debug
        if debug >= 1:
            print ("Initialising User Trace")
            userFile = open('UserTrace.txt', 'w+')
            self.userFile = userFile
            self.userFile.write("User Trace \n")
        if debug >= 2:
            print ("Initialising Stack Trace")
            stackFile = open('StackTrace.txt', 'w+')
            self.stackFile = stackFile
            self.stackFile.write("Stack Trace\n")

    def __exit__(self):
        if self.debugLevel >= 1:
            self.userFile.close()
        if self.debugLevel >= 2:
            self.stackFile.close()

    def writeTrace(self, message = ""):
        if self.debugLevel >= 1:
            self.userTrace(message)
        if self.debugLevel >= 2:
            self.stackTrace()

    def userTrace(self, message):
        self.userFile.write(message + "\n")

    def stackTrace(self):
        self.formatStackTrace(len(inspect.stack())-2)
        self.stackFile.write(inspect.stack()[2][3] + " ")
        self.formatStackTrace(len(inspect.stack())-2)
        self.stackFile.write(" " + inspect.stack()[2][1] + " : " + str(inspect.stack()[1][2]-2) + "\n")

    #Allows the method calls to be formatted in a cascading tree
    def formatStackTrace(self,count):
        while count > 0:
            self.stackFile.write("  ")
            count -= 1
