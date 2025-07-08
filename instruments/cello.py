import numpy as np


def cello(frequency=220, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = 0.7 * (2 * (t * frequency - np.floor(0.5 + t * frequency)))
    attack = int(0.12 * sample_rate)
    release = int(0.25 * sample_rate)
    sustain = n_samples - attack - release
    envelope = np.concatenate(
        [np.linspace(0, 1, attack), np.ones(sustain), np.linspace(1, 0, release)]
    )
    envelope = envelope[:n_samples]
    return wave * envelope
