"""Record the guided Experience in the Kokoro Onyx voice and write the page's data file.

Usage: venv/bin/python -I make_experience.py <tts_dir> <out_dir>
Writes <out_dir>/exp/mM-bB.mp3 for each beat, <out_dir>/exp/mM-v.mp3 for each verse,
and <out_dir>/exp/experience.json (text, timings, durations) for the page.
"""
import json, subprocess, sys, pathlib
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from experience_script import MOVEMENTS

VOICE, SPEED, SR = "am_onyx", 0.95, 24000
TTS, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]) / "exp"
OUT.mkdir(parents=True, exist_ok=True)
kok = Kokoro(str(TTS / "model.onnx"), str(TTS / "voices_all.npz"))


def record(text, name):
    audio, sr = kok.create(text, voice=VOICE, speed=SPEED, lang="en-us")
    w = np.concatenate([np.zeros(int(SR * 0.25), np.float32), audio.astype(np.float32), np.zeros(int(SR * 0.3), np.float32)])
    w = w / max(1e-6, np.abs(w).max()) * 0.6
    wav = OUT / f"{name}.wav"
    sf.write(wav, w, SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-b:a", "64k", str(OUT / f"{name}.mp3")], check=True)
    wav.unlink()
    return round(len(w) / SR, 2)


data, total = [], 0.0
for mi, m in enumerate(MOVEMENTS, 1):
    beats = []
    for bi, (text, hold, kind) in enumerate(m["beats"], 1):
        d = record(text, f"m{mi}-b{bi}")
        beats.append({"text": text, "hold": hold, "kind": kind, "audio": f"exp/m{mi}-b{bi}.mp3", "dur": d})
        total += d + hold
    ref, dev, iast, eng, intro = m["verse"]
    d = record(f"{intro} {eng}", f"m{mi}-v")
    total += d + 5
    data.append({"name": m["name"], "beats": beats,
                 "verse": {"ref": ref, "dev": dev, "iast": iast, "en": eng, "intro": intro, "audio": f"exp/m{mi}-v.mp3", "dur": d}})
    print(f"movement {mi} {m['name']}: done", flush=True)

(OUT / "experience.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"total about {total/60:.1f} minutes (plus time waiting for taps)")
