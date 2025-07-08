SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "pentatonic": [0, 2, 4, 7, 9],
    "blues": [0, 3, 5, 6, 7, 10],
}

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_name_to_midi(note):
    name = note[:-1]
    octave = int(note[-1])
    return NOTE_NAMES.index(name) + 12 * (octave + 1)


def midi_to_freq(midi):
    return 440.0 * (2 ** ((midi - 69) / 12))


def get_scale_notes(root, scale, octaves=(4, 5)):
    root_idx = NOTE_NAMES.index(root)
    notes = []
    for octv in range(octaves[0], octaves[1] + 1):
        for interval in SCALES[scale]:
            midi = root_idx + interval + 12 * (octv + 1)
            notes.append(midi)
    return notes
