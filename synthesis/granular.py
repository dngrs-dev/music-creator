import numpy as np
import random


def granular_synthesis(audio, grain_ms=50, overlap=0.5, random_pitch=0.1):
    grains = []
    grain_len = int(audio.frame_rate * grain_ms / 1000)
    step = int(grain_len * (1 - overlap))
    samples = np.array(audio.get_array_of_samples())
    for i in range(0, len(samples) - grain_len, step):
        grain = samples[i : i + grain_len].copy()
        pitch = 1 + random.uniform(-random_pitch, random_pitch)
        idx = np.round(np.arange(0, len(grain), pitch))
        idx = idx[idx < len(grain)].astype(int)
        grain = grain[idx]
        grains.append(grain)
    out = np.zeros(len(samples), dtype=samples.dtype)
    for i, grain in enumerate(grains):
        start = i * step
        end = start + len(grain)
        if end > len(out):
            break
        out[start:end] += grain
    return audio._spawn(out.tobytes())
