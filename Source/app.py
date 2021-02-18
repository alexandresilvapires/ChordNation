#!/usr/bin/python3
# Main app file for Chordnation, by .Lx
# Handles communication between GUI and Database, and handles MIDI input

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

## Libs postgres
import psycopg2
import psycopg2.extras

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QThread
from PyQt5.QtGui import QFont

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
# Database Communication
# ------------------------

app = Flask(__name__)

## SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="-" 
DB_DATABASE=DB_USER
DB_PASSWORD="-"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

def makequery(query):
    """ Given a query, executes it in the database, seperating each obtained value in lists with resultspace size"""
    dbConn=None
    cursor=None
    try:
        # Connects to the database
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

        #Executes query
        cursor.execute(query)

        #Turns it into a list
        results = []
        for r in cursor:
            results.append(r)

        return results

    except Exception as e:
        return str(e) 
    finally:
        cursor.close()
        dbConn.close()


# ------------------------
# MIDI-Handler
# ------------------------

def setup_midi_connection(port):
    """ Sets up midi connection by enabling port given, returns midiin class"""
    
    midiin = rtmidi.MidiIn()

    #Checks if port number is legit
    if(midiin.get_port_count() < port-1 or port < 0):
        raise ValueError("\nPort Number invalid\n")
    
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

    #Writes first 3 chords in window (symbol or chord)
    for i in range(0,max(len(progression),3)):
        if(window.chordview):
            #Chord symbol is done by first note and the chord symbol
            window.setChordText(ct, progression[i][2][0]+progression[i][1],progression[i][2], i)
    
        else:
            #Chord symbol is done by chord number and the chord symbol
            window.setChordText(ct, progression[i][0]+progression[i][1],progression[i][2], i)

    #For each chord, highlights message, and makes midi recognition
    for i in range(0,len(progression)):

        #Highlight chord in site
        print("Current chord: ", progression[i][2])

        window.setChordTodo(ct, i%3)

        #Make player play chord
        objective = music.chord_to_note_1_12(progression[i][2], True)
        play_chord(midiin, window, ct, objective)

        window.setChordDone(ct, i % 3)

    print("Success!")

def challange_generator(midiin, window, ct, progs, scales):
    """ Given a list of possible progressions (name, progression), plays a random progression in a random key"""


    # Picks a random progression, scale and key, and makes the progression
    prog = random.choice(progs)
    scale = random.choice(scales)
    key = random.choice(['C','C#','Db','D','D#','Eb','E','F','F#','Gb','G','G#','Ab','A','A#','B'])

    #Prog[0] contains the prog name and prog[1] the progression details
    progression = music.make_progression(key, scale, prog[1])

    print(prog[0], "in the key of",key)
    window.setKeyText(key)
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
        #self.wait()
        pass
    
    def run(self):
        """ Handles the full program after main window creation, handling MIDI setup and calling exercice generation """

        time.sleep(1)       #Used to give time for the UI to load

        # Sets up MIDI
        midiin = setup_midi_connection(1)

        # Starts exercise (still temporary)

        #TODO: get stuff from database
        MajorScale = ['T','T','t','T','T','T','t']

        #When getting the progression from the database, we keep each chord in order of appearence,
        #   composed by: ScaleNote (eg: II), and a list which especifies the chord
        #   as ["ChordSymbol","ListOfIntervalsWhichMakeItUp"].
        #   To use the list of intervals, it needs to be eval'd and separated into (IntervalSize,'quality'), 
        #   which is done next in format_prog_from_database()
        twofiveone = makequery("select degree, c_symbol, intervals from progcontains natural join chord where p_name = '2-5-1' order by position asc;")

        twofiveone = music.format_prog_from_database(twofiveone)
        print(twofiveone)

        
        challange_generator(midiin, self.ct,self.win, (("ii-V-I",twofiveone),("ii-V-I",twofiveone)), (MajorScale, MajorScale))

        challange_generator(midiin, self.ct,self.win, (("ii-V-I",twofiveone),("ii-V-I",twofiveone)), (MajorScale, MajorScale))


# ------------------------
# GUI Handling
# ------------------------

ct = styles.theme()
ct.set_via_theme_name("Royal")



def startup():
    """ Generates the main program window and runs main program"""

    guiapp = QApplication(sys.argv)
    mainWin = QtWidgets.QMainWindow()
    win = mainWindow.Ui_mainWindow()
    win.setupUi(mainWin, ct)
    mainWin.show()

    # Runs main program code in a thread
    challageGen = challangeThread(win, ct)
    challageGen.start()

    #Starts GUI
    sys.exit(guiapp.exec_())


# ------------------------
# Function Calls
# ------------------------

startup()
