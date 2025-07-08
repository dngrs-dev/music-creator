import numpy as np


def marimba(frequency=440, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = (
        0.6 * np.sin(2 * np.pi * frequency * t)
        + 0.3 * np.sin(2 * np.pi * frequency * 4 * t)
        + 0.1 * np.sin(2 * np.pi * frequency * 10 * t)
    )
    envelope = np.exp(-6 * t)
    return wave * envelope
