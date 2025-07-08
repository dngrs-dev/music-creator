from pydub import AudioSegment
import numpy as np


def pan_3d(audio, pan=-1.0, elevation=0.0):
    if audio.channels == 1:
        return audio
    left, right = audio.split_to_mono()
    left = left - (1 - pan) * 6
    right = right - (1 + pan) * 6
    return AudioSegment.from_mono_audiosegments(left, right)
