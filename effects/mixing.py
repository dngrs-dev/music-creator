import numpy as np
from pydub import AudioSegment
from scipy.signal import lfilter, butter


def apply_eq(audio, freqs_gains):
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    sr = audio.frame_rate
    for freq, gain in freqs_gains:
        low = max(20, freq - 50)
        high = min(sr // 2 - 1, freq + 50)
        b, a = butter(2, [low / (sr / 2), high / (sr / 2)], btype="bandpass")
        band = lfilter(b, a, samples)
        samples += (10 ** (gain / 20) - 1) * band
    return audio._spawn(samples.astype(np.int16).tobytes())


def apply_compression(audio, threshold_db=-20, ratio=4, attack_ms=10, release_ms=100):
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    peak = np.max(np.abs(samples))
    threshold = peak * 10 ** (threshold_db / 20)
    over = np.abs(samples) > threshold
    samples[over] = np.sign(samples[over]) * (
        threshold + (np.abs(samples[over]) - threshold) / ratio
    )
    return audio._spawn(samples.astype(np.int16).tobytes())


def apply_limiter(audio, threshold_db=-1):
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
    peak = np.max(np.abs(samples))
    threshold = peak * 10 ** (threshold_db / 20)
    samples = np.clip(samples, -threshold, threshold)
    return audio._spawn(samples.astype(np.int16).tobytes())


def stereo_imaging(audio, width=1.0):
    if audio.channels == 1:
        return audio
    left, right = audio.split_to_mono()
    left_samples = np.array(left.get_array_of_samples(), dtype=np.float32)
    right_samples = np.array(right.get_array_of_samples(), dtype=np.float32)
    mid = (left_samples + right_samples) / 2
    side = (left_samples - right_samples) / 2
    left_new = mid + width * side
    right_new = mid - width * side
    left_new = np.clip(left_new, -32768, 32767).astype(np.int16)
    right_new = np.clip(right_new, -32768, 32767).astype(np.int16)
    left_seg = left._spawn(left_new.tobytes())
    right_seg = right._spawn(right_new.tobytes())
    return AudioSegment.from_mono_audiosegments(left_seg, right_seg)
