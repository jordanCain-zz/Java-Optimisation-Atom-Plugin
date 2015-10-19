from packageHolder import Package
from classHolder import Class
from methodHolder import Method
from statementHolder import Statement

javaString = 'package helloworld;\n\npublic class HelloWorld {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello World");\n\t}\n}'
#print (javaString)

newPackage = Package("package")
print ("Get name of package: " + newPackage.getName())

newClass = Class("class", newPackage)
print ("Get name of class: " + newClass.getName())
print ("Get parent of class: " + newClass.getParent().getName())

newMethod = Method("method", newClass, "scope", "return type")
print ("Get name of method: " + newMethod.getName())
print ("Get parent of method: " + newMethod.getParent().getName())
print ("Get parent of parent method: " + newMethod.getParent().getParent().getName())

newStatement = Statement("statement", newMethod)
print ("Get name of statement: " + newStatement.getName())
print ("Get parent of statement: " + newStatement.getParent().getName())
print ("Get parent of parent statement: " + newStatement.getParent().getParent().getName())
print ("Get parent of parent of parent statement: " + newStatement.getParent().getParent().getParent().getName())

#SOURCE:: http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python/323259#323259
def decision(word, currentCharPosition):
    return {
        'package': foundPackage("Get the package name here"),
        #TODO:: Class usually preceeded by public/ private
        #Must find way to get around this
        'class': foundClass("Get the class name here"),
        'public': foundMethod("Get the method name here and set scope public"),
        'private': foundMethod("Get the method name here and set scope private"),
    }.get(word, foundStatement("get statement and any params"))

def foundPackage(name):
    print ("found new package")

def foundClass(name):
    print ("Found new class")

def foundMethod(name):
    print ("Found new method")
