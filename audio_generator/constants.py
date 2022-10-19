from enum import Enum

TEMP_DIR = "generate_sounds_temp"
OUTPUT_DIR = "audio"
INSTRUCTIONS_FILE = "instructions.txt"

IGNORED_WARNINGS = [
    "are identical (not copied).",
    "rm:",
    "decrease volume?"
]

# when generating all semi-tones this is the number of
# pitching down it must to out of 11 other semi-tones
NUM_PITCH_DOWNS = 7


class ChordPurpose(Enum):
    normal = 0
    pivot = 1


# mode of instrument (chord/scale/arpeggio)
class Mode(Enum):
    chord = 0
    scale = 1
    arpeggio = 2


RANGE_IN_MODE = {
    Mode.chord: 1,
    Mode.scale: 7,
    Mode.arpeggio: 3
}
SCALE_INDEX_IN_MODE = {
    Mode.chord: [],
    Mode.scale: [0, 1, 2, 3, 4, 5, 6],
    Mode.arpeggio: [0, 2, 4]
}


# keys including majors, minors, harmonic and minors
class Key(Enum):
    A_major = 0
    A_sharp_major = 1
    B_major = 2
    C_major = 3
    C_sharp_major = 4
    D_major = 5
    D_sharp_major = 6
    E_major = 7
    F_major = 8
    F_sharp_major = 9
    G_major = 10
    G_sharp_major = 11
    A_minor = 12
    A_sharp_minor = 13
    B_minor = 14
    C_minor = 15
    C_sharp_minor = 16
    D_minor = 17
    D_sharp_minor = 18
    E_minor = 19
    F_minor = 20
    F_sharp_minor = 21
    G_minor = 22
    G_sharp_minor = 23
    A_harmonic_minor = 24
    A_sharp_harmonic_minor = 25
    B_harmonic_minor = 26
    C_harmonic_minor = 27
    C_sharp_harmonic_minor = 28
    D_harmonic_minor = 29
    D_sharp_harmonic_minor = 30
    E_harmonic_minor = 31
    F_harmonic_minor = 32
    F_sharp_harmonic_minor = 33
    G_harmonic_minor = 34
    G_sharp_harmonic_minor = 35


# chords including majors, minors, diminished, 7th majors, 7th minors,
# 7th harmonic minors, 7th diminished
class Chord(Enum):
    # major
    A_major = 0
    A_sharp_major = 1
    B_major = 2
    C_major = 3
    C_sharp_major = 4
    D_major = 5
    D_sharp_major = 6
    E_major = 7
    F_major = 8
    F_sharp_major = 9
    G_major = 10
    G_sharp_major = 11
    # minor
    A_minor = 12
    A_sharp_minor = 13
    B_minor = 14
    C_minor = 15
    C_sharp_minor = 16
    D_minor = 17
    D_sharp_minor = 18
    E_minor = 19
    F_minor = 20
    F_sharp_minor = 21
    G_minor = 22
    G_sharp_minor = 23
    # harmonic minor
    A_harmonic_minor = 24
    A_sharp_harmonic_minor = 25
    B_harmonic_minor = 26
    C_harmonic_minor = 27
    C_sharp_harmonic_minor = 28
    D_harmonic_minor = 29
    D_sharp_harmonic_minor = 30
    E_harmonic_minor = 31
    F_harmonic_minor = 32
    F_sharp_harmonic_minor = 33
    G_harmonic_minor = 34
    G_sharp_harmonic_minor = 35
    # diminished
    A_diminished = 36
    A_sharp_diminished = 37
    B_diminished = 38
    C_diminished = 39
    C_sharp_diminished = 40
    D_diminished = 41
    D_sharp_diminished = 42
    E_diminished = 43
    F_diminished = 44
    F_sharp_diminished = 45
    G_diminished = 46
    G_sharp_diminished = 47
    # major seventh
    A_major_seventh = 48
    A_sharp_major_seventh = 49
    B_major_seventh = 50
    C_major_seventh = 51
    C_sharp_major_seventh = 52
    D_major_seventh = 53
    D_sharp_major_seventh = 54
    E_major_seventh = 55
    F_major_seventh = 56
    F_sharp_major_seventh = 57
    G_major_seventh = 58
    G_sharp_major_seventh = 59
    # minor seventh
    A_minor_seventh = 60
    A_sharp_minor_seventh = 61
    B_minor_seventh = 62
    C_minor_seventh = 63
    C_sharp_minor_seventh = 64
    D_minor_seventh = 65
    D_sharp_minor_seventh = 66
    E_minor_seventh = 67
    F_minor_seventh = 68
    F_sharp_minor_seventh = 69
    G_minor_seventh = 70
    G_sharp_minor_seventh = 71
    # harmonic minor seventh
    A_harmonic_minor_seventh = 72
    A_sharp_harmonic_minor_seventh = 73
    B_harmonic_minor_seventh = 74
    C_harmonic_minor_seventh = 75
    C_sharp_harmonic_minor_seventh = 76
    D_harmonic_minor_seventh = 77
    D_sharp_harmonic_minor_seventh = 78
    E_harmonic_minor_seventh = 79
    F_harmonic_minor_seventh = 80
    F_sharp_harmonic_minor_seventh = 81
    G_harmonic_minor_seventh = 82
    G_sharp_harmonic_minor_seventh = 83
    # diminished seventh
    A_diminished_seventh = 84
    A_sharp_diminished_seventh = 85
    B_diminished_seventh = 86
    C_diminished_seventh = 87
    C_sharp_diminished_seventh = 88
    D_diminished_seventh = 89
    D_sharp_diminished_seventh = 90
    E_diminished_seventh = 91
    F_diminished_seventh = 92
    F_sharp_diminished_seventh = 93
    G_diminished_seventh = 94
    G_sharp_diminished_seventh = 95


class ChordClassification(Enum):
    major = 0
    minor = 1
    harmonic_minor = 2
    diminished = 3
    major_seventh = 4
    minor_seventh = 5
    harmonic_minor_seventh = 6
    diminished_seventh = 7


