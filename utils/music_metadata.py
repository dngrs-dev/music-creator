import json
from collections import defaultdict


def collect_music_metadata(song, effects_chain=None, effect_automations=None):
    metadata = {
        "song": {
            "tempo": getattr(song, "tempo", None),
            "time_signature": getattr(song, "time_signature", None),
            "key": getattr(song, "key", None),
            "scale": getattr(song, "scale", None),
            "total_length_sec": (
                song.get_total_length_sec()
                if hasattr(song, "get_total_length_sec")
                else None
            ),
            "total_bars": sum(
                getattr(s, "bars", 0) for s in getattr(song, "sections", [])
            ),
        },
        "sections": [],
        "instruments": set(),
        "effects": [],
        "unique_notes": set(),
    }
    from composition.theory import NOTE_NAMES, midi_to_freq

    for idx, section in enumerate(song.sections):
        section_info = {
            "name": section.name,
            "bars": section.bars,
            "key": section.key,
            "scale": section.scale,
            "events": [],
        }
        section_start_sec = (
            song.get_section_start_sec(idx)
            if hasattr(song, "get_section_start_sec")
            else None
        )
        for event in section.pattern:
            if len(event) > 7 and isinstance(event[-1], dict):
                auto = event[-1]
                base = event[:-1]
            else:
                auto = {}
                base = event
            event_type = base[1]
            event_info = {"type": event_type}
            beat_offset = base[0] if len(base) > 0 else None
            event_info["beat_offset"] = beat_offset
            if section_start_sec is not None and beat_offset is not None:
                sec_per_beat = 60.0 / getattr(song, "tempo", 120)
                event_info["time_sec"] = section_start_sec + beat_offset * sec_per_beat
            event_info["section_index"] = idx
            event_info["section_name"] = section.name
            if event_type == "melodic":
                instr = base[2]
                midi = base[3]
                note_dur = base[4] if len(base) > 4 else None
                vol = base[5] if len(base) > 5 else None
                pan = base[6] if len(base) > 6 else None
                articulation = (
                    base[7] if len(base) > 7 and not isinstance(base[7], dict) else None
                )
                event_info.update(
                    {
                        "instrument": instr,
                        "midi": midi,
                        "note_name": NOTE_NAMES[midi % 12] + str(midi // 12 - 1),
                        "frequency_hz": midi_to_freq(midi),
                        "duration_beats": note_dur,
                        "duration_sec": (
                            note_dur * sec_per_beat if note_dur is not None else None
                        ),
                        "volume_db": vol,
                        "pan": pan,
                        "articulation": articulation,
                    }
                )
                metadata["instruments"].add(instr)
                metadata["unique_notes"].add(event_info["note_name"])
            elif event_type == "chord":
                instr = base[2]
                midis = base[3]
                note_dur = base[4] if len(base) > 4 else None
                vol = base[5] if len(base) > 5 else None
                pan = base[6] if len(base) > 6 else None
                event_info.update(
                    {
                        "instrument": instr,
                        "midis": midis,
                        "note_names": [
                            NOTE_NAMES[m % 12] + str(m // 12 - 1) for m in midis
                        ],
                        "frequencies_hz": [midi_to_freq(m) for m in midis],
                        "duration_beats": note_dur,
                        "duration_sec": (
                            note_dur * sec_per_beat if note_dur is not None else None
                        ),
                        "volume_db": vol,
                        "pan": pan,
                    }
                )
                metadata["instruments"].add(instr)
                for m in midis:
                    metadata["unique_notes"].add(NOTE_NAMES[m % 12] + str(m // 12 - 1))
            elif event_type == "arpeggio":
                instr = base[2]
                midis = base[3]
                note_dur = base[4] if len(base) > 4 else None
                vol = base[5] if len(base) > 5 else None
                pan = base[6] if len(base) > 6 else None
                arp_type = base[7] if len(base) > 7 else None
                event_info.update(
                    {
                        "instrument": instr,
                        "midis": midis,
                        "note_names": [
                            NOTE_NAMES[m % 12] + str(m // 12 - 1) for m in midis
                        ],
                        "frequencies_hz": [midi_to_freq(m) for m in midis],
                        "duration_beats": note_dur,
                        "duration_sec": (
                            note_dur * sec_per_beat if note_dur is not None else None
                        ),
                        "volume_db": vol,
                        "pan": pan,
                        "arpeggio_type": arp_type,
                    }
                )
                metadata["instruments"].add(instr)
                for m in midis:
                    metadata["unique_notes"].add(NOTE_NAMES[m % 12] + str(m // 12 - 1))
            elif event_type == "drum":
                kind = base[2]
                note_dur = base[4] if len(base) > 4 else None
                vol = base[5] if len(base) > 5 else None
                pan = base[6] if len(base) > 6 else None
                event_info.update(
                    {
                        "drum": kind,
                        "duration_beats": note_dur,
                        "duration_sec": (
                            note_dur * sec_per_beat if note_dur is not None else None
                        ),
                        "volume_db": vol,
                        "pan": pan,
                    }
                )
                metadata["instruments"].add(kind)
            if auto:
                event_info["automation"] = {
                    k: getattr(v, "points", v) if hasattr(v, "points") else v
                    for k, v in auto.items()
                }
            section_info["events"].append(event_info)
        metadata["sections"].append(section_info)
    if effects_chain:
        metadata["effects"] = []
        for fx in effects_chain:
            fx_info = {"name": fx}
            if effect_automations and fx in effect_automations:
                autom = effect_automations[fx]
                param_points = {}
                for param, auto_obj in autom.items():
                    if hasattr(auto_obj, "points"):
                        param_points[param] = auto_obj.points
                    else:
                        param_points[param] = auto_obj
                if param_points:
                    fx_info["automation_points"] = param_points
            metadata["effects"].append(fx_info)
    if effect_automations:
        metadata["effect_automations"] = list(effect_automations.keys())
    metadata["instruments"] = list(metadata["instruments"])
    metadata["unique_notes"] = list(metadata["unique_notes"])
    key_hist = {}
    for section in song.sections:
        k = getattr(section, "key", None)
        if k:
            key_hist[k] = key_hist.get(k, 0) + 1
    metadata["key_histogram"] = key_hist
    note_hist = {}
    for note in metadata["unique_notes"]:
        note_hist[note] = note_hist.get(note, 0) + 1
    metadata["note_histogram"] = note_hist
    motifs = []
    for section in song.sections:
        notes = []
        for event in section.pattern:
            if len(event) > 3 and event[1] == "melodic":
                midi = event[3]
                notes.append(NOTE_NAMES[midi % 12] + str(midi // 12 - 1))
            if len(notes) >= 4:
                break
        motifs.append({"section": section.name, "motif": notes})
    metadata["section_motifs"] = motifs
    return metadata


def export_music_metadata(metadata, output_path):

    def make_json_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_json_serializable(v) for v in obj]
        elif hasattr(obj, "points") and isinstance(obj.points, list):
            return obj.points
        elif hasattr(obj, "__dict__"):
            return make_json_serializable(obj.__dict__)
        else:
            try:
                json.dumps(obj)
                return obj
            except TypeError:
                return str(obj)

    serializable_metadata = make_json_serializable(metadata)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable_metadata, f, indent=2)
