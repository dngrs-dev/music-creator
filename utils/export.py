import os
import numpy as np
from pydub import AudioSegment, effects
from effects.effects import (
    add_delay,
    add_chorus,
    add_flanger,
    add_phaser,
    add_advanced_reverb,
)
from synthesis.granular import granular_synthesis
from effects.mixing import apply_eq, apply_compression, apply_limiter, stereo_imaging
from effects.spatial_audio import pan_3d
from composition.theory import midi_to_freq


def combine_and_export_song(song, output_file, automation=None, effects_chain=None):
    total_sec = song.get_total_length_sec()
    timeline = AudioSegment.silent(duration=int(total_sec * 1000))
    beats_per_bar = song.time_signature[0]
    sec_per_beat = 60.0 / song.tempo

    print(
        f"[Progress] Song has {len(song.sections)} sections, total {total_sec:.1f} seconds."
    )
    for idx, section in enumerate(song.sections):
        print(
            f"[Progress] Section {idx+1}/{len(song.sections)}: {section.name} (bars={section.bars}, key={section.key}, scale={section.scale}, tempo={getattr(section, 'tempo', song.tempo)})"
        )
        section_start = song.get_section_start_sec(idx)
        for ev_idx, event in enumerate(section.pattern):
            if len(event) > 7 and isinstance(event[-1], dict):
                auto = event[-1]
                base = event[:-1]
            else:
                auto = {}
                base = event
            beat_offset = base[0]
            event_type = base[1]
            t_sec = section_start + beat_offset * sec_per_beat
            if event_type == "melodic":
                if len(base) == 8:
                    _, _, instr, midi, note_dur, vol, pan, articulation = base
                else:
                    _, _, instr, midi, note_dur, vol, pan = base
                    articulation = "normal"
                if isinstance(pan, dict):
                    pan = 0.0
                freq = midi_to_freq(midi)
                detune = np.random.uniform(-5, 5)
                timing = np.random.uniform(-0.03, 0.03)
                note_wav = os.path.join("sounds", f"{instr}_{midi}_{t_sec}.wav")
                from instruments.utils import INSTRUMENTS

                samples = INSTRUMENTS[instr](
                    freq, note_dur * sec_per_beat, articulation=articulation
                )
                samples = np.int16(samples / np.max(np.abs(samples)) * 32767)
                from scipy.io.wavfile import write

                write(note_wav, 44100, samples)
                note_sound = AudioSegment.from_wav(note_wav) + vol
                if "volume" in auto:
                    note_sound += auto["volume"].get(t_sec)
                if "pan" in auto:
                    note_sound = effects.pan(note_sound, auto["pan"].get(t_sec))
                elif pan != 0:
                    note_sound = effects.pan(note_sound, pan)
                position_ms = int((t_sec + timing) * 1000)
                timeline = timeline.overlay(note_sound, position=position_ms)
            elif event_type == "chord":
                _, _, instr, midis, note_dur, vol, pan = base
                if isinstance(pan, dict):
                    pan = 0.0
                timing = np.random.uniform(-0.03, 0.03)
                chord_sounds = []
                for midi in midis:
                    freq = midi_to_freq(midi)
                    detune = np.random.uniform(-5, 5)
                    note_wav = os.path.join("sounds", f"{instr}_{midi}_{t_sec}.wav")
                    from instruments.utils import generate_instrument_note_wav

                    generate_instrument_note_wav(
                        instr,
                        freq,
                        note_dur * sec_per_beat,
                        note_wav,
                        detune_cents=detune,
                    )
                    note_sound = AudioSegment.from_wav(note_wav)
                    chord_sounds.append(note_sound)
                chord_mix = chord_sounds[0]
                for snd in chord_sounds[1:]:
                    chord_mix = chord_mix.overlay(snd)
                chord_mix += vol
                if "volume" in auto:
                    chord_mix += auto["volume"].get(t_sec)
                if "pan" in auto:
                    chord_mix = effects.pan(chord_mix, auto["pan"].get(t_sec))
                elif pan != 0:
                    chord_mix = effects.pan(chord_mix, pan)
                position_ms = int((t_sec + timing) * 1000)
                timeline = timeline.overlay(chord_mix, position=position_ms)
            elif event_type == "arpeggio":
                _, _, instr, midis, note_dur, vol, pan, arp_type = base
                if isinstance(pan, dict):
                    pan = 0.0
                timing = np.random.uniform(-0.03, 0.03)
                arp_notes = midis if arp_type == "up" else list(reversed(midis))
                arp_gap = (note_dur * sec_per_beat) / len(arp_notes)
                for i, midi in enumerate(arp_notes):
                    freq = midi_to_freq(midi)
                    detune = np.random.uniform(-5, 5)
                    note_wav = os.path.join(
                        "sounds", f"{instr}_{midi}_{t_sec}_arp{i}.wav"
                    )
                    from instruments.utils import generate_instrument_note_wav

                    generate_instrument_note_wav(
                        instr, freq, arp_gap, note_wav, detune_cents=detune
                    )
                    note_sound = AudioSegment.from_wav(note_wav)
                    note_sound += vol
                    if "volume" in auto:
                        note_sound += auto["volume"].get(t_sec + i * arp_gap)
                    if "pan" in auto:
                        note_sound = effects.pan(
                            note_sound, auto["pan"].get(t_sec + i * arp_gap)
                        )
                    elif pan != 0:
                        note_sound = effects.pan(note_sound, pan)
                    position_ms = int((t_sec + timing + i * arp_gap) * 1000)
                    timeline = timeline.overlay(note_sound, position=position_ms)
            elif event_type == "drum":
                _, _, kind, _, note_dur, vol, pan = base
                if isinstance(pan, dict):
                    pan = 0.0
                timing = np.random.uniform(-0.01, 0.01)
                drum_wav = os.path.join("sounds", f"drum_{kind}_{t_sec}.wav")
                from instruments.utils import generate_drum_wav

                generate_drum_wav(kind, note_dur * sec_per_beat, drum_wav)
                drum_sound = AudioSegment.from_wav(drum_wav) + vol
                if "volume" in auto:
                    drum_sound += auto["volume"].get(t_sec)
                if "pan" in auto:
                    drum_sound = effects.pan(drum_sound, auto["pan"].get(t_sec))
                elif pan != 0:
                    drum_sound = effects.pan(drum_sound, pan)
                position_ms = int((t_sec + timing) * 1000)
                timeline = timeline.overlay(drum_sound, position=position_ms)

    if effects_chain:
        print(f"[Progress] Applying effects: {effects_chain}")
        segment_ms = 100
        total_ms = len(timeline)
        for fx in effects_chain:
            print(f"  [Progress] Effect: {fx}")
            autom = automation[fx] if automation and fx in automation else {}
            segments = []
            for start in range(0, total_ms, segment_ms):
                if start % (1000 * 5) == 0:
                    print(
                        f"    [Progress] {fx}: {start/1000:.1f}s / {total_ms/1000:.1f}s"
                    )
                seg = timeline[start : start + segment_ms]
                t_sec = start / 1000.0
                if fx == "reverb":
                    decay = autom["decay"].get(t_sec) if "decay" in autom else 0.5
                    seg = add_advanced_reverb(seg, decay=decay)
                elif fx == "eq":
                    gain = autom["gain"].get(t_sec) if "gain" in autom else 0
                    seg = apply_eq(seg, [(200, gain)])
                elif fx == "stereo":
                    width = autom["width"].get(t_sec) if "width" in autom else 1.2
                    seg = stereo_imaging(seg, width=width)
                elif fx == "granular":
                    grain_ms = (
                        autom["grain_ms"].get(t_sec) if "grain_ms" in autom else 50
                    )
                    seg = granular_synthesis(seg, grain_ms=grain_ms)
                elif fx == "bitcrusher":
                    bits = autom["bits"].get(t_sec) if "bits" in autom else 8
                    seg = bitcrusher(seg, bits=bits)
                elif fx == "distortion":
                    gain = autom["gain"].get(t_sec) if "gain" in autom else 10
                    seg = distortion(seg, gain=gain)
                else:
                    if fx == "delay":
                        seg = add_delay(seg)
                    elif fx == "chorus":
                        seg = add_chorus(seg)
                    elif fx == "flanger":
                        seg = add_flanger(seg)
                    elif fx == "phaser":
                        seg = add_phaser(seg)
                    elif fx == "compressor":
                        seg = apply_compression(seg)
                    elif fx == "limiter":
                        seg = apply_limiter(seg)
                    elif fx == "spatial":
                        seg = pan_3d(seg)
                segments.append(seg)
            timeline = segments[0]
            for seg in segments[1:]:
                timeline += seg
    timeline.export(output_file, format="wav")


def bitcrusher(audioseg, bits=8):
    arr = np.array(audioseg.get_array_of_samples())
    arr = np.round(arr / (2 ** (16 - bits))) * (2 ** (16 - bits))
    arr = np.clip(arr, -32768, 32767)
    return audioseg._spawn(arr.astype(np.int16).tobytes())


def distortion(audioseg, gain=10):
    arr = np.array(audioseg.get_array_of_samples(), dtype=np.float32)
    arr = arr * gain
    arr = np.tanh(arr / 32768.0) * 32768
    arr = np.clip(arr, -32768, 32767)
    return audioseg._spawn(arr.astype(np.int16).tobytes())