# all 12 semi-tones
class Note(Enum):
    A = 0
    A_sharp = 1
    B = 2
    C = 3
    C_sharp = 4
    D = 5
    D_sharp = 6
    E = 7
    F = 8
    F_sharp = 9
    G = 10
    G_sharp = 11
    none = 12


# stores the notes in the scale of the key
SCALES = {
    # major
    Key.A_major: [Note.A, Note.B, Note.C_sharp, Note.D, Note.E, Note.F_sharp,
                  Note.G_sharp],
    Key.A_sharp_major: [Note.A_sharp, Note.C, Note.D, Note.D_sharp, Note.F,
                        Note.G, Note.A],
    Key.B_major: [Note.B, Note.C_sharp, Note.D_sharp, Note.E, Note.F_sharp,
                  Note.G_sharp, Note.A_sharp],
    Key.C_major: [Note.C, Note.D, Note.E, Note.F, Note.G, Note.A, Note.B],
    Key.C_sharp_major: [Note.C_sharp, Note.D_sharp, Note.F, Note.F_sharp,
                        Note.G_sharp, Note.A_sharp, Note.C],
    Key.D_major: [Note.D, Note.E, Note.F_sharp, Note.G, Note.A, Note.B,
                  Note.C_sharp],
    Key.D_sharp_major: [Note.D_sharp, Note.F, Note.G, Note.G_sharp,
                        Note.A_sharp, Note.C, Note.D],
    Key.E_major: [Note.E, Note.F_sharp, Note.G_sharp, Note.A, Note.B,
                  Note.C_sharp, Note.D_sharp],
    Key.F_major: [Note.F, Note.G, Note.A, Note.A_sharp, Note.C, Note.D, Note.E],
    Key.F_sharp_major: [Note.F_sharp, Note.G_sharp, Note.A_sharp, Note.B,
                        Note.C_sharp, Note.D_sharp, Note.F],
    Key.G_major: [Note.G, Note.A, Note.B, Note.C, Note.D, Note.E, Note.F_sharp],
    Key.G_sharp_major: [Note.G_sharp, Note.A_sharp, Note.C, Note.C_sharp,
                        Note.D_sharp, Note.F, Note.G],
    # minor
    Key.A_minor: [Note.A, Note.B, Note.C, Note.D, Note.E, Note.F, Note.G],
    Key.A_sharp_minor: [Note.A_sharp, Note.C, Note.C_sharp, Note.D_sharp,
                        Note.F, Note.F_sharp, Note.G_sharp],
    Key.B_minor: [Note.B, Note.C_sharp, Note.D, Note.E, Note.F_sharp, Note.G,
                  Note.A],
    Key.C_minor: [Note.C, Note.D, Note.D_sharp, Note.F, Note.G, Note.G_sharp,
                  Note.A_sharp],
    Key.C_sharp_minor: [Note.C_sharp, Note.D_sharp, Note.E, Note.F_sharp,
                        Note.G_sharp, Note.A, Note.B],
    Key.D_minor: [Note.D, Note.E, Note.F, Note.G, Note.A, Note.A_sharp, Note.C],
    Key.D_sharp_minor: [Note.D_sharp, Note.F, Note.F_sharp, Note.G_sharp,
                        Note.A_sharp, Note.B, Note.C_sharp],
    Key.E_minor: [Note.E, Note.F_sharp, Note.G, Note.A, Note.B, Note.C, Note.D],
    Key.F_minor: [Note.F, Note.G, Note.G_sharp, Note.A_sharp, Note.C,
                  Note.C_sharp, Note.D_sharp],
    Key.F_sharp_minor: [Note.F_sharp, Note.G_sharp, Note.A, Note.B,
                        Note.C_sharp, Note.D, Note.E],
    Key.G_minor: [Note.G, Note.A, Note.A_sharp, Note.C, Note.D, Note.D_sharp,
                  Note.F],
    Key.G_sharp_minor: [Note.G_sharp, Note.A_sharp, Note.B, Note.C_sharp,
                        Note.D_sharp, Note.E, Note.F_sharp],
    # harmonic minor
    Key.A_harmonic_minor: [Note.A, Note.B, Note.C, Note.D, Note.E, Note.F_sharp,
                           Note.G_sharp],
    Key.A_sharp_harmonic_minor: [Note.A_sharp, Note.C, Note.C_sharp,
                                 Note.D_sharp, Note.F, Note.G, Note.A],
    Key.B_harmonic_minor: [Note.B, Note.C_sharp, Note.D, Note.E, Note.F_sharp,
                           Note.G_sharp, Note.A_sharp],
    Key.C_harmonic_minor: [Note.C, Note.D, Note.D_sharp, Note.F, Note.G, Note.A,
                           Note.B],
    Key.C_sharp_harmonic_minor: [Note.C_sharp, Note.D_sharp, Note.E,
                                 Note.F_sharp, Note.G_sharp, Note.A_sharp,
                                 Note.C],
    Key.D_harmonic_minor: [Note.D, Note.E, Note.F, Note.G, Note.A, Note.B,
                           Note.C_sharp],
    Key.D_sharp_harmonic_minor: [Note.D_sharp, Note.F, Note.F_sharp,
                                 Note.G_sharp, Note.A_sharp, Note.C, Note.D],
    Key.E_harmonic_minor: [Note.E, Note.F_sharp, Note.G, Note.A, Note.B,
                           Note.C_sharp, Note.D_sharp],
    Key.F_harmonic_minor: [Note.F, Note.G, Note.G_sharp, Note.A_sharp, Note.C,
                           Note.D, Note.E],
    Key.F_sharp_harmonic_minor: [Note.F_sharp, Note.G_sharp, Note.A, Note.B,
                                 Note.C_sharp, Note.D_sharp, Note.F],
    Key.G_harmonic_minor: [Note.G, Note.A, Note.A_sharp, Note.C, Note.D, Note.E,
                           Note.F_sharp],
    Key.G_sharp_harmonic_minor: [Note.G_sharp, Note.A_sharp, Note.B,
                                 Note.C_sharp, Note.D_sharp, Note.F, Note.G]
}
# stores the classification of each chord
CHORD_CLASSIFICATIONS = {
    # major
    Chord.A_major: ChordClassification.major,
    Chord.A_sharp_major: ChordClassification.major,
    Chord.B_major: ChordClassification.major,
    Chord.C_major: ChordClassification.major,
    Chord.C_sharp_major: ChordClassification.major,
    Chord.D_major: ChordClassification.major,
    Chord.D_sharp_major: ChordClassification.major,
    Chord.E_major: ChordClassification.major,
    Chord.F_major: ChordClassification.major,
    Chord.F_sharp_major: ChordClassification.major,
    Chord.G_major: ChordClassification.major,
    Chord.G_sharp_major: ChordClassification.major,
    # minor
    Chord.A_minor: ChordClassification.minor,
    Chord.A_sharp_minor: ChordClassification.minor,
    Chord.B_minor: ChordClassification.minor,
    Chord.C_minor: ChordClassification.minor,
    Chord.C_sharp_minor: ChordClassification.minor,
    Chord.D_minor: ChordClassification.minor,
    Chord.D_sharp_minor: ChordClassification.minor,
    Chord.E_minor: ChordClassification.minor,
    Chord.F_minor: ChordClassification.minor,
    Chord.F_sharp_minor: ChordClassification.minor,
    Chord.G_minor: ChordClassification.minor,
    Chord.G_sharp_minor: ChordClassification.minor,
    # harmonic minor
    Chord.A_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.A_sharp_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.B_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.C_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.C_sharp_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.D_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.D_sharp_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.E_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.F_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.F_sharp_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.G_harmonic_minor: ChordClassification.harmonic_minor,
    Chord.G_sharp_harmonic_minor: ChordClassification.harmonic_minor,
    # diminished
    Chord.A_diminished: ChordClassification.diminished,
    Chord.A_sharp_diminished: ChordClassification.diminished,
    Chord.B_diminished: ChordClassification.diminished,
    Chord.C_diminished: ChordClassification.diminished,
    Chord.C_sharp_diminished: ChordClassification.diminished,
    Chord.D_diminished: ChordClassification.diminished,
    Chord.D_sharp_diminished: ChordClassification.diminished,
    Chord.E_diminished: ChordClassification.diminished,
    Chord.F_diminished: ChordClassification.diminished,
    Chord.F_sharp_diminished: ChordClassification.diminished,
    Chord.G_diminished: ChordClassification.diminished,
    Chord.G_sharp_diminished: ChordClassification.diminished,
    # major seventh
    Chord.A_major_seventh: ChordClassification.major_seventh,
    Chord.A_sharp_major_seventh: ChordClassification.major_seventh,
    Chord.B_major_seventh: ChordClassification.major_seventh,
    Chord.C_major_seventh: ChordClassification.major_seventh,
    Chord.C_sharp_major_seventh: ChordClassification.major_seventh,
    Chord.D_major_seventh: ChordClassification.major_seventh,
    Chord.D_sharp_major_seventh: ChordClassification.major_seventh,
    Chord.E_major_seventh: ChordClassification.major_seventh,
    Chord.F_major_seventh: ChordClassification.major_seventh,
    Chord.F_sharp_major_seventh: ChordClassification.major_seventh,
    Chord.G_major_seventh: ChordClassification.major_seventh,
    Chord.G_sharp_major_seventh: ChordClassification.major_seventh,
    # minor seventh
    Chord.A_minor_seventh: ChordClassification.minor_seventh,
    Chord.A_sharp_minor_seventh: ChordClassification.minor_seventh,
    Chord.B_minor_seventh: ChordClassification.minor_seventh,
    Chord.C_minor_seventh: ChordClassification.minor_seventh,
    Chord.C_sharp_minor_seventh: ChordClassification.minor_seventh,
    Chord.D_minor_seventh: ChordClassification.minor_seventh,
    Chord.D_sharp_minor_seventh: ChordClassification.minor_seventh,
    Chord.E_minor_seventh: ChordClassification.minor_seventh,
    Chord.F_minor_seventh: ChordClassification.minor_seventh,
    Chord.F_sharp_minor_seventh: ChordClassification.minor_seventh,
    Chord.G_minor_seventh: ChordClassification.minor_seventh,
    Chord.G_sharp_minor_seventh: ChordClassification.minor_seventh,
    # harmonic minor seventh
    Chord.A_harmonic_minor_seventh: ChordClassification.harmonic_minor_seventh,
    Chord.A_sharp_harmonic_minor_seventh:
        ChordClassification.harmonic_minor_seventh,
    Chord.B_harmonic_minor_seventh: ChordClassification.harmonic_minor_seventh,
    Chord.C_harmonic_minor_seventh: ChordClassification.harmonic_minor_seventh,
    Chord.C_sharp_harmonic_minor_seventh:
        ChordClassification.harmonic_minor_seventh,
    Chord.D_harmonic_minor_seventh: ChordClassification.harmonic_minor_seventh,
    Chord.D_sharp_harmonic_minor_seventh:
        ChordClassification.harmonic_minor_seventh,
    Chord.E_harmonic_minor_seventh: ChordClassification.harmonic_minor_seventh,
    Chord.F_harmonic_minor_seventh: ChordClassification.harmonic_minor_seventh,
    Chord.F_sharp_harmonic_minor_seventh:
        ChordClassification.harmonic_minor_seventh,
    Chord.G_harmonic_minor_seventh: ChordClassification.harmonic_minor_seventh,
    Chord.G_sharp_harmonic_minor_seventh:
        ChordClassification.harmonic_minor_seventh,
    # diminished seventh
    Chord.A_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.A_sharp_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.B_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.C_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.C_sharp_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.D_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.D_sharp_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.E_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.F_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.F_sharp_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.G_diminished_seventh: ChordClassification.diminished_seventh,
    Chord.G_sharp_diminished_seventh: ChordClassification.diminished_seventh,
}
# stores the notes of each chord in Chords
CHORD_NOTES = {
    # major
    Chord.A_major: [Note.A, Note.C_sharp, Note.E],
    Chord.A_sharp_major: [Note.A_sharp, Note.D, Note.F_sharp],
    Chord.B_major: [Note.B, Note.D_sharp, Note.G],
    Chord.C_major: [Note.C, Note.E, Note.G],
    Chord.C_sharp_major: [Note.C_sharp, Note.F, Note.G_sharp],
    Chord.D_major: [Note.D, Note.F_sharp, Note.A],
    Chord.D_sharp_major: [Note.D_sharp, Note.G, Note.A_sharp],
    Chord.E_major: [Note.E, Note.G_sharp, Note.B],
    Chord.F_major: [Note.F, Note.A, Note.C],
    Chord.F_sharp_major: [Note.F_sharp, Note.A_sharp, Note.C_sharp],
    Chord.G_major: [Note.G, Note.B, Note.D],
    Chord.G_sharp_major: [Note.G_sharp, Note.C, Note.D_sharp],
    # minor
    Chord.A_minor: [Note.A, Note.C, Note.E],
    Chord.A_sharp_minor: [Note.A_sharp, Note.C_sharp, Note.F],
    Chord.B_minor: [Note.B, Note.D, Note.F_sharp],
    Chord.C_minor: [Note.C, Note.D_sharp, Note.G],
    Chord.C_sharp_minor: [Note.C_sharp, Note.E, Note.G_sharp],
    Chord.D_minor: [Note.D, Note.F, Note.A],
    Chord.D_sharp_minor: [Note.D_sharp, Note.F_sharp, Note.A_sharp],
    Chord.E_minor: [Note.E, Note.G, Note.B],
    Chord.F_minor: [Note.F, Note.G_sharp, Note.C],
    Chord.F_sharp_minor: [Note.F_sharp, Note.A, Note.C_sharp],
    Chord.G_minor: [Note.G, Note.A_sharp, Note.D],
    Chord.G_sharp_minor: [Note.G_sharp, Note.B, Note.D_sharp],
    # harmonic minor
    Chord.A_harmonic_minor: [Note.A, Note.C, Note.E],
    Chord.A_sharp_harmonic_minor: [Note.A_sharp, Note.C_sharp, Note.F],
    Chord.B_harmonic_minor: [Note.B, Note.D, Note.F_sharp],
    Chord.C_harmonic_minor: [Note.C, Note.D_sharp, Note.G],
    Chord.C_sharp_harmonic_minor: [Note.C_sharp, Note.E, Note.G_sharp],
    Chord.D_harmonic_minor: [Note.D, Note.F, Note.A],
    Chord.D_sharp_harmonic_minor: [Note.D_sharp, Note.F_sharp, Note.A_sharp],
    Chord.E_harmonic_minor: [Note.E, Note.G, Note.B],
    Chord.F_harmonic_minor: [Note.F, Note.G_sharp, Note.C],
    Chord.F_sharp_harmonic_minor: [Note.F_sharp, Note.A, Note.C_sharp],
    Chord.G_harmonic_minor: [Note.G, Note.A_sharp, Note.D],
    Chord.G_sharp_harmonic_minor: [Note.G_sharp, Note.B, Note.D_sharp],
    # diminished
    Chord.A_diminished: [Note.A, Note.C, Note.D_sharp],
    Chord.A_sharp_diminished: [Note.A_sharp, Note.C_sharp, Note.E],
    Chord.B_diminished: [Note.B, Note.D, Note.F],
    Chord.C_diminished: [Note.C, Note.D_sharp, Note.G],
    Chord.C_sharp_diminished: [Note.C_sharp, Note.E, Note.G_sharp],
    Chord.D_diminished: [Note.D, Note.F, Note.A],
    Chord.D_sharp_diminished: [Note.D_sharp, Note.F_sharp, Note.A_sharp],
    Chord.E_diminished: [Note.E, Note.G, Note.B],
    Chord.F_diminished: [Note.F, Note.G_sharp, Note.C],
    Chord.F_sharp_diminished: [Note.F_sharp, Note.A, Note.C_sharp],
    Chord.G_diminished: [Note.G, Note.A_sharp, Note.D],
    Chord.G_sharp_diminished: [Note.G_sharp, Note.B, Note.D_sharp],
    # major seventh
    Chord.A_major_seventh: [Note.A, Note.C, Note.E, Note.G],
    Chord.A_sharp_major_seventh: [Note.A_sharp, Note.C_sharp, Note.F,
                                  Note.G_sharp],
    Chord.B_major_seventh: [Note.B, Note.D, Note.F_sharp, Note.A],
    Chord.C_major_seventh: [Note.C, Note.D_sharp, Note.G, Note.A_sharp],
    Chord.C_sharp_major_seventh: [Note.C_sharp, Note.E, Note.G_sharp, Note.B],
    Chord.D_major_seventh: [Note.D, Note.F, Note.A, Note.C],
    Chord.D_sharp_major_seventh: [Note.D_sharp, Note.F_sharp, Note.A_sharp,
                                  Note.C_sharp],
    Chord.E_major_seventh: [Note.E, Note.G, Note.B, Note.D],
    Chord.F_major_seventh: [Note.F, Note.G_sharp, Note.C, Note.D_sharp],
    Chord.F_sharp_major_seventh: [Note.F_sharp, Note.A, Note.C_sharp, Note.E],
    Chord.G_major_seventh: [Note.G, Note.A_sharp, Note.D, Note.F],
    Chord.G_sharp_major_seventh: [Note.G_sharp, Note.B, Note.D_sharp,
                                  Note.F_sharp],
    # minor seventh
    Chord.A_minor_seventh: [Note.A, Note.C, Note.E, Note.G],
    Chord.A_sharp_minor_seventh: [Note.A_sharp, Note.C_sharp, Note.F, Note.A],
    Chord.B_minor_seventh: [Note.B, Note.D, Note.F_sharp, Note.A_sharp],
    Chord.C_minor_seventh: [Note.C, Note.D_sharp, Note.G, Note.B],
    Chord.C_sharp_minor_seventh: [Note.C_sharp, Note.E, Note.G_sharp, Note.C],
    Chord.D_minor_seventh: [Note.D, Note.F, Note.A, Note.C],
    Chord.D_sharp_minor_seventh: [Note.D_sharp, Note.F_sharp, Note.A_sharp,
                                  Note.C_sharp],
    Chord.E_minor_seventh: [Note.E, Note.G, Note.B, Note.D],
    Chord.F_minor_seventh: [Note.F, Note.G_sharp, Note.C, Note.D_sharp],
    Chord.F_sharp_minor_seventh: [Note.F_sharp, Note.A, Note.C_sharp, Note.E],
    Chord.G_minor_seventh: [Note.G, Note.A_sharp, Note.D, Note.F],
    Chord.G_sharp_minor_seventh: [Note.G_sharp, Note.B, Note.D_sharp,
                                  Note.F_sharp],
    # harmonic minor seventh
    Chord.A_harmonic_minor_seventh: [Note.A, Note.C, Note.E, Note.G_sharp],
    Chord.A_sharp_harmonic_minor_seventh: [Note.A_sharp, Note.C_sharp, Note.F,
                                           Note.A],
    Chord.B_harmonic_minor_seventh: [Note.B, Note.D, Note.F_sharp,
                                     Note.A_sharp],
    Chord.C_harmonic_minor_seventh: [Note.C, Note.D_sharp, Note.G, Note.B],
    Chord.C_sharp_harmonic_minor_seventh: [Note.C_sharp, Note.E, Note.G_sharp,
                                           Note.C],
    Chord.D_harmonic_minor_seventh: [Note.D, Note.F, Note.A, Note.C_sharp],
    Chord.D_sharp_harmonic_minor_seventh: [Note.D_sharp, Note.F_sharp,
                                           Note.A_sharp, Note.D],
    Chord.E_harmonic_minor_seventh: [Note.E, Note.G, Note.B, Note.D_sharp],
    Chord.F_harmonic_minor_seventh: [Note.F, Note.G_sharp, Note.C, Note.E],
    Chord.F_sharp_harmonic_minor_seventh: [Note.F_sharp, Note.A, Note.C_sharp,
                                           Note.F],
    Chord.G_harmonic_minor_seventh: [Note.G, Note.A_sharp, Note.D,
                                     Note.F_sharp],
    Chord.G_sharp_harmonic_minor_seventh: [Note.G_sharp, Note.B, Note.D_sharp,
                                           Note.G],
    # diminished seventh
    Chord.A_diminished_seventh: [Note.A, Note.C, Note.E, Note.G],
    Chord.A_sharp_diminished_seventh: [Note.A_sharp, Note.C_sharp, Note.F,
                                       Note.A],
    Chord.B_diminished_seventh: [Note.B, Note.D, Note.F_sharp, Note.A_sharp],
    Chord.C_diminished_seventh: [Note.C, Note.D_sharp, Note.G, Note.B],
    Chord.C_sharp_diminished_seventh: [Note.C_sharp, Note.E, Note.G_sharp,
                                       Note.C],
    Chord.D_diminished_seventh: [Note.D, Note.F, Note.A, Note.C],
    Chord.D_sharp_diminished_seventh: [Note.D_sharp, Note.F_sharp, Note.A_sharp,
                                       Note.C_sharp],
    Chord.E_diminished_seventh: [Note.E, Note.G, Note.B, Note.D],
    Chord.F_diminished_seventh: [Note.F, Note.G_sharp, Note.C, Note.D_sharp],
    Chord.F_sharp_diminished_seventh: [Note.F_sharp, Note.A, Note.C_sharp,
                                       Note.E],
    Chord.G_diminished_seventh: [Note.G, Note.A_sharp, Note.D, Note.F],
    Chord.G_sharp_diminished_seventh: [Note.G_sharp, Note.B, Note.D_sharp,
                                       Note.F_sharp],
}
# stores a list of all the chords (including major, major seventh, minor, minor
# seventh, diminishedn and diminished seventh) that can be formed from the notes
# in the key's scale, excluding the root note
KEY_NATIVE_CHORDS = {
    # major
    Key.A_major: [Chord.B_minor, Chord.B_minor_seventh, Chord.C_sharp_minor,
                  Chord.C_sharp_minor_seventh, Chord.D_major,
                  Chord.D_major_seventh, Chord.E_major, Chord.E_major_seventh,
                  Chord.F_sharp_minor, Chord.F_sharp_minor_seventh,
                  Chord.G_sharp_diminished, Chord.G_sharp_diminished_seventh],
    Key.A_sharp_major: [Chord.C_minor, Chord.C_minor_seventh, Chord.D_minor,
                        Chord.D_minor_seventh, Chord.D_sharp_major,
                        Chord.D_sharp_major_seventh, Chord.F_minor,
                        Chord.F_minor_seventh, Chord.G_minor,
                        Chord.G_minor_seventh, Chord.A_diminished,
                        Chord.A_diminished_seventh],
    Key.B_major: [Chord.C_sharp_minor, Chord.C_sharp_minor_seventh,
                  Chord.D_sharp_minor, Chord.D_sharp_minor_seventh,
                  Chord.E_major, Chord.E_major_seventh, Chord.F_sharp_minor,
                  Chord.F_sharp_minor_seventh, Chord.G_sharp_minor,
                  Chord.G_sharp_minor_seventh, Chord.A_sharp_diminished,
                  Chord.A_sharp_diminished_seventh],
    Key.C_major: [Chord.D_minor, Chord.D_minor_seventh, Chord.E_diminished,
                  Chord.E_diminished_seventh, Chord.F_major,
                  Chord.F_major_seventh, Chord.G_major, Chord.G_major_seventh,
                  Chord.A_minor, Chord.A_minor_seventh, Chord.B_diminished,
                  Chord.B_diminished_seventh],
    Key.C_sharp_major: [Chord.D_sharp_minor, Chord.D_sharp_minor_seventh,
                        Chord.F_minor, Chord.F_minor_seventh,
                        Chord.F_sharp_major, Chord.F_sharp_major_seventh,
                        Chord.G_sharp_major, Chord.G_sharp_major_seventh,
                        Chord.A_sharp_minor, Chord.A_sharp_minor_seventh,
                        Chord.C_diminished, Chord.C_diminished_seventh],
    Key.D_major: [Chord.E_minor, Chord.E_minor_seventh, Chord.F_sharp_minor,
                  Chord.F_sharp_minor_seventh, Chord.G_major,
                  Chord.G_major_seventh, Chord.A_major, Chord.A_major_seventh,
                  Chord.B_minor, Chord.B_minor_seventh,
                  Chord.C_sharp_diminished, Chord.C_sharp_diminished_seventh],
    Key.D_sharp_major: [Chord.F_minor, Chord.F_minor_seventh, Chord.G_minor,
                        Chord.G_minor_seventh, Chord.G_sharp_major,
                        Chord.G_sharp_major_seventh, Chord.A_sharp_major,
                        Chord.A_sharp_major_seventh, Chord.C_minor,
                        Chord.C_minor_seventh, Chord.D_diminished,
                        Chord.D_diminished_seventh],
    Key.E_major: [Chord.F_sharp_minor, Chord.F_sharp_minor_seventh,
                  Chord.G_sharp_minor, Chord.G_sharp_minor_seventh,
                  Chord.A_major, Chord.A_major_seventh, Chord.B_major,
                  Chord.B_major_seventh, Chord.C_sharp_minor,
                  Chord.C_sharp_minor_seventh, Chord.D_sharp_diminished,
                  Chord.D_sharp_diminished_seventh],
    Key.F_major: [Chord.G_minor, Chord.G_minor_seventh, Chord.A_diminished,
                  Chord.A_diminished_seventh, Chord.A_sharp_major,
                  Chord.A_sharp_major_seventh, Chord.C_major,
                  Chord.C_major_seventh, Chord.D_minor, Chord.D_minor_seventh,
                  Chord.E_diminished, Chord.E_diminished_seventh],
    Key.F_sharp_major: [Chord.G_sharp_minor, Chord.G_sharp_minor_seventh,
                        Chord.A_sharp_minor, Chord.A_sharp_minor_seventh,
                        Chord.B_major, Chord.B_major_seventh,
                        Chord.C_sharp_major, Chord.C_sharp_major_seventh,
                        Chord.D_sharp_minor, Chord.D_sharp_minor_seventh,
                        Chord.F_diminished, Chord.F_diminished_seventh],
    Key.G_major: [Chord.A_minor, Chord.A_minor_seventh, Chord.B_diminished,
                  Chord.B_diminished_seventh, Chord.C_major,
                  Chord.C_major_seventh, Chord.D_major, Chord.D_major_seventh,
                  Chord.E_minor, Chord.E_minor_seventh,
                  Chord.F_sharp_diminished, Chord.F_sharp_diminished_seventh],
    Key.G_sharp_major: [Chord.A_sharp_minor, Chord.A_sharp_minor_seventh,
                        Chord.C_minor, Chord.C_minor_seventh,
                        Chord.C_sharp_major, Chord.C_sharp_major_seventh,
                        Chord.D_sharp_major, Chord.D_sharp_major_seventh,
                        Chord.F_minor, Chord.F_minor_seventh,
                        Chord.G_diminished, Chord.G_diminished_seventh],
    # minor
    Key.A_minor: [Chord.B_diminished, Chord.B_diminished_seventh, Chord.C_major,
                  Chord.C_major_seventh, Chord.D_minor, Chord.D_minor_seventh,
                  Chord.E_minor, Chord.E_minor_seventh, Chord.F_major,
                  Chord.F_major_seventh, Chord.G_major, Chord.G_major_seventh],
    Key.A_sharp_minor: [Chord.C_diminished, Chord.C_diminished_seventh,
                        Chord.C_sharp_major, Chord.C_sharp_major_seventh,
                        Chord.D_sharp_minor, Chord.D_sharp_minor_seventh,
                        Chord.F_minor, Chord.F_minor_seventh,
                        Chord.F_sharp_major, Chord.F_sharp_major_seventh,
                        Chord.G_sharp_major, Chord.G_sharp_major_seventh],
    Key.B_minor: [Chord.C_sharp_diminished, Chord.C_sharp_diminished_seventh,
                  Chord.D_major, Chord.D_major_seventh, Chord.E_minor,
                  Chord.E_minor_seventh, Chord.F_sharp_minor,
                  Chord.F_sharp_minor_seventh, Chord.G_major,
                  Chord.G_major_seventh, Chord.A_major, Chord.A_major_seventh],
    Key.C_minor: [Chord.D_diminished, Chord.D_diminished_seventh,
                  Chord.D_sharp_major, Chord.D_sharp_major_seventh,
                  Chord.F_minor, Chord.F_minor_seventh, Chord.G_minor,
                  Chord.G_minor_seventh, Chord.G_sharp_major,
                  Chord.G_sharp_major_seventh, Chord.A_sharp_major,
                  Chord.A_sharp_major_seventh],
    Key.C_sharp_minor: [Chord.D_sharp_diminished,
                        Chord.D_sharp_diminished_seventh, Chord.F_major,
                        Chord.F_major_seventh, Chord.F_sharp_minor,
                        Chord.F_sharp_minor_seventh, Chord.G_sharp_minor,
                        Chord.G_sharp_minor_seventh, Chord.A_major,
                        Chord.A_major_seventh, Chord.B_major,
                        Chord.B_major_seventh],
    Key.D_minor: [Chord.E_diminished, Chord.E_diminished_seventh,
                  Chord.F_sharp_major, Chord.F_sharp_major_seventh,
                  Chord.G_minor, Chord.G_minor_seventh, Chord.A_minor,
                  Chord.A_minor_seventh, Chord.A_sharp_major,
                  Chord.A_sharp_major_seventh, Chord.C_major,
                  Chord.C_major_seventh],
    Key.D_sharp_minor: [Chord.F_diminished, Chord.F_diminished_seventh,
                        Chord.G_major, Chord.G_major_seventh,
                        Chord.G_sharp_minor, Chord.G_sharp_minor_seventh,
                        Chord.A_sharp_minor, Chord.A_sharp_minor_seventh,
                        Chord.B_major, Chord.B_major_seventh,
                        Chord.C_sharp_major, Chord.C_sharp_major_seventh],
    Key.E_minor: [Chord.F_sharp_diminished, Chord.F_sharp_diminished_seventh,
                  Chord.G_sharp_major, Chord.G_sharp_major_seventh,
                  Chord.A_minor, Chord.A_minor_seventh, Chord.B_minor,
                  Chord.B_minor_seventh, Chord.C_major, Chord.C_major_seventh,
                  Chord.D_major, Chord.D_major_seventh],
    Key.F_minor: [Chord.G_diminished, Chord.G_diminished_seventh, Chord.A_major,
                  Chord.A_major_seventh, Chord.A_sharp_minor,
                  Chord.A_sharp_minor_seventh, Chord.C_minor,
                  Chord.C_minor_seventh, Chord.C_sharp_major,
                  Chord.C_sharp_major_seventh, Chord.D_sharp_major,
                  Chord.D_sharp_major_seventh],
    Key.F_sharp_minor: [Chord.G_sharp_diminished,
                        Chord.G_sharp_diminished_seventh, Chord.A_sharp_major,
                        Chord.A_sharp_major_seventh, Chord.B_minor,
                        Chord.B_minor_seventh, Chord.C_sharp_minor,
                        Chord.C_sharp_minor_seventh, Chord.D_major,
                        Chord.D_major_seventh, Chord.E_major,
                        Chord.E_major_seventh],
    Key.G_minor: [Chord.A_diminished, Chord.A_diminished_seventh, Chord.B_major,
                  Chord.B_major_seventh, Chord.C_minor, Chord.C_minor_seventh,
                  Chord.D_minor, Chord.D_minor_seventh, Chord.D_sharp_major,
                  Chord.D_sharp_major_seventh, Chord.F_major,
                  Chord.F_major_seventh],
    Key.G_sharp_minor: [Chord.A_sharp_diminished,
                        Chord.A_sharp_diminished_seventh, Chord.C_major,
                        Chord.C_major_seventh, Chord.C_sharp_minor,
                        Chord.C_sharp_minor_seventh, Chord.D_sharp_minor,
                        Chord.D_sharp_minor_seventh, Chord.E_major,
                        Chord.E_major_seventh, Chord.F_sharp_major,
                        Chord.F_sharp_major_seventh],
    # harmonic minor
    Key.A_harmonic_minor: [Chord.B_diminished, Chord.B_diminished_seventh,
                           Chord.D_minor, Chord.D_minor_seventh, Chord.E_major,
                           Chord.E_major_seventh, Chord.F_major,
                           Chord.F_major_seventh, Chord.G_sharp_diminished,
                           Chord.G_sharp_diminished_seventh],
    Key.A_sharp_harmonic_minor: [Chord.C_diminished, Chord.C_diminished_seventh,
                                 Chord.D_sharp_minor,
                                 Chord.D_sharp_minor_seventh, Chord.F_major,
                                 Chord.F_major_seventh, Chord.F_sharp_major,
                                 Chord.F_sharp_major_seventh,
                                 Chord.A_diminished,
                                 Chord.A_diminished_seventh],
    Key.B_harmonic_minor: [Chord.C_sharp_diminished,
                           Chord.C_sharp_diminished_seventh, Chord.E_minor,
                           Chord.E_minor_seventh, Chord.F_sharp_major,
                           Chord.F_sharp_major_seventh, Chord.G_major,
                           Chord.G_major_seventh, Chord.A_sharp_diminished,
                           Chord.A_sharp_diminished_seventh],
    Key.C_harmonic_minor: [Chord.D_diminished, Chord.D_diminished_seventh,
                           Chord.F_minor, Chord.F_minor_seventh, Chord.G_major,
                           Chord.G_major_seventh, Chord.G_sharp_major,
                           Chord.G_sharp_major_seventh, Chord.B_diminished,
                           Chord.B_diminished_seventh],
    Key.C_sharp_harmonic_minor: [Chord.D_sharp_diminished,
                                 Chord.D_sharp_diminished_seventh,
                                 Chord.F_sharp_minor,
                                 Chord.F_sharp_minor_seventh,
                                 Chord.G_sharp_major,
                                 Chord.G_sharp_major_seventh, Chord.A_major,
                                 Chord.A_major_seventh, Chord.C_diminished,
                                 Chord.C_diminished_seventh],
    Key.D_harmonic_minor: [Chord.E_diminished, Chord.E_diminished_seventh,
                           Chord.G_minor, Chord.G_minor_seventh, Chord.A_major,
                           Chord.A_major_seventh, Chord.A_sharp_major,
                           Chord.A_sharp_major_seventh,
                           Chord.C_sharp_diminished,
                           Chord.C_sharp_diminished_seventh],
    Key.D_sharp_harmonic_minor: [Chord.F_diminished, Chord.F_diminished_seventh,
                                 Chord.G_sharp_minor,
                                 Chord.G_sharp_minor_seventh,
                                 Chord.A_sharp_major,
                                 Chord.A_sharp_major_seventh, Chord.B_major,
                                 Chord.B_major_seventh, Chord.D_diminished,
                                 Chord.D_diminished_seventh],
    Key.E_harmonic_minor: [Chord.F_sharp_diminished,
                           Chord.F_sharp_diminished_seventh, Chord.A_minor,
                           Chord.A_minor_seventh, Chord.B_major,
                           Chord.B_major_seventh, Chord.C_major,
                           Chord.C_major_seventh, Chord.D_sharp_diminished,
                           Chord.D_sharp_diminished_seventh],
    Key.F_harmonic_minor: [Chord.G_diminished, Chord.G_diminished_seventh,
                           Chord.A_sharp_minor, Chord.A_sharp_minor_seventh,
                           Chord.C_major, Chord.C_major_seventh,
                           Chord.C_sharp_major, Chord.C_sharp_major_seventh,
                           Chord.E_diminished, Chord.E_diminished_seventh],
    Key.F_sharp_harmonic_minor: [Chord.G_sharp_diminished,
                                 Chord.G_sharp_diminished_seventh,
                                 Chord.B_minor, Chord.B_minor_seventh,
                                 Chord.C_sharp_major,
                                 Chord.C_sharp_major_seventh, Chord.D_major,
                                 Chord.D_major_seventh, Chord.F_diminished,
                                 Chord.F_diminished_seventh],
    Key.G_harmonic_minor: [Chord.A_diminished, Chord.A_diminished_seventh,
                           Chord.C_minor, Chord.C_minor_seventh, Chord.D_major,
                           Chord.D_major_seventh, Chord.D_sharp_major,
                           Chord.D_sharp_major_seventh,
                           Chord.F_sharp_diminished,
                           Chord.F_sharp_diminished_seventh],
    Key.G_sharp_harmonic_minor: [Chord.A_sharp_diminished,
                                 Chord.A_sharp_diminished_seventh,
                                 Chord.C_sharp_minor,
                                 Chord.C_sharp_minor_seventh,
                                 Chord.D_sharp_major,
                                 Chord.D_sharp_major_seventh, Chord.E_major,
                                 Chord.E_major_seventh, Chord.G_diminished,
                                 Chord.G_diminished_seventh],
}

