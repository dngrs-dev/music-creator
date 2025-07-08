import numpy as np


def flute(frequency=523.25, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    sine = 0.8 * np.sin(2 * np.pi * frequency * t)
    noise = 0.2 * np.random.normal(0, 1, n_samples)
    attack = int(0.08 * sample_rate)
    release = int(0.2 * sample_rate)
    sustain = n_samples - attack - release
    envelope = np.concatenate(
        [np.linspace(0, 1, attack), np.ones(sustain), np.linspace(1, 0, release)]
    )
    envelope = envelope[:n_samples]
    return (sine + noise) * envelope
