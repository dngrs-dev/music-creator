# random_effects.py
"""
Randomly select effects and generate random automation curves for a song render.
"""
import random
from effects.effect_automation import EffectAutomation


def random_effects_and_automation(song_length_sec):
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
    ]
    n_fx = random.randint(2, 6)
    effects_chain = random.sample(all_effects, n_fx)
    automation = {}
    for fx in effects_chain:
        params = {}
        if fx == "reverb" and random.random() < 0.7:
            points = [
                (0, random.uniform(0.2, 0.5)),
                (song_length_sec, random.uniform(0.6, 1.0)),
            ]
            params["decay"] = EffectAutomation(points)
        if fx == "eq" and random.random() < 0.7:
            points = [
                (0, random.uniform(-6, 3)),
                (song_length_sec, random.uniform(-3, 6)),
            ]
            params["gain"] = EffectAutomation(points)
        if fx == "stereo" and random.random() < 0.7:
            points = [
                (0, random.uniform(0.8, 1.2)),
                (song_length_sec, random.uniform(1.0, 2.0)),
            ]
            params["width"] = EffectAutomation(points)
        if fx == "granular" and random.random() < 0.7:
            points = [
                (0, random.uniform(20, 60)),
                (song_length_sec, random.uniform(40, 120)),
            ]
            params["grain_ms"] = EffectAutomation(points)
        if params:
            automation[fx] = params
    return effects_chain, automation
