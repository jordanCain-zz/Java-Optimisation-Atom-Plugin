import sys
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\OptimisationDetect')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\Gui')
import parse
import scan
import inspect

#Debug levels:
#1 User trace - produces extra logging info
#2 Service Trace - Produces a stackTrace
debugLevel = 0

def stackTrace():
    formatStackTrace(len(inspect.stack())-2)
    print (inspect.stack()[1][3] + " ", end="")
    formatStackTrace(len(inspect.stack())-2)
    print (" " + inspect.stack()[1][1] + " : " + str(inspect.stack()[1][2]-2))

#Allows the method calls to be formatted in a cascading tree
def formatStackTrace(count):
    while count > 0:
        print("  ", end="")
        count -= 1

#Run the parse and detect
def run():
    if debugLevel == 2:
        stackTrace()
    parent = parse.read(debugLevel)
    if debugLevel == 2:
        stackTrace()
    scan.detect(parent, debugLevel)

run()
