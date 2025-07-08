import os
import numpy as np
from scipy.io.wavfile import write
from instruments import (
    guitar,
    drums,
    bass,
    piano,
    synth_lead,
    synth_pad,
    organ,
    bell,
    flute,
    clarinet,
    violin,
    cello,
    trumpet,
    trombone,
    french_horn,
    oboe,
    saxophone,
    synth_bass,
    marimba,
    choir,
)

INSTRUMENTS = {
    "guitar": lambda freq, dur, articulation=None: guitar.karplus_strong(
        freq, dur, articulation=articulation
    ),
    "bass": lambda freq, dur, articulation=None: bass.bass(
        freq, dur, articulation=articulation
    ),
    "piano": lambda freq, dur, articulation=None: piano.piano(
        freq, dur, articulation=articulation
    ),
    "synth_lead": lambda freq, dur, articulation=None: synth_lead.synth_lead(
        freq, dur, articulation=articulation
    ),
    "synth_pad": lambda freq, dur, articulation=None: synth_pad.synth_pad(
        freq, dur, articulation=articulation
    ),
    "organ": lambda freq, dur, articulation=None: organ.organ(
        freq, dur, articulation=articulation
    ),
    "bell": lambda freq, dur, articulation=None: bell.bell(
        freq, dur, articulation=articulation
    ),
    "flute": lambda freq, dur, articulation=None: flute.flute(
        freq, dur, articulation=articulation
    ),
    "clarinet": lambda freq, dur, articulation=None: clarinet.clarinet(
        freq, dur, articulation=articulation
    ),
    "violin": lambda freq, dur, articulation=None: violin.violin(
        freq, dur, articulation=articulation
    ),
    "cello": lambda freq, dur, articulation=None: cello.cello(
        freq, dur, articulation=articulation
    ),
    "trumpet": lambda freq, dur, articulation=None: trumpet.trumpet(
        freq, dur, articulation=articulation
    ),
    "trombone": lambda freq, dur, articulation=None: trombone.trombone(
        freq, dur, articulation=articulation
    ),
    "french_horn": lambda freq, dur, articulation=None: french_horn.french_horn(
        freq, dur, articulation=articulation
    ),
    "oboe": lambda freq, dur, articulation=None: oboe.oboe(
        freq, dur, articulation=articulation
    ),
    "saxophone": lambda freq, dur, articulation=None: saxophone.saxophone(
        freq, dur, articulation=articulation
    ),
    "synth_bass": lambda freq, dur, articulation=None: synth_bass.synth_bass(
        freq, dur, articulation=articulation
    ),
    "marimba": lambda freq, dur, articulation=None: marimba.marimba(
        freq, dur, articulation=articulation
    ),
    "choir": lambda freq, dur, articulation=None: choir.choir(
        freq, dur, articulation=articulation
    ),
}

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "samples")


def generate_instrument_note_wav(instr, frequency, duration, filename, detune_cents=0):
    import glob

    midi_guess = int(round(69 + 12 * np.log2(frequency / 440.0)))
    sample_pattern = os.path.join(SAMPLES_DIR, f"{instr}_*{midi_guess}*.wav")
    sample_files = glob.glob(sample_pattern)
    if sample_files:
        from pydub import AudioSegment

        seg = AudioSegment.from_wav(sample_files[0])
        seg = (
            seg[: int(duration * 1000)]
            if len(seg) > int(duration * 1000)
            else seg + AudioSegment.silent(int(duration * 1000) - len(seg))
        )
        seg.export(filename, format="wav")
        return
    freq = frequency * (2 ** (detune_cents / 1200))
    samples = INSTRUMENTS[instr](freq, duration)
    samples2 = INSTRUMENTS[instr](freq * 1.003, duration)
    samples3 = INSTRUMENTS[instr](freq * 0.997, duration)
    samples = (samples + samples2 + samples3) / 3
    samples = samples * (0.95 + 0.1 * np.random.rand())
    samples = np.int16(samples / np.max(np.abs(samples)) * 32767)
    write(filename, 44100, samples)


def generate_drum_wav(kind, duration, filename):
    import glob

    sample_pattern = os.path.join(SAMPLES_DIR, f"drum_{kind}*.wav")
    sample_files = glob.glob(sample_pattern)
    if sample_files:
        from pydub import AudioSegment

        seg = AudioSegment.from_wav(sample_files[0])
        seg = (
            seg[: int(duration * 1000)]
            if len(seg) > int(duration * 1000)
            else seg + AudioSegment.silent(int(duration * 1000) - len(seg))
        )
        seg.export(filename, format="wav")
        return
    if kind == "snare":
        samples = drums.snare(duration=duration)
    elif kind == "kick":
        samples = drums.kick(duration=duration)
    elif kind == "hihat":
        samples = drums.hihat(duration=duration)
    else:
        raise ValueError("Unknown drum type")
    samples2 = samples * (0.98 + 0.04 * np.random.rand())
    samples = (samples + samples2) / 2
    samples = np.int16(samples / np.max(np.abs(samples)) * 32767)
    write(filename, 44100, samples)
