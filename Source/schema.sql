/*  ChordNation DB Schema by .Lx
    ****************************
*/


/* Erase existing tables */
DROP TABLE IF EXISTS scale CASCADE;     
DROP TABLE IF EXISTS chord CASCADE;
DROP TABLE IF EXISTS progression CASCADE;
DROP TABLE IF EXISTS progcontains CASCADE;


/* Table creation*/

/* A Scale entry is composed of a name and list of tones (t=semitone, T=tone, Tt = 1.5 Tones, etc)
 *   Ex: <'Major','["T","T","t","T","T","T","t"]'>
 */
CREATE TABLE scale (
    s_name VARCHAR(30),
    tones VARCHAR(30) NOT NULL,

    CONSTRAINT pk_name_scale PRIMARY KEY (s_name)
);


/* A Chord entry is composed of a name, symbol (where X is replaced by the note later) and list of intervals (Interval = 'NumberQuality', Ex: 5p for perfect fifth)
 *   Ex: <'Major7', 'M7' ,["3M","5p","7M"]'>
 */
CREATE TABLE chord (
    c_name VARCHAR(30),
    c_symbol VARCHAR(30) NOT NULL,
    intervals VARCHAR(40) NOT NULL,

    CONSTRAINT pk_name_chord PRIMARY KEY (c_name)
);


/* A Progression entry is composed of a name
 *   Ex: <'ii-V7-I','[("II","Minor7"),("V","Dominant"),("I","Major7")]>
 */
CREATE TABLE progression (
    p_name VARCHAR(30),

    CONSTRAINT pk_name_prog PRIMARY KEY (p_name)
);


/* ProgContains has each chord played in a given progression, in a certain order (given by position)
 *   Ex: <ii-V7-I',1,'II','Minor7'>
 */
CREATE TABLE progcontains (
    p_name VARCHAR(30),
    position INT,
    degree VARCHAR(5),
    c_name VARCHAR(30),

    CONSTRAINT pk_progcontains PRIMARY KEY (p_name,position),

    CONSTRAINT fk_p_name FOREIGN KEY (p_name) REFERENCES progression(p_name) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_c_name FOREIGN KEY (c_name) REFERENCES chord(c_name) ON DELETE CASCADE ON UPDATE CASCADE
);
