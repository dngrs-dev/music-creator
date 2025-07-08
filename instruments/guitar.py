import numpy as np
import sounddevice as sd


def karplus_strong(
    frequency, duration=1.0, sample_rate=44100, decay=0.998, articulation=None
):
    n_samples = int(sample_rate * duration)
    buf = np.random.rand(int(sample_rate // frequency)) * 2 - 1
    samples = np.zeros(n_samples)
    for i in range(n_samples):
        samples[i] = buf[0]
        avg = decay * 0.5 * (buf[0] + buf[1])
        buf = np.append(buf[1:], avg)

    # Add a subtle second harmonic for warmth
    t = np.arange(n_samples) / sample_rate
    harmonic = 0.15 * np.sin(2 * np.pi * frequency * 2 * t)
    samples = samples + harmonic

    # ADSR envelope: attack, decay, sustain, release
    attack = int(0.01 * sample_rate)
    decay_len = int(0.08 * sample_rate)
    sustain_len = n_samples - attack - decay_len - int(0.3 * sample_rate)
    sustain_level = 0.7
    release = int(0.3 * sample_rate)
    env = np.concatenate(
        [
            np.linspace(0, 1, attack),
            np.linspace(1, sustain_level, decay_len),
            np.ones(max(0, sustain_len)) * sustain_level,
            np.linspace(sustain_level, 0, release),
        ]
    )
    env = env[:n_samples]
    samples *= env
    return samples


def play_note(frequency, duration=1.0, sample_rate=44100, articulation=None):
    samples = karplus_strong(frequency, duration, sample_rate)
    sd.play(samples, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_note(82.41, duration=2.0)
