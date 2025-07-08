class Section:
    def __init__(
        self, name, bars, pattern, key, scale, tempo=None, time_signature=(4, 4)
    ):
        self.name = name
        self.bars = bars
        self.pattern = pattern
        self.key = key
        self.scale = scale
        self.tempo = tempo
        self.time_signature = time_signature


class Song:
    def __init__(
        self, sections, tempo=120, time_signature=(4, 4), key="C", scale="major"
    ):
        self.sections = sections
        self.tempo = tempo
        self.time_signature = time_signature
        self.key = key
        self.scale = scale

    def get_total_length_sec(self):
        beats_per_bar = self.time_signature[0]
        sec_per_beat = 60.0 / self.tempo
        total_bars = sum(s.bars for s in self.sections)
        return total_bars * beats_per_bar * sec_per_beat

    def get_section_start_sec(self, idx):
        beats_per_bar = self.time_signature[0]
        sec_per_beat = 60.0 / self.tempo
        t = 0
        for i, s in enumerate(self.sections):
            if i == idx:
                return t
            t += s.bars * beats_per_bar * sec_per_beat
        return t
