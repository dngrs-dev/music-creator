import numpy as np


def plucked_string(frequency, duration, sample_rate=44100, decay=0.998):
    n_samples = int(sample_rate * duration)
    noise = np.random.randn(n_samples)
    samples = np.zeros(n_samples)
    samples[: len(noise)] = noise
    for i in range(1, n_samples):
        samples[i] = decay * 0.5 * (samples[i - 1] + samples[i - 1])
    return samples
