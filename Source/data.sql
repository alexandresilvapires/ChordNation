/*  ChordNation DB Basic Data by .Lx
    ****************************
*/

-- Scales
insert into scale(s_name,tones) values ('Major', '['T','T','t','T','T','T','t']');
insert into scale(s_name,tones) values ('Minor', '['T','t','T','T','t','T','T']');
insert into scale(s_name,tones) values ('Harmonic Minor', '['T','t','T','T','t','Tt','t']');
insert into scale(s_name,tones) values ('Melodic Minor', '['T','t','T','T','T','T','t']');
insert into scale(s_name,tones) values ('Whole-Tone', '['T','T','T','T','T','T']');
insert into scale(s_name,tones) values ('Gypsy', '['T','t','Tt','t','t','T','T']');


-- Chords (Ver forma de fazer extensions)
insert into chord(c_name,c_symbol, intervals) values ('Major', ' ', '["3M","5p"]');
insert into chord(c_name,c_symbol, intervals) values ('Augmented', 'aug','["3M","5a"]');
insert into chord(c_name,c_symbol, intervals) values ('Minor', 'm','["3m","5p"]');
insert into chord(c_name,c_symbol, intervals) values ('Diminished', 'o', '["3m","5d"]');
insert into chord(c_name,c_symbol, intervals) values ('Dominant', '7', '["3M","5p","7m"]');
insert into chord(c_name,c_symbol, intervals) values ('Major7', 'maj7', '["3M","5p","7M"]');
insert into chord(c_name,c_symbol, intervals) values ('Augmented7', 'aug7', '["3M","5a","7m"]');
insert into chord(c_name,c_symbol, intervals) values ('Minor7', 'm7', '["3m","5p","7m"]');
insert into chord(c_name,c_symbol, intervals) values ('Minor-Major', 'mM7', '["3m","5p","7M"]');
insert into chord(c_name,c_symbol, intervals) values ('Diminished7', 'o7', '["3m","5d","7d"]');
insert into chord(c_name,c_symbol, intervals) values ('Half-Diminished7', 'ø7', '["3m","5d","7m"]');
insert into chord(c_name,c_symbol, intervals) values ('Major6', '6', '["3M","5p","6M"]');
insert into chord(c_name,c_symbol, intervals) values ('Minor6', 'm6', '["3m","5p","6M"]');
insert into chord(c_name,c_symbol, intervals) values ('Sus2', 'sus2', '["2M","5p"]');
insert into chord(c_name,c_symbol, intervals) values ('Sus4', 'sus4', '["4p","5p"]');
insert into chord(c_name,c_symbol, intervals) values ('JazzSus', '9sus4', '["p","5p","7m","9M"]');
/*TODO EXTENSIONS*/


-- Progressions
insert into progression(p_name) values('Perfect Cadence');
insert into progression(p_name) values('2-5-1');
insert into progression(p_name) values('Plagal Cadence');

-- ProgContains
insert into progcontains(p_name, position, degree, c_name) values ('Perfect Cadence', 1, 'I', 'Major7');
insert into progcontains(p_name, position, degree, c_name) values ('Perfect Cadence', 2, 'IV', 'Major7');
insert into progcontains(p_name, position, degree, c_name) values ('Perfect Cadence', 3, 'V', 'Dominant');
insert into progcontains(p_name, position, degree, c_name) values ('Perfect Cadence', 4, 'I', 'Major7');
insert into progcontains(p_name, position, degree, c_name) values ('2-5-1', 1, 'II', 'Minor7');
insert into progcontains(p_name, position, degree, c_name) values ('2-5-1', 2, 'V', 'Dominant');
insert into progcontains(p_name, position, degree, c_name) values ('2-5-1', 3, 'I', 'Major7');
insert into progcontains(p_name, position, degree, c_name) values ('Plagal Cadence', 1, 'IV', 'Major7');
insert into progcontains(p_name, position, degree, c_name) values ('Plagal Cadence', 2, 'I', 'Major7');