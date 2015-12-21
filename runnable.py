import sys
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\ASTParser')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\OptimisationDetect')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser\Gui')
sys.path.insert(0, r'C:\Users\Jordan\Documents\GitHub\javaParser')
import parse
import scan
import debugUtil

#Debug levels:
#0 Dev trace        - produces extra log info in areas being written
#1 User trace       - produces extra logging info
#2 Service Trace    - Produces a stackTrace
debugLevel = 0

#Run the parse and detect
def run():
    if debugLevel == 2:
        debugUtil.stackTrace()
    parent = parse.read(debugLevel)
    optimisations = scan.detect(parent, debugLevel)
    scan.output(optimisations)

run()
