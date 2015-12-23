import sys
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\OptimisationDetect')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\Gui')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser')
import parse
import scan
from debugUtil import Trace

#Debug levels:
#0 Dev trace        - produces extra log info in areas being written
#1 User trace       - Produces logging info to a UserTrace.txt file
#2 Service Trace    - Produces a stackTrace in StackTrace.txts
debugLevel = 2

#Run the parse and detect
def run():
    if debugLevel >= 1:
        debug = Trace(debugLevel)
        debug.writeTrace()
    parent = parse.read(debug)
    parent.printNode()
    optimisations = scan.detect(parent, debug)
    scan.output(optimisations)

run()
