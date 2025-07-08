import numpy as np


def bell(frequency=880, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = (
        0.6 * np.sin(2 * np.pi * frequency * t)
        + 0.3 * np.sin(2 * np.pi * frequency * 2.7 * t)
        + 0.2 * np.sin(2 * np.pi * frequency * 5.5 * t)
    )
    envelope = np.exp(-3 * t)
    return wave * envelope
