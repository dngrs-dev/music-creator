import numpy as np
import random


def add_delay(audio, delay_ms=250, decay=0.5, repeats=3):
    out = audio
    for i in range(1, repeats + 1):
        out = out.overlay(audio - (i * 4), position=i * delay_ms)
    return out


def add_chorus(audio, depth_ms=15, n_voices=3):
    out = audio
    for i in range(1, n_voices):
        out = out.overlay(
            audio._spawn(
                audio.raw_data,
                overrides={
                    "frame_rate": int(
                        audio.frame_rate
                        * (1 + (random.uniform(-1, 1) * depth_ms / 1000))
                    )
                },
            )
        )
    return out


def add_flanger(audio, depth_ms=5, rate_hz=0.25):
    out = audio
    for i in range(
        0, int(audio.duration_seconds * audio.frame_rate), int(audio.frame_rate / 100)
    ):
        delay = int(depth_ms * (1 + np.sin(2 * np.pi * rate_hz * i / audio.frame_rate)))
        out = out.overlay(audio - 6, position=delay)
    return out


def add_phaser(audio, depth_ms=2, rate_hz=0.5):
    out = audio
    for i in range(
        0, int(audio.duration_seconds * audio.frame_rate), int(audio.frame_rate / 200)
    ):
        delay = int(depth_ms * (1 + np.sin(2 * np.pi * rate_hz * i / audio.frame_rate)))
        out = out.overlay(audio - 8, position=delay)
    return out


def add_advanced_reverb(audio, delay_ms=60, decay=0.5, repeats=8):
    out = audio
    for i in range(1, repeats + 1):
        out = out.overlay(audio - (i * 6), position=i * delay_ms)
    return out
