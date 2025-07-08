import numpy as np


def bass(frequency=55, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    sine = 0.7 * np.sin(2 * np.pi * frequency * t)
    sub = 0.2 * np.sin(2 * np.pi * (frequency / 2) * t)
    overtone = 0.1 * np.sin(2 * np.pi * (frequency * 2) * t)
    sound = sine + sub + overtone
    sound = np.tanh(1.5 * sound)
    attack = int(0.01 * sample_rate)
    decay_len = int(0.1 * sample_rate)
    sustain_len = n_samples - attack - decay_len - int(0.2 * sample_rate)
    sustain_level = 0.8
    release = int(0.2 * sample_rate)
    env = np.concatenate(
        [
            np.linspace(0, 1, attack),
            np.linspace(1, sustain_level, decay_len),
            np.ones(max(0, sustain_len)) * sustain_level,
            np.linspace(sustain_level, 0, release),
        ]
    )
    env = env[:n_samples]
    return sound * env
