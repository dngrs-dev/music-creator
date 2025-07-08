import numpy as np


def saxophone(frequency=415.3, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = (
        0.5 * np.sin(2 * np.pi * frequency * t)
        + 0.3 * np.sin(2 * np.pi * frequency * 2 * t)
        + 0.2 * np.sin(2 * np.pi * frequency * 4 * t)
    )
    attack = int(0.04 * sample_rate)
    release = int(0.18 * sample_rate)
    sustain = n_samples - attack - release
    envelope = np.concatenate(
        [np.linspace(0, 1, attack), np.ones(sustain), np.linspace(1, 0, release)]
    )
    envelope = envelope[:n_samples]
    return wave * envelope
