import numpy as np


def synth_pad(frequency=220, duration=1.0, sample_rate=44100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    wave = 0.5 * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
    attack = int(0.2 * sample_rate)
    release = int(0.3 * sample_rate)
    sustain = n_samples - attack - release
    envelope = np.concatenate(
        [np.linspace(0, 1, attack), np.ones(sustain), np.linspace(1, 0, release)]
    )
    envelope = envelope[:n_samples]
    return wave * envelope
