import numpy as np


def violin(frequency=440, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    vibrato = 5 * np.sin(2 * np.pi * 5 * t)
    wave = 0.6 * (2 * (t * frequency - np.floor(0.5 + t * frequency + vibrato / 100)))
    attack = int(0.1 * sample_rate)
    release = int(0.2 * sample_rate)
    sustain = n_samples - attack - release
    envelope = np.concatenate(
        [np.linspace(0, 1, attack), np.ones(sustain), np.linspace(1, 0, release)]
    )
    envelope = envelope[:n_samples]
    return wave * envelope
