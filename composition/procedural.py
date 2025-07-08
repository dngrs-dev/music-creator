import random


def random_melody_pattern(length_beats, instr, scale_midis, vol=0, pan=0):
    articulations = ["normal", "staccato", "legato", "vibrato", "slide", "bend"]
    pattern = []
    for b in range(length_beats):
        midi = random.choice(scale_midis)
        articulation = random.choice(articulations)
        pattern.append((b, "melodic", instr, midi, 1, vol, pan, articulation))
    return pattern


def random_chord_pattern(length_bars, instr, scale_midis, time_signature, vol=0, pan=0):
    articulations = ["normal", "staccato", "legato", "vibrato", "slide", "bend"]
    pattern = []
    beats_per_bar = time_signature[0]
    for bar in range(length_bars):
        root = random.choice(scale_midis)
        chord = [root, root + 4, root + 7]
        articulation = random.choice(articulations)
        pattern.append(
            (
                bar * beats_per_bar,
                "chord",
                instr,
                chord,
                beats_per_bar,
                vol,
                pan,
                articulation,
            )
        )
    return pattern


def random_drum_pattern(length_beats, drum_types=None):
    if drum_types is None:
        drum_types = ["kick", "snare", "hihat"]
    pattern = []
    for b in range(length_beats):
        for drum in drum_types:
            if random.random() < (0.5 if drum == "hihat" else 0.3):
                velocity = random.uniform(-6, 2)
                pan = random.uniform(-0.2, 0.2)
                pattern.append((b, "drum", drum, None, 1, velocity, pan))
    return pattern
