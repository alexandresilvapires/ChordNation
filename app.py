# Main app file for Chordnation, by .Lx
# Handles communication between GUI and Database, and handles MIDI input

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QThread
from PyQt5.QtGui import QFont
from PySimpleGUI.PySimpleGUI import TRANSPARENT_BUTTON, theme
import music
import rtmidi
import styles

import random
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import mainWindow

# ------------------------
# MIDI-Handler
# ------------------------

def setup_midi_connection(port):
    """ Sets up midi connection by enabling port given, returns midiin class"""
    
    midiin = rtmidi.MidiIn()

    #Checks if port number is legit
    if(midiin.get_port_count() < port-1 or port < 0):
        raise ValueError("Port Number invalid")
    
    #Enables port
    if(not midiin.is_port_open()):
        print("Enabling MIDI: ", midiin.get_port_name(port))

        midiin.open_port(port)
    return midiin


def convert_midi_message_note_number_status(message) -> int:
    """ Given a midi message, returns the number of the note involved
        in music.py notation (C=0, B=11) and True if it was pressed, or False if released"""

    # Gets number note from message and converts it to music.py notation,
    # Adds status True if sensitivity > 0
    return (message[0][1] % 12, message[0][2] != 0)

def convert_midi_message_to_key_number(message) -> int:
    """ Given a midi message, returns the number of the key corresponding to the note involved """

    # Gets the message that contains the key and changes it to have a 0 where the keys start
    return message[0][1]-21

# ------------------------
# Challange Generation
# ------------------------

def play_chord(midiin, window, ct, objective):
    """ Given an objective array (size 12, where False = note i not needed for chord)
        only stops when the only input notes are the same as objective """
    current = [False,False,False,False,False,False,False,False,False,False,False,False]

    while(current != objective):
        midi_message = midiin.get_message()
        if(midi_message != None):

            #gets note in format (note_number, pressedStatus)
            noteStat = convert_midi_message_note_number_status(midi_message)
            
            #Turns current note in current status array equal to pressedStatus
            current[noteStat[0]] = noteStat[1]

            # Change key in window to theme color
            keynumber = convert_midi_message_to_key_number(midi_message)

            #   To check if a key is white, checks if the pressed note is one of the white keys
            isWhite = noteStat[0] in [0,2,4,5,7,9,11]

            window.changeKey(ct, keynumber, isWhite, noteStat[1])


def play_progression(midiin, window, ct, progression):
    """ Given a chord progression, makes player play each chord """

    #Writes each chord in window


    #For each chord, highlights message, and makes midi recognition
    for chord in progression:

        #Highlight chord in site
        print("Current chord: ", chord)

        #Make player play chord
        objective = music.chord_to_note_1_12(chord, True)
        play_chord(midiin, window, ct, objective)

    print("Success!")

def challange_generator(midiin, window, ct, progs, scales):
    """ Given a list of possible progressions (name, progression), plays a random progression in a random key"""

    # Picks a random progression, scale and key, and makes the progression
    prog = random.choice(progs)
    scale = random.choice(scales)
    key = random.choice(['C','C#','Db','D','D#','Eb','E','F','F#','Gb','G','G#','Ab','A','A#','B'])

    print(prog, scale, key)

    progression = music.make_progression(key, scale, prog[1])

    print(prog[0], "in the key of",key)
    play_progression(midiin, window, ct, progression)

# ------------------------
# Startup
# ------------------------

class challangeThread(QThread):
    def __init__(self, c_theme, window):
        QThread.__init__(self)
        self.ct = c_theme
        self.win = window
    
    def __del__(self):
        self.wait()
    
    def run(self):
        """ Handles the full program after main window creation, handling MIDI setup and calling exercice generation """
        # Sets up MIDI
        midiin = setup_midi_connection(0)

        # Starts exercise (still temporary)

        #TODO: get stuff from database
        MajorScale = ['T','T','t','T','T','T','t']

        #When getting the progression from the database, we keep each chord in order of appearence,
        #   composed by: ScaleNote (eg: II), and a list which especifies the chord
        #   as ["ChordSymbol","ListOfIntervalsWhichMakeItUp"].
        #   To use the list of intervals, it needs to be eval'd and seperated into (IntervalSize,'quality'), 
        #   which is done next

        twofiveone = [['II',"m7", '["3m","5p","7m"]'],
                ['V',"7", '["3M","5p","7m"]'],
                ['I',"maj7", '["3M","5p","7M"]']]

        twofiveone = music.format_prog_from_database(twofiveone)

        # Todo: get new format fixed in challange
        time.sleep(1)
        #challange_generator(midiin, self.ct,self.win, (("ii-V-I",twofiveone),("ii-V-I",twofiveone)), (MajorScale, MajorScale))


# ------------------------
# Database Handling
# ------------------------

# ------------------------
# GUI Handling
# ------------------------

ct = styles.theme()
ct.set_via_theme_name("Incognito")



def startup():
    """ Generates the main program window and runs main program"""

    app = QApplication(sys.argv)
    mainWin = QtWidgets.QMainWindow()
    win = mainWindow.Ui_mainWindow()
    win.setupUi(mainWin, ct)
    mainWin.show()

    # Runs main program code in a thread
    challageGen = challangeThread(win, ct)
    challageGen.start()

    #Starts GUI
    sys.exit(app.exec_())


# ------------------------
# Function Calls
# ------------------------

startup()
