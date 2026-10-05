"""Synthèse de musiques d'ambiance originales (numpy) pour chaque biome du Sift -> .ogg via ffmpeg."""
import os
import subprocess
import wave

import numpy as np

SR = 32000


def _env(n, a, d, s, r, sus=0.6):
    t = np.arange(n) / SR
    a, d, r = max(a, 1e-3), max(d, 1e-3), max(r, 1e-3)
    e = np.where(t < a, t / a, np.where(t < a + d, 1 - (1 - sus) * (t - a) / d, sus))
    tail = np.clip((n / SR - t) / r, 0, 1)
    return e * tail


def tone(f, dur, kind="sine", vib=0.0, a=0.05, d=0.2, r=0.4, sus=0.7, detune=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = 2 * np.pi * f * t + (vib * np.sin(2 * np.pi * 5 * t) if vib else 0)
    if kind == "sine":
        y = np.sin(ph)
    elif kind == "soft":      # sinus + harmoniques douces
        y = np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    elif kind == "pad":       # voix désaccordées
        y = sum(np.sin(2 * np.pi * f * (1 + k * detune) * t + k) for k in (-1, 0, 1)) / 3
        y += 0.3 * np.sin(2 * np.pi * f * 2 * t)
    elif kind == "bell":      # cloche inharmonique
        y = (np.sin(ph) + 0.6 * np.sin(2.76 * ph) + 0.35 * np.sin(5.4 * ph) + 0.2 * np.sin(8.93 * ph))
        e = np.exp(-t * (1.6 + f / 900.0))
        return y * e * (1 - np.exp(-t * 400))
    elif kind == "glass":
        y = np.sin(ph) + 0.5 * np.sin(3.01 * ph)
        e = np.exp(-t * 2.2)
        return y * e * (1 - np.exp(-t * 300))
    elif kind == "flute":
        y = np.sin(ph) + 0.15 * np.sin(2 * ph) + 0.05 * np.random.randn(n)
    elif kind == "choir":
        # formants approximatifs (« aah »)
        base = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 12))
        y = base * (1 + 0.25 * np.sin(2 * np.pi * 5.2 * t))
    else:
        y = np.sin(ph)
    return y * _env(n, a, d, 0, r, sus)


def ping(f, dur=3.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 1.4) * (1 - np.exp(-t * 500))


