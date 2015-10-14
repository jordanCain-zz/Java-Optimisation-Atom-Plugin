from packageHolder import Package
from classHolder import Class
from methodHolder import Method

javaString = 'package helloworld;\n\npublic class HelloWorld {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello World");\n\t}\n}'
#print (javaString)

newPackage = Package("package")
print ("Get name of package: " + newPackage.getName())

newClass = Class("class", newPackage)
print ("Get name of class: " + newClass.getName())
print ("Get parent of class: " + newClass.getParent().getName())

newMethod = Method("method", newClass, "void")
print ("Get name of method: " + newMethod.getName())
print ("Get parent of method: " + newMethod.getParent().getName())
print ("Get parent of parent method: " + newMethod.getParent().getParent().getName())
