import inspect

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