def blip(f0, dur=0.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + 2.5 * t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


def click(dur=0.12, bright=0.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.random.randn(n) * np.exp(-t * 45) * bright


def place(buf, y, start, gain=1.0, pan=None):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(y))
    buf[i:j] += y[: j - i] * gain


def reverb(x, seconds=3.2, wet=0.38, seed=7):
    rng = np.random.RandomState(seed)
    n = int(seconds * SR)
    ir = rng.randn(n) * np.exp(-np.arange(n) / SR * (6.0 / seconds))
    ir[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
    ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x * (1 - wet) + y * wet * 2.2


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)


SCALES = {
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "penta": [0, 2, 4, 7, 9],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "whole": [0, 2, 4, 6, 8, 10],
    "minor_penta": [0, 3, 5, 7, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
}


def scale_notes(root, name, lo, hi):
    out = []
    for octv in range(-2, 8):
        for s in SCALES[name]:
            m = root + 12 * octv + s
            if lo <= m <= hi:
                out.append(m)
    return sorted(out)


def compose(name, seconds, root, scale, chords, spec, seed):
    rng = np.random.RandomState(seed)
    np.random.seed(seed)
    buf = np.zeros(int(seconds * SR))
    # nappes d'accords
    t, ci = 0.0, 0
    while t < seconds:
        ch = chords[ci % len(chords)]
        dur = spec.get("chord_len", 10.0)
        for k, deg in enumerate(ch):
            f = midi(root + deg + (0 if k < 2 else 12))
            place(buf, tone(f, dur + 4, "pad", a=3.5, d=2, r=4, sus=0.8, detune=0.0035), t, spec.get("pad", 0.16))
        if spec.get("sub"):
            place(buf, tone(midi(root + ch[0] - 12), dur + 3, "sine", a=3, r=4), t, spec["sub"])
        t += dur
        ci += 1
    notes = scale_notes(root, scale, spec.get("lo", 64), spec.get("hi", 96))
    # mélodie principale : tintements aléatoires marchant dans la gamme
    t, idx = spec.get("start", 2.0), len(notes) // 2
    while t < seconds - 3:
        idx = int(np.clip(idx + rng.choice([-2, -1, -1, 0, 1, 1, 2, 3]), 0, len(notes) - 1))
        place(buf, tone(midi(notes[idx]), 4.5, spec.get("lead", "bell")), t, spec.get("lead_gain", 0.3))
        if rng.rand() < spec.get("echo", 0.3):
            place(buf, tone(midi(notes[idx]), 4.0, spec.get("lead", "bell")), t + 0.375, spec.get("lead_gain", 0.3) * 0.45)
        t += rng.choice(spec.get("rhythm", [0.75, 1.5, 1.5, 2.25, 3.0]))
    if spec.get("choir"):
        t = 6.0
        while t < seconds - 8:
            m = rng.choice(scale_notes(root, scale, 52, 68))
            place(buf, tone(midi(m), 7, "choir", a=2.5, r=3, sus=0.7), t, spec["choir"])
            t += rng.choice([8, 10, 12])
    if spec.get("flute"):
        t = 8.0
        while t < seconds - 6:
            for j in range(rng.randint(2, 4)):
                m = rng.choice(scale_notes(root, scale, 60, 79))
                place(buf, tone(midi(m), 2.2, "flute", vib=0.6, a=0.25, r=0.8), t + j * 1.7, spec["flute"])
            t += rng.choice([14, 18])
    if spec.get("blips"):
        t = 3.0
        while t < seconds - 2:
            place(buf, blip(rng.choice([300, 380, 450, 520, 640]), 0.22), t, spec["blips"])
            t += rng.choice([1.2, 2.4, 3.1, 5.0])
    if spec.get("clicks"):
        t = 4.0
        while t < seconds - 2:
            place(buf, click(0.1, 0.5), t, spec["clicks"])
            t += rng.choice([2.5, 3.0, 5.5])
    if spec.get("pings"):
        t = 5.0
        while t < seconds - 5:
            place(buf, ping(midi(rng.choice(scale_notes(root, scale, 72, 100))), 3.5), t, spec["pings"])
            t += rng.choice([6, 7.5, 9, 11])
    buf = reverb(buf, spec.get("verb", 3.4), spec.get("wet", 0.4), seed)
    # fondu d'entrée/sortie + normalisation douce
    n = len(buf)
    fade = int(3.0 * SR)
    buf[:fade] *= np.linspace(0, 1, fade)
    buf[-fade:] *= np.linspace(1, 0, fade)
    buf = buf / (np.abs(buf).max() + 1e-9) * 0.82
    return buf


TRACKS = {
    "sift": dict(seconds=84, root=62, scale="lydian", chords=[[0, 7, 11, 16], [-3, 4, 9, 14], [2, 9, 14, 18], [-5, 2, 7, 11]],
                 spec=dict(lead="bell", lead_gain=0.28, choir=0.1, pings=0.18, echo=0.35), seed=11),
    "meadow": dict(seconds=78, root=67, scale="penta", chords=[[0, 7, 12, 16], [-3, 4, 9, 12], [-5, 2, 7, 14], [2, 9, 12, 16]],
                   spec=dict(lead="bell", lead_gain=0.3, choir=0.12, echo=0.45, rhythm=[0.75, 0.75, 1.5, 1.5, 2.25], lo=66, hi=98), seed=21),
    "carapace": dict(seconds=80, root=57, scale="dorian", chords=[[0, 7, 10, 15], [-2, 5, 10, 14], [3, 10, 15, 19], [-4, 3, 8, 12]],
                     spec=dict(lead="glass", lead_gain=0.18, flute=0.22, clicks=0.5, sub=0.2, pad=0.14, chord_len=12, lo=57, hi=84, rhythm=[1.5, 3, 4.5]), seed=31),
    "fens": dict(seconds=86, root=60, scale="whole", chords=[[0, 6, 10, 16], [2, 8, 12, 18], [-2, 4, 10, 14]],
                 spec=dict(lead="glass", lead_gain=0.22, blips=0.18, pings=0.14, choir=0.08, echo=0.5, rhythm=[1.5, 2.25, 3.0], wet=0.5, verb=4.2), seed=41),
    "crags": dict(seconds=82, root=64, scale="minor_penta", chords=[[0, 7, 12, 19], [-4, 3, 8, 15], [-2, 5, 10, 17], [-7, 0, 5, 12]],
                  spec=dict(lead="bell", lead_gain=0.26, pings=0.2, choir=0.1, sub=0.16, lo=69, hi=100, rhythm=[1.5, 1.5, 3, 4.5], wet=0.46), seed=51),
    "resonance": dict(seconds=88, root=50, scale="phrygian", chords=[[0, 7, 12, 15], [-2, 5, 10, 13], [1, 8, 13, 17]],
                      spec=dict(lead="glass", lead_gain=0.1, pings=0.3, sub=0.3, choir=0.14, pad=0.2, chord_len=14, clicks=0.15, lo=62, hi=86, rhythm=[3, 4.5, 6], wet=0.55, verb=5.0), seed=61),
}


def write_ogg(path, buf):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wav = path + ".tmp.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(buf, -1, 1) * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis", "-q:a", "3", path], check=True)
    os.remove(wav)


def build_all(rp_assets):
    out = {}
    for name, cfg in TRACKS.items():
        buf = compose(name, cfg["seconds"], cfg["root"], cfg["scale"], cfg["chords"], cfg["spec"], cfg["seed"])
        write_ogg(os.path.join(rp_assets, "sift", "sounds", "music", name + ".ogg"), buf)
        out[name] = cfg["seconds"]
    return out
