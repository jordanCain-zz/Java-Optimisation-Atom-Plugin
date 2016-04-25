# Author: Jordan Cain, 2015-16

import sys
baseDir = sys.path[0]
sys.path.insert(0, baseDir + r'\ASTParser')
sys.path.insert(0, baseDir + r'\OptimisationDetect')
sys.path.insert(0, baseDir + r'\ASTWalker')
import parse
import scan
from debugUtil import Trace
import walker

#Debug levels:
#0 Dev trace        - produces extra log info in areas being written
#1 User trace       - Produces logging info to a UserTrace.txt file
#2 Service Trace    - Produces a stackTrace in StackTrace.txts
debugLevel = 0

#Run the parse and detect
def run():
    debug = Trace(debugLevel)
    if debugLevel >= 1:
        debug.writeTrace()
    #Check if command line call or not
    if len(sys.argv) > 1:
        fname = sys.argv[1]     #File to analyse is passed as the first argument
    else:
        #Backup file for testing purposes
        fname = r"C:\Users\jordan\Documents\GitHub\javaParser\SampleJavaFiles\ToThePowerOf.java"
    parent = parse.read(fname, debug)
    #walker.getNodeCount(parent)
    #parse.printTree(parent)
    recursions, loops = scan.detect(parent, debug)
    scan.output(recursions, loops)

run()
