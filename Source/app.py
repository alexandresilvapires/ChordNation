# Main app file for Chordnation, by .Lx
# Handles communication between GUI and Database, and handles MIDI input

import music
import rtmidi

# MIDI-Handler

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


def play_chord(midiin, objective):
    """ Given an objective array (size 12, where False = note i not needed for chord)
        only stops when the only input notes are the same as objective """
    current = [False,False,False,False,False,False,False,False,False,False,False,False]

    while(current != objective):
        midi_message = midiin.get_message()
        if(midi_message != None):

            #gets note in format (note_number, pressedStatus)
            note = convert_midi_message_note_number_status(midi_message)
            
            #Turns current note in current status array equal to pressedStatus
            current[note[0]] = note[1]

            #TODO: Set notes in keyboard and on screen correctly

def play_progression(midiin, progression):
    """ Given a chord progression, makes player play each chord """

    #For each chord, highlights message, and makes midi recognition
    for chord in progression:

        #Highlight chord in site
        print("Current chord: ", chord)

        #Make player play chord
        objective = music.chord_to_note_1_12(chord, True)
        play_chord(midiin, objective)

    print("Success!")


Major = ['T','T','t','T','T','T','t']
a = music.make_progression('D', Major, [['II',[(3,'m'),(5,'p'),(7,'m')]],
                                    ['V',[(3,'M'),(5,'p'),(7,'m')]],
                                    ['I',[(3,'M'),(5,'p'),(7,'M')]]])

midiin = setup_midi_connection(0)

play_progression(midiin, a)