# App style file for Chordnation, by .Lx
# Organizes and stores various styles for Chordnation

import xml.etree.ElementTree as ET

class theme:
    """ The class responsible for saving the current theme's colors and fonts """
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

    def set_aux(self, theme):
        """Given an xml root with the theme, sets every variable.
            Returns False if something is not set or has invalid values"""


        # Checks if every attribute in the theme is legit by checking against correct attribute list
        listOfAttribs = ["maincolor","accentcolor","sheetcolor","todocolor","donecolor","challangetextcolor","optionstextcolor",
                                    "unpressedwhitekeycolor","pressedwhitekeycolor","unpressedblackkeycolor","pressedblackkeycolor",
                                    "challangefont","optionsfont","signaturefont"]
        listOfThemeAttribs = []
        for element in theme:
            listOfThemeAttribs.append(element.tag)
        
        if(listOfAttribs != listOfThemeAttribs):
            print("Invalid theme given")
            return False

        else:
            #If every attribute is legit, sets it in the theme
            self.theme = theme.get("name")
            
            self.maincolor = theme.find('maincolor').text                 
            self.accentcolor = theme.find('accentcolor').text 
            self.sheetcolor = theme.find('sheetcolor').text
            self.todocolor = theme.find('todocolor').text 
            self.donecolor = theme.find('donecolor').text
            self.challangetextcolor = theme.find('challangetextcolor').text  
            self.optionstextcolor = theme.find('optionstextcolor').text         

            self.unpressedwhitekeycolor = theme.find('unpressedwhitekeycolor').text
            self.pressedwhitekeycolor = theme.find('pressedwhitekeycolor').text
            self.unpressedblackkeycolor = theme.find('unpressedblackkeycolor').text
            self.pressedblackkeycolor = theme.find('pressedblackkeycolor').text

            self.challangefont = theme.find('challangefont').text
            self.optionsfont = theme.find('optionsfont').text
            self.signaturefont = theme.find('signaturefont').text
            print(self.theme,"theme applied")
            return True


    def set_via_file(self, file):
        """ Given a xml file that is well structured, changes the theme to the given file's themes """
        
        root = ET.parse(file).getroot()

        theme = root.findall('theme')[0]
        
        print("Setting theme")

        if(not self.set_aux(theme)):
            print("Theme not found")

    def set_via_theme_name(self, theme_name):
        """ Given a theme name, goes to the default theme files and sets the theme"""

        root = ET.parse('themes.xml').getroot()

        for theme in root.findall('theme'):

            #If a theme with the given theme name is found, tries to apply it
            if(theme.get('name') == theme_name):
                print("Setting theme")
                if(self.set_aux(theme)):
                    return

        print("Theme not found")
