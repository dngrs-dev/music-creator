import os
import random
from composition.song import Song, Section
from composition.theory import (
    SCALES,
    NOTE_NAMES,
    note_name_to_midi,
    midi_to_freq,
    get_scale_notes,
)
from utils.export import combine_and_export_song
from utils.random_effects import random_effects_and_automation
from utils.music_metadata import collect_music_metadata, export_music_metadata


def generate_music_main(params, output_file, metadata_file):
    class MarkovMelodyGenerator:
        def __init__(self, scale_midis):
            self.scale_midis = scale_midis
            self.transition = self._build_transition()

        def _build_transition(self):
            trans = {}
            for midi in self.scale_midis:
                steps = [m for m in self.scale_midis if abs(m - midi) == 1]
                small_steps = [m for m in self.scale_midis if abs(m - midi) == 2]
                leaps = [m for m in self.scale_midis if abs(m - midi) > 2]
                pool = steps * 8 + small_steps * 2 + leaps + [midi] * 2
                trans[midi] = pool
            return trans

        def generate(self, length, start=None):
            if not self.scale_midis:
                return []
            melody = []
            curr = start if start else random.choice(self.scale_midis)
            for _ in range(length):
                melody.append(curr)
                curr = random.choice(self.transition[curr])
            return melody

    MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")
    all_instruments = [
        "guitar",
        "piano",
        "violin",
        "synth_lead",
        "synth_pad",
        "organ",
        "bell",
        "flute",
        "clarinet",
        "cello",
        "trumpet",
        "trombone",
        "french_horn",
        "oboe",
        "saxophone",
        "synth_bass",
        "marimba",
        "choir",
        "bass",
    ]
    all_drums = ["kick", "snare", "hihat"]
    all_effects = [
        "delay",
        "chorus",
        "flanger",
        "phaser",
        "reverb",
        "granular",
        "eq",
        "compressor",
        "limiter",
        "stereo",
        "spatial",
        "bitcrusher",
        "distortion",
    ]
    time_signature = (4, 4)
    sections_param = params.get("sections", [])
    structure = params.get(
        "structure",
        [s.get("name", f"Section {i+1}") for i, s in enumerate(sections_param)],
    )
    if not sections_param:
        raise ValueError("No sections provided")
    section_dict = {
        s.get("name", f"Section {i+1}"): s for i, s in enumerate(sections_param)
    }
    song_sections = []
    for idx, section_name in enumerate(structure):
        s = section_dict.get(section_name)
        if not s:
            raise ValueError(f'Section name "{section_name}" not found in sections')
        instrs = s.get("instruments", [])
        if "__random__" in instrs:
            instrs = random.sample(all_instruments, k=random.randint(1, 3))
        drs = s.get("drums", [])
        if "__random__" in drs:
            drs = random.sample(all_drums, k=random.randint(1, 3))
        fx = s.get("effects", [])
        if "__random__" in fx:
            fx = random.sample(all_effects, k=random.randint(1, 3))
        name = s.get("name", f"Section {idx+1}")
        duration_sec = int(s.get("duration", 4))
        tempo = int(s.get("tempo", 120))
        key = s.get("key", "C")
        scale = s.get("scale", "major")
        bars = max(1, int(duration_sec * tempo / 60 / time_signature[0]))
        scale_midis = get_scale_notes(key, scale, octaves=(3, 5))

        def markov_melody_pattern(length_beats, instr, vol=0, pan=0):
            pattern = []
            markov = MarkovMelodyGenerator(scale_midis)
            melody = markov.generate(length_beats)
            for b, midi in enumerate(melody):
                timing = random.uniform(-0.05, 0.05)
                velocity = vol + random.uniform(-2, 2)
                pattern.append(
                    (
                        b + timing,
                        "melodic",
                        instr,
                        midi,
                        1,
                        velocity,
                        pan + random.uniform(-0.1, 0.1),
                    )
                )
            return pattern

        def random_chord_pattern(length_bars, instr, vol=0, pan=0):
            pattern = []
            beats_per_bar = time_signature[0]
            for bar in range(length_bars):
                root = random.choice(scale_midis)
                chord = [root, root + 4, root + 7]
                timing = random.uniform(-0.05, 0.05)
                velocity = vol + random.uniform(-2, 2)
                pattern.append(
                    (
                        bar * beats_per_bar + timing,
                        "chord",
                        instr,
                        chord,
                        beats_per_bar,
                        velocity,
                        pan + random.uniform(-0.1, 0.1),
                    )
                )
            return pattern

        def random_drum_pattern(length_beats):
            pattern = []
            for b in range(length_beats):
                timing = random.uniform(-0.02, 0.02)
                velocity = random.uniform(-2, 2)
                if b % 4 == 0 and "kick" in drs:
                    pattern.append((b + timing, "drum", "kick", None, 1, velocity, 0))
                if b % 4 == 2 and "snare" in drs:
                    pattern.append((b + timing, "drum", "snare", None, 1, velocity, 0))
                if b % 2 == 1 and "hihat" in drs:
                    pattern.append((b + timing, "drum", "hihat", None, 1, velocity, 0))
            return pattern

        beats = bars * time_signature[0]
        pattern = []
        if instrs:
            for i, instr in enumerate(instrs):
                start_beat = int(i * beats / len(instrs))
                end_beat = int((i + 1) * beats / len(instrs))
                length = end_beat - start_beat
                if length > 0:
                    melody_pat = markov_melody_pattern(length, instr, vol=0, pan=0)
                    melody_pat = [(b + start_beat, *rest) for (b, *rest) in melody_pat]
                    pattern.extend(melody_pat)
        if instrs:
            for instr in instrs:
                chord_pat = random_chord_pattern(bars, instr, vol=-3, pan=0.1)
                pattern.extend(chord_pat)
        pattern += random_drum_pattern(beats)
        if instrs or drs:
            section_obj = Section(
                name,
                bars=bars,
                pattern=pattern,
                key=key,
                scale=scale,
                tempo=tempo,
                time_signature=time_signature,
            )
            song_sections.append(section_obj)
    if not song_sections:
        raise ValueError(
            "No instruments or drums selected for any section. Please select at least one instrument or drum."
        )
    song = Song(
        song_sections,
        tempo=song_sections[0].tempo,
        time_signature=time_signature,
        key=song_sections[0].key,
        scale=song_sections[0].scale,
    )
    song_length_sec = song.get_total_length_sec()
    all_fx = []
    for s in sections_param:
        fx = s.get("effects", [])
        if "__random__" in fx:
            fx = random.sample(all_effects, k=random.randint(1, 3))
        all_fx.extend(fx)
    effects_chain = list(dict.fromkeys(all_fx))
    effect_automations = {}
    for fx in effects_chain:
        effect_automations[fx] = random_effects_and_automation(song_length_sec)[1].get(
            fx, {}
        )
    combine_and_export_song(
        song, output_file, effects_chain=effects_chain, automation=effect_automations
    )
    metadata = collect_music_metadata(
        song, effects_chain=effects_chain, effect_automations=effect_automations
    )
    export_music_metadata(metadata, metadata_file)
    print(
        f"Music exported to {output_file}\nMetadata exported to {metadata_file}\nEffects: {effects_chain}\nAutomations: {list(effect_automations.keys())}"
    )
