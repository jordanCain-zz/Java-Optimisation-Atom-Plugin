README.txt

Pre reqs:
  Atom text editor installed
  Python 3 installed

Installation:
  Windows:
    Run install.bat,
      This will create a package link for Atom
      Add the file path of the python application to the PATH environment variables
      Note, the environment variable is added to the windows user environment variable permanently
  Other (Linux):
    Navigate to \javaParser\Plugin\test-pack in a console
    Run apm link
    Add \javaParser to path E.g: export PATH=$PATH:/path/to/javaParser
    Note, this is not a permanent solution, the path will remain only in that console and will need to be reset every time you need to launch atom
    *To make the path permanent add it to ~/.profile file

Running:
  Windows:
    Launch atom
    Open a Java file
    Run plugin, from menu or keyboard shortcut ctrl-alt-1
  Other (Linux):
    From within the install console launch atom
    Open a Java file
    Run plugin, from menu or keyboard shortcut ctrl-alt-1
