import numpy as np


def french_horn(frequency=220, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t) + 0.2 * np.sin(
        2 * np.pi * frequency * 3 * t
    )
    attack = int(0.08 * sample_rate)
    release = int(0.25 * sample_rate)
    sustain = n_samples - attack - release
    envelope = np.concatenate(
        [np.linspace(0, 1, attack), np.ones(sustain), np.linspace(1, 0, release)]
    )
    envelope = envelope[:n_samples]
    return wave * envelope
