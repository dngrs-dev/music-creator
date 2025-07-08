import numpy as np


def piano(frequency=261.63, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    sound = (
        0.5 * np.sin(2 * np.pi * frequency * t)
        + 0.2 * np.sin(2 * np.pi * frequency * 2 * t + 0.01)
        + 0.15 * np.sin(2 * np.pi * frequency * 3 * t - 0.02)
        + 0.1 * np.sin(2 * np.pi * frequency * 4 * t + 0.03)
        + 0.05 * np.sin(2 * np.pi * frequency * 5 * t)
    )
    attack = int(0.005 * sample_rate)
    decay_len = int(0.08 * sample_rate)
    sustain_len = n_samples - attack - decay_len - int(0.2 * sample_rate)
    sustain_level = 0.5
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
