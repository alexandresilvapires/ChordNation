# .ui to .py util for Chordnation, by .Lx
# Gets a .ui file from Qt, transforms it into a .py, and replaces color codes with themes.

import os

# Windows
#inputpath = '.\\resources\mainWindow.ui'
#tempinputpath =".\\resources\mainWindowTemp.py"
#outputpath = ".\\mainWindow.py"
#newfuncpath = ".\\newFunctionsUI.txt"


# Linux
inputpath = './resources/mainWindow.ui'
tempinputpath ="./resources/mainWindowTemp.py"
outputpath = "./mainWindow.py"
newfuncpath = "./newFunctionsUI.txt"


# Dictionary that contains every word that needs to be replaced, and what value it needs
toreplace = {"def setupUi(self, mainWindow):":"def setupUi(self, mainWindow, theme):\n        self.chordview = True",
            'rgb(111, 111, 111)"':'"+theme.maincolor',
            'rgb(255, 255, 255)"':'"+theme.unpressedwhitekeycolor',
            'rgb(4,4,4)"':'"+theme.unpressedblackkeycolor',
            'rgb(235, 235, 235)"':'"+theme.sheetcolor',
            'rgb(63, 63, 63)"':'"+theme.challangetextcolor',
            'rgb(255, 0, 0)"':'"+theme.todocolor',
            'rgb(0, 255, 0)"':'"+theme.donecolor',
            'rgb(56, 56, 56)"':'"+theme.accentcolor',
            'rgb(214, 214, 214)"':'"+theme.optionstextcolor',
            'rgb(140, 140, 140)"':'"+theme.accentcolor'}

# Converts .ui to .py
os.system(f"python -m PyQt5.uic.pyuic "+ inputpath +" -o " + tempinputpath)

# Replaces every string matched in toreplace with its replacement

input = open(tempinputpath, "rt")

output = open(outputpath, "wt")

for line in input:
    newLine = "batata"

    #Searches for first word to replace, breaks if it finds it and adds it to new file
    for wordtoreplace in toreplace:
        newLine = line.replace(wordtoreplace, toreplace[wordtoreplace])

        if(newLine != line):
            break

    output.write(newLine)

# Adds new functions to mainWindow.py

toadd = open(newfuncpath, "rt")

for line in toadd:
    output.write(line)

# Close files
output.close()
input.close()
toadd.close()

# Deletes temp file
os.remove(tempinputpath)

