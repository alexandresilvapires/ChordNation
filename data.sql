/*  ChordNation DB Basic Data by .Lx
    ****************************
*/

-- Scales
insert into scale values ('Major', '["T","T","t","T","T","T","t"]');
insert into scale values ('Minor', '["T","t","T","T","t","T","T"]');
insert into scale values ('Harmonic Minor', '["T","t","T","T","t","Tt","t"]');
insert into scale values ('Melodic Minor', '["T","t","T","T","T","T","t"]');
insert into scale values ('Whole-Tone', '["T","T","T","T","T","T"]');
insert into scale values ('Gypsy', '["T","t","Tt","t","t","T","T"]');


-- Chords (Ver forma de fazer extensions)
insert into chord values ("Major", "", '["3M","5p"]');
insert into chord values ("Augmented", "aug",'["3M","5a"]');
insert into chord values ("Minor", "m",'["3m","5p"]');
insert into chord values ("Diminished", "o", '["3m","5d"]');
insert into chord values ("Dominant", "7", '["3M","5p","7m"]');
insert into chord values ("Major7", "maj7", '["3M","5p","7M"]');
insert into chord values ("Augmented7", "aug7", '["3M","5a","7m"]');
insert into chord values ("Minor7", "m7", '["3m","5p","7m"]');
insert into chord values ("Minor-Major", "mM7", '["3m","5p","7M"]');
insert into chord values ("Diminished7", "o7", '["3m","5d","7d"]');
insert into chord values ("Half-Diminished7", "ø7", '["3m","5d","7m"]');
insert into chord values ("Major6", "6", '["3M","5p","6M"]');
insert into chord values ("Minor6", "m6", '["3m","5p","6M"]');
insert into chord values ("Sus2", "sus2", '["2M","5p"]');
insert into chord values ("Sus4", "sus4", '["4p","5p"]');
insert into chord values ("JazzSus", "9sus4", '["4p","5p","7m","9M"]');
/*TODO EXTENSIONS*/


-- Progressions
insert into progression values("Perfect Cadence");
insert into progression values("2-5-1");
insert into progression values("Plagal Cadence");

-- ProgContains
insert into progcontains values ("Perfect Cadence", 1, "I", "Major7");
insert into progcontains values ("Perfect Cadence", 2, "IV", "Major7");
insert into progcontains values ("Perfect Cadence", 3, "V", "Dominant");
insert into progcontains values ("Perfect Cadence", 4, "I", "Major7");

insert into progcontains values ("2-5-1", 1, "II", "Minor7");
insert into progcontains values ("2-5-1", 2, "V", "Dominant");
insert into progcontains values ("2-5-1", 3, "I", "Major7");

insert into progcontains values ("Plagal Cadence", 1, "IV", "Major7");
insert into progcontains values ("Plagal Cadence", 2, "I", "Major7");