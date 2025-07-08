import numpy as np


def snare(sample_rate=44100, duration=0.2, articulation=None):
    n_samples = int(sample_rate * duration)
    noise = np.random.normal(0, 1, n_samples)
    t = np.linspace(0, duration, n_samples, False)
    body = 0.2 * np.sin(2 * np.pi * 180 * t) * np.exp(-20 * t)
    attack = int(0.005 * sample_rate)
    decay = int(0.12 * sample_rate)
    envelope = np.concatenate([np.linspace(0, 1, attack), np.linspace(1, 0, decay)])
    envelope = np.pad(envelope, (0, n_samples - len(envelope)), "constant")
    filtered_noise = noise - np.roll(noise, 1)
    return (filtered_noise + body) * envelope


def kick(sample_rate=44100, duration=0.3, f0=100, articulation=None):
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    freq = f0 * np.exp(-6 * t) + 40
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    sine = np.sin(phase)
    click = np.zeros(n_samples)
    click[: int(0.01 * sample_rate)] = 1.0 * np.hanning(int(0.01 * sample_rate))
    envelope = np.exp(-5 * t)
    return (sine * envelope) + (0.2 * click)


def hihat(sample_rate=44100, duration=0.1, articulation=None):
    n_samples = int(sample_rate * duration)
    noise = np.random.normal(0, 1, n_samples)
    t = np.linspace(0, duration, n_samples, False)
    metallic = sum(
        [np.sin(2 * np.pi * f * t) for f in [8000, 9000, 10000, 12000, 14000]]
    )
    sound = 0.5 * noise + 0.5 * metallic / 5
    for i in range(1, n_samples):
        sound[i] = sound[i] - 0.98 * sound[i - 1]
    envelope = np.linspace(1, 0, n_samples)
    return sound * envelope