# stores the first chords for each key
KEY_FIRST_CHORDS = {
    # major
    Key.A_major: [Chord.A_major, Chord.A_major_seventh],
    Key.A_sharp_major: [Chord.A_sharp_major, Chord.A_sharp_major_seventh],
    Key.B_major: [Chord.B_major, Chord.B_major_seventh],
    Key.C_major: [Chord.C_major, Chord.C_major_seventh],
    Key.C_sharp_major: [Chord.C_sharp_major, Chord.C_sharp_major_seventh],
    Key.D_major: [Chord.D_major, Chord.D_major_seventh],
    Key.D_sharp_major: [Chord.D_sharp_major, Chord.D_sharp_major_seventh],
    Key.E_major: [Chord.E_major, Chord.E_major_seventh],
    Key.F_major: [Chord.F_major, Chord.F_major_seventh],
    Key.F_sharp_major: [Chord.F_sharp_major, Chord.F_sharp_major_seventh],
    Key.G_major: [Chord.G_major, Chord.G_major_seventh],
    Key.G_sharp_major: [Chord.G_sharp_major, Chord.G_sharp_major_seventh],
    # minor
    Key.A_minor: [Chord.A_minor, Chord.A_minor_seventh],
    Key.A_sharp_minor: [Chord.A_sharp_minor, Chord.A_sharp_minor_seventh],
    Key.B_minor: [Chord.B_minor, Chord.B_minor_seventh],
    Key.C_minor: [Chord.C_minor, Chord.C_minor_seventh],
    Key.C_sharp_minor: [Chord.C_sharp_minor, Chord.C_sharp_minor_seventh],
    Key.D_minor: [Chord.D_minor, Chord.D_minor_seventh],
    Key.D_sharp_minor: [Chord.D_sharp_minor, Chord.D_sharp_minor_seventh],
    Key.E_minor: [Chord.E_minor, Chord.E_minor_seventh],
    Key.F_minor: [Chord.F_minor, Chord.F_minor_seventh],
    Key.F_sharp_minor: [Chord.F_sharp_minor, Chord.F_sharp_minor_seventh],
    Key.G_minor: [Chord.G_minor, Chord.G_minor_seventh],
    Key.G_sharp_minor: [Chord.G_sharp_minor, Chord.G_sharp_minor_seventh],
    # harmonic minor
    Key.A_harmonic_minor: [Chord.A_harmonic_minor,
                           Chord.A_harmonic_minor_seventh],
    Key.A_sharp_harmonic_minor: [Chord.A_sharp_harmonic_minor,
                                 Chord.A_sharp_harmonic_minor_seventh],
    Key.B_harmonic_minor: [Chord.B_harmonic_minor,
                           Chord.B_harmonic_minor_seventh],
    Key.C_harmonic_minor: [Chord.C_harmonic_minor,
                           Chord.C_harmonic_minor_seventh],
    Key.C_sharp_harmonic_minor: [Chord.C_sharp_harmonic_minor,
                                 Chord.C_sharp_harmonic_minor_seventh],
    Key.D_harmonic_minor: [Chord.D_harmonic_minor,
                           Chord.D_harmonic_minor_seventh],
    Key.D_sharp_harmonic_minor: [Chord.D_sharp_harmonic_minor,
                                 Chord.D_sharp_harmonic_minor_seventh],
    Key.E_harmonic_minor: [Chord.E_harmonic_minor,
                           Chord.E_harmonic_minor_seventh],
    Key.F_harmonic_minor: [Chord.F_harmonic_minor,
                           Chord.F_harmonic_minor_seventh],
    Key.F_sharp_harmonic_minor: [Chord.F_sharp_harmonic_minor,
                                 Chord.F_sharp_harmonic_minor_seventh],
    Key.G_harmonic_minor: [Chord.G_harmonic_minor,
                           Chord.G_harmonic_minor_seventh],
    Key.G_sharp_harmonic_minor: [Chord.G_sharp_harmonic_minor,
                                 Chord.G_sharp_harmonic_minor_seventh],
}
