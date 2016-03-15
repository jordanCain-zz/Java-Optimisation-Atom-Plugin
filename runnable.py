import sys
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\OptimisationDetect')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\Gui')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser')
import parse
import scan
from debugUtil import Trace
import walker

#Debug levels:
#0 Dev trace        - produces extra log info in areas being written
#1 User trace       - Produces logging info to a UserTrace.txt file
#2 Service Trace    - Produces a stackTrace in StackTrace.txts
debugLevel = 1

#Run the parse and detect
def run():
    debug = Trace(debugLevel)
    if debugLevel >= 1:
        debug.writeTrace()
    #Check if command line call or not
    if len(sys.argv) > 1:
        fname = sys.argv[1]     #File to analyse is passed as the first argument
    else:
        fname = r"C:\Users\jordan\Documents\GitHub\javaParser\SampleJavaFiles\HelloWorld.java"
    parent = parse.read(fname, debug)
    walker.getNodeCount(parent)
    parse.printTree(parent)
    #recursions, loops = scan.detect(parent, debug)
    #scan.output(recursions, loops)

run()
