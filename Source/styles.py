# App style file for Chordnation, by .Lx
# Organizes and stores various styles for Chordnation

import xml.etree.ElementTree as ET

class style:
    def __init__(self):
        self.theme = ""                 #The name of the theme
        
        #Colors
        self.maincolor = ""                 #The program's main color
        self.accentcolor = ""               #The program's accent color
        self.sheetcolor = ""                 #The color of the background where the chords are
        self.todocolor = ""                 #The color of the currently unfinished notes and chord
        self.donecolor = ""                 #The color of correct notes and chords
        self.challangetextcolor = ""        #The color for the chords and notes that are not yet to be played
        self.optionstextcolor = ""          #The option text's color

        #Keyboard customization
        self.unpressedwhitekeycolor = ""    #The color for unpressed white keys
        self.pressedwhitekeycolor = ""      #The color for pressed white keys
        self.unpressedblackkeycolor = ""    #The color for unpressed black keys
        self.pressedblackkeycolor = ""      #The color for pressed black keys

        #Font customization
        self.challangefont = ""             #The font used for the chords and notes
        self.optionsfont = ""               #The font used for the options
        self.signaturefont = ""             #The font used for the signature