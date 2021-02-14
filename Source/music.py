# Music concepts for Chordnation, by .Lx
# Handles music related concepts like notes, scales, intervals, chords and chord progressions

# ------------------------
# Codification
# ------------------------

#Notes are numbered from 0 (C) to 11 (B)

#Scales are formed by an array of tones, semitones, etc. 
#   Ex: Maj = [T,T,t,T,T,T,t], Minor Blues = [Tt,T,t,t,Tt,T], stored as t=1, T=2, Tt=3

#Intervals are pairs <Interval, quality>, that can be translated into a number of steps
#   Ex: Major 3rd = <3,M>
# M = Major, m = Minor, p = Perfect, a = augmented, d = diminuished

#Chords are defined by either the steps from the 

# ------------------------
# Notes
# ------------------------


def note_format(number: int) -> int:
    """Given a number of a note > 11, sets the number to the correct format between [0,11]"""
    return number % 12

def number_to_note(number) -> int:
    """Given a number, returns a string with the matching note name
        Warning: Does not account scales, so # and b can be wrong in certain contexts"""

    number = note_format(number)

    notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

    return notes[number]

def numbers_to_notes(notes: list) -> list:
    """Given a list of numbers of notes, returns a list with their letter names"""
    array = []

    for note in notes:
        array.append(number_to_note(note))
    return array

def note_to_number(note) -> int:
    """Converts a note to its key code"""

    accidental = 0
    value = 0

    #Cycles every letter in the note name to accept names with multiple accidentals
    for letter in note:
        if(letter == '#'):
            accidental += 1
        elif(letter == 'b' or letter == 'f'):
            accidental -= 1
        
        elif(letter == 'C'):
            value = 0
        elif(letter == 'D'):
            value = 2
        elif(letter == 'E'):
            value = 4
        elif(letter == 'F'):
            value = 5
        elif(letter == 'G'):
            value = 7
        elif(letter == 'A'):
            value = 9
        elif(letter == 'B'):
            value = 11
    
    #Adds the accidentals and makes the note octave independent 
    if(value+accidental > 11):
        value = value+accidental+1
    else:
        value = value+accidental
    
    return note_format(value)

def count_accidentals(note) -> int:
    """ Given a note, returns total number of accidental values. -1 for each flat, +1 for each sharp"""
    
    accidentals = 0
    for letter in note:
        if letter == '#':
            accidentals += 1
        elif letter == 'b':
            accidentals -= 1
    return accidentals

def has_accidental(note, accidental) -> bool:
    """ Given a note, returns true if that note has the given accidental sign"""
    for letter in note:
        if(letter == accidental):
            return True
    return False

def note_without_accidental(note):
    """ Given a note, returns the same note without accidentals """

    newNote = ''
    for letter in note:
        if(letter != 'b' and letter != '#'):
            newNote += letter
    return newNote

def normalize_accidentals(note):
    """ Given a note, normalizes the notes acciddentals to cancel # and b"""

    # Counts accidentals, makes note default letter, then adds remaining accidentals
    accidentals = count_accidentals(note)
    
    newNote = note_without_accidental(note)

    while accidentals != 0:
        if accidentals > 0:
            newNote += '#'
            accidentals -= 1
        else:
            newNote += 'b'
            accidentals += 1
    return newNote

def add_accidental(note, accidental):
    """ Given a note, returns the same note with the given accidental """
    return normalize_accidentals(note+accidental)

def add_accidental_values(note, accidentals):
    """ Given a note, adds the accidentals where each flat is -1, and each sharp is +1 """
    while accidentals != 0:
        if accidentals > 0:
            note += '#'
            accidentals -= 1
        else:
            note += 'b'
            accidentals += 1

    return normalize_accidentals(note)

def get_next_letter(letter):
    """ Given a letter, returns the next letter """
    letter = note_without_accidental(letter)

    letters = ['C','D','E','F','G','A','B']
    for i in range(0,len(letters)):
        if(letter == letters[i]):
            return letters[(i+1)%7]

# ------------------------
# Scales
# ------------------------

def tones_to_numbers(tones: list) -> list:
    """Transforms a given scale in Tones and semitones to nr of steps"""

    n_scale = []

    #for every item in the given scale, checks every letter and adds its value
    for steps in tones:
        value = 0
        for letter in steps:
            if(letter == 't'):
                value += 1
            elif(letter == 'T'):
                value += 2
        n_scale.append(value)

    return n_scale

def scale_to_mode(scale: list, inTones: bool, mode_nr: int) -> list:
    """ Given a scale, either in tones or number of steps, returns the given mode nr's scale
        Ex: Ionian = 0, Dorian = 1, etc"""

    #Normalizes mode_nr
    mode_nr = mode_nr % len(scale)

    if(mode_nr < 0):
        raise ValueError("Mode number must be positive!")

    #Cycles array, creating modes
    while mode_nr > 0:
        newval = scale.pop(0)
        scale.append(newval)
        mode_nr -= 1

    #Converts given input if flag is set
    if(not inTones):
        scale = tones_to_numbers(scale)

    return scale

def make_scale(root, inLetter:bool, scale: list, inTones: bool) -> list:
    """Given a root note and a scale, returns a list of notes that make up that scale.
        If root is a letter (Eg. C#), inLetter is True
        If scale is in tones (Eg. [T,T,t]), inTones is True"""


    #Converts given input if flags are set
    rootN = root 
    if(inLetter):
        rootN = note_to_number(root)
        
    scaleN = scale
    if(inTones):
        scaleN = tones_to_numbers(scale)

    scale_result = [rootN]

    #Checks if the scale is correct: if the total value is 12
    sum = 0
    for elem in scaleN:
        sum += elem
    if(sum != 12):
        raise ValueError("Invalid Scale Given, total sum of steps must equal an octave!")

    #Goes through every element of the scale and gets the notes by adding their value to the past note
    for i in range(0,len(scaleN)-1):
        nextNote = scale_result[i] + scaleN[i]
        nextNote = note_format(nextNote)
        scale_result.append(nextNote)

    return scale_result

def scale_to_notes(scale: list, root) -> list:
    """ Given a list of 7 numbers corresponding to notes, returns the correct nomenclature for their note names based on root"""

    if(len(scale) != 7):
        raise ValueError("Only scales with 7 notes can be converted accurately to numbers")

    #Gets each letter based on root
    newScale = [root]
    for i in range(0,len(scale)-1):
        nextLetter = get_next_letter(note_without_accidental(newScale[i]))

        #Adds accidentals based on the value of the note
        if(note_to_number(nextLetter) < scale[i+1]):
            while(note_to_number(nextLetter) < scale[i+1]):
                nextLetter = add_accidental(nextLetter,'#')

                #Hotfix for a count-to-infinity problem related to B=11, C=0
                if(len(nextLetter) == 5):
                    nextLetter = 'Cb'
                    break
        elif(note_to_number(nextLetter) > scale[i+1]):
            while(note_to_number(nextLetter) > scale[i+1]):
                #Hotfix for a count-to-infinity problem related to B=11, C=0
                nextLetter = add_accidental(nextLetter,'b')
                if(len(nextLetter) == 5):
                    nextLetter = 'B#'
                    break

        newScale.append(nextLetter)

    return newScale

def number_from_scale(scale:list, number) -> int:
    """Given a list of notes, returns the number corresponding to the given number,
        Ex: II from CMaj is D. Used musical notation, not array, so starts from 1"""
    return scale[number-1]

def note_from_scale(scale:list, root, number: int):
    """Given a list of notes, returns the note corresponding to the given number,
        Ex: II from CMaj is D. Used musical notation, not array, so starts from 1"""
    scaleNotes = scale_to_notes(scale, root)
    return scaleNotes[number-1]

def note_from_scale_accidental(scale:list, root, symbol):
    """"Given a list of notes, returns the note corresponding to the given Symbol (I, II, ,, VII),
        Ex: II from CMaj is D. Used musical notation, not array, so starts from II
        Accepts accidentals, like Ib, #I, VIb"""

    number = 0          #To be translated from roman numeral

    # Gets accidentals from symbol
    accidentals = count_accidentals(symbol)

    # Gets number from roman numerals by first removing accidentals, then using value table

    symbol = note_without_accidental(symbol)
    
    if(symbol == 'I'):
        number = 1
    elif(symbol == 'II'):
        number = 2
    elif(symbol == 'III'):
        number = 3
    elif(symbol == 'IV'):
        number = 4
    elif(symbol == 'V'):
        number = 5
    elif(symbol == 'VI'):
        number = 6
    elif(symbol == 'VII'):
        number = 7
    else:
        #Else assumes symbol is a number
        number = int(symbol)
        if(number < 9):
            number = number % 8
        else:
            number = (number % 8) + 1
        

    note = note_from_scale(scale, root, number)

    # With note, adds accidentals to get new note
    
    note = add_accidental_values(note, accidentals)

    return note

# ------------------------
# Intervals
# ------------------------

def sep_interval_pair(interval):
    """ Given a interval in the form "numberQuality", separates it into (number,quality)"""

    numbersTemp = ''
    quality = ''

    for letter in interval:
        if letter in ['0','1','2','3','4','5','6','7','8','9']:
            numbersTemp += letter
        else:
            quality += letter
    print(numbersTemp, quality)
    return (eval(numbersTemp),quality)

