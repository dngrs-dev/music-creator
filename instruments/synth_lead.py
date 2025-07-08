import numpy as np


def synth_lead(frequency=440, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = 0.7 * (2 * (t * frequency - np.floor(0.5 + t * frequency)))
    attack = int(0.01 * sample_rate)
    decay = n_samples - attack
    envelope = np.concatenate([np.linspace(0, 1, attack), np.linspace(1, 0.5, decay)])
    return wave * envelope
