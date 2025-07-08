import numpy as np


def choir(frequency=261.63, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = (
        0.4 * np.sin(2 * np.pi * frequency * t)
        + 0.2 * np.sin(2 * np.pi * (frequency * 1.01) * t)
        + 0.2 * np.sin(2 * np.pi * (frequency * 0.99) * t)
        + 0.2 * np.sin(2 * np.pi * (frequency * 2) * t)
    )
    if articulation == "staccato":
        attack = int(0.01 * sample_rate)
        release = int(0.1 * sample_rate)
        sustain = max(0, n_samples - attack - release)
    elif articulation == "legato":
        attack = int(0.2 * sample_rate)
        release = int(0.2 * sample_rate)
        sustain = max(0, n_samples - attack - release)
    else:
        attack = int(0.2 * sample_rate)
        release = int(0.3 * sample_rate)
        sustain = max(0, n_samples - attack - release)
    envelope = np.concatenate(
        [np.linspace(0, 1, attack), np.ones(sustain), np.linspace(1, 0, release)]
    )
    envelope = envelope[:n_samples]
    if articulation == "vibrato":
        vibrato = 0.01 * np.sin(2 * np.pi * 6 * t)
        wave = (
            0.4 * np.sin(2 * np.pi * (frequency + vibrato * frequency) * t)
            + 0.2 * np.sin(2 * np.pi * ((frequency * 1.01) + vibrato * frequency) * t)
            + 0.2 * np.sin(2 * np.pi * ((frequency * 0.99) + vibrato * frequency) * t)
            + 0.2 * np.sin(2 * np.pi * ((frequency * 2) + vibrato * frequency) * t)
        )
    elif articulation == "slide":
        f0 = frequency * 0.7
        f1 = frequency
        freqs = np.linspace(f0, f1, n_samples)
        wave = (
            0.4 * np.sin(2 * np.pi * freqs * t)
            + 0.2 * np.sin(2 * np.pi * (freqs * 1.01) * t)
            + 0.2 * np.sin(2 * np.pi * (freqs * 0.99) * t)
            + 0.2 * np.sin(2 * np.pi * (freqs * 2) * t)
        )
    elif articulation == "bend":
        bend = np.linspace(0, 0.2, n_samples)
        wave = (
            0.4 * np.sin(2 * np.pi * (frequency + bend * frequency) * t)
            + 0.2 * np.sin(2 * np.pi * ((frequency * 1.01) + bend * frequency) * t)
            + 0.2 * np.sin(2 * np.pi * ((frequency * 0.99) + bend * frequency) * t)
            + 0.2 * np.sin(2 * np.pi * ((frequency * 2) + bend * frequency) * t)
        )
    return wave * envelope