def note_from_interval(note, interval: int, quality):
    """ Given a note, an interval [1,15] and a quality (+,-,a,d,p) 
    returns the note that given interval's away from the other"""

    # Checks interval legality
    if(interval > 15 or interval <= 0):
        raise ValueError("Interval size not supported.")

    #Checks if quality is supported
    if(quality == 'p' and interval not in (1,4,5,8,11,12,15)):
        raise ValueError("Perfect quality not applicable to given interval size.")
    
    elif(quality in ('m','M') and interval not in (2,3,6,7,9,10,13,14)):
        raise ValueError("Minor/Major quality not applicable to given interval size.")
    elif(quality in ('d') and interval == 1):
        raise ValueError("Diminished quality not applicable to unisson.")
    

    # Makes scale based on quality
    scale = []
    if(quality in ('p','M','a')):
        scale = make_scale(note, True, ['T','T','t','T','T','T','t'], True)
    else:
        scale = make_scale(note, True, ['T','t','T','T','t','T','T'], True)

    # Gets note based on interval size:
    #   First gets all names of notes from the scale, then gets the index based on the interval size to determine
    #   which note number we want
    #   Then adds accidentals based if it is diminuished or augmented
    types = ['I','II','III','IV','V','VI','VII']
    if(interval == 1):
        index = 0
    elif(interval < 9):
        index = ((interval) % 8) - 1
    else:
        index = ((interval) % 8)

    toGet = types[index]

    if(quality == 'd'):
        toGet = add_accidental(toGet, 'b')
    elif(quality == 'a'):
        toGet = add_accidental(toGet, '#')
    
    #Returns note with the given interval size
    return note_from_scale_accidental(scale, note, toGet)

# ------------------------
# Chords
# ------------------------

def make_chord(root, intervals: list) -> list:
    """ Given a root, a list of intervals [(interval, quality)]
        returns a list of notes that belong in that chord"""

    notes = [root]
    
    #Adds notes from each interval in chord
    for elem in intervals:
        notes.append(note_from_interval(root, elem[0], elem[1]))
    
    return notes

def make_progression(root, scale: list, chords: list) -> list:
    """ Given a scale (in tones), and a list of chords (number of note and chord. Ex: (II,[list to make minor])),
    returns every note of every chord of the progression"""

    resultingChords = []

    #Gets the scale notes
    scale = make_scale(root, True, scale, True)

    #For every note of chord, gets root of chord and makes chord
    for chord in chords:
        chordRoot = note_from_scale_accidental(scale, root, chord[0])

        resultingChords.append(make_chord(chordRoot, chord[1]))

    return resultingChords

def get_needed_numbers_prog(l: list) -> list:
    """ Given a list of list of notes (a chord prog), returns a list with a list
    for every number needed to be pressed for the chord to be correct"""
    result = []

    # Goes throught every note and makes it a number, simply
    for chord in l:
        numbers = []
        for note in chord:
            numbers.append(note_to_number(note))
        result.append(numbers)

    return result

def chord_to_note_1_12(chord, in_notes):
    """ Given a chord (in numbers or notes), returns an array where each entry (0-12)
    is either True or False depending if note is played in chord or not """
    
    ar = [False,False,False,False,False,False,False,False,False,False,False,False]

    for note in chord:

        #Converts note to number if it aint already
        if(in_notes):
            note = note_to_number(note)
        ar[note] = True

    return ar

def format_prog_from_database(prog):
    """ Given a progression from the database, it is formated into a easier-to-work format:
    [['II',"m7", '["3m","5p","7m"]'], ['V',"7", '["3M","5p","7m"]'], ['I',"maj7", '["3M","5p","7M"]']]
    
    Gets turned into:

    [['II', 'm7', [(3, 'm'), (5, 'p'), (7, 'm')]], ['V', '7', [(3, 'M'), (5, 'p'), (7, 'm')]], ['I', 'maj7', [(3, 'M'), (5, 'p'), (7, 'M')]]]
    """
    
    formatedProg = []
    
    for chord in prog:
        newChord = [chord[0], chord[1]]

        intervals = eval(chord[2])
        newIntervals = []
        for i in intervals:
            newIntervals.append(sep_interval_pair(i))

        newChord.append(newIntervals)
        formatedProg.append(newChord)
    print(formatedProg)
    return formatedProg

# ------------------------
# Examples
# ------------------------

"""
#Makes C major scale
Major = ['T','T','t','T','T','T','t']
scale = make_scale("C",True,Major,True)
print(scale_to_notes(scale,"C"))

#Makes mode 1 (dorian) from major 
mode = scale_to_mode(Major, True, 1)
scale2 = make_scale("D",True,mode,True)
print(scale_to_notes(scale2, "D"))

#Gets 2, 5 and 1 notes from major scale
print(note_from_scale(scale,'C',2),note_from_scale(scale,'C',5),note_from_scale(scale,'C',1))

#Gets sharp 5 from major scale
print(note_from_scale_accidental(scale, 'C', 'VIIb'))

#Gets note augmented fifth away from G
print(note_from_interval('G',5,'a'))

#Prints Ab Dominant 7th chord flat 9
print(make_chord('G', [(3,'M'),(5,'p'),(7,'m'),[9,'d']]))

#Prints 2 - 5 b9 - 1 in the key of C Major
a = make_progression('C', Major, [['II',[(3,'m'),(5,'p'),(7,'m')]],
                                    ['V',[(3,'M'),(5,'p'),(7,'m'),(9,'d')]],
                                    ['I',[(3,'M'),(5,'p'),(7,'M')]]])

print(a)

print(get_needed_numbers_prog(a))
"""