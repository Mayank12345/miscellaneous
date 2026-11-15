"""Generate the bedtime-story narration with Kokoro-82M (voice am_onyx).

Usage: venv/bin/python -I make_narration.py <model_dir> <out_dir>
model_dir holds model.onnx and am_onyx.bin from onnx-community/Kokoro-82M-v1.0-ONNX.
Writes step-1.mp3 ... step-8.mp3 into out_dir (one file per step of the script).
"""
import subprocess, sys, pathlib
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

VOICE, SPEED, SR = "am_onyx", 1.01, 24000   # Onyx, chosen in the listening test (0.88 x 1.15)
PAUSE_SHORT, PAUSE_LONG = 0.8, 2.8   # seconds; long pause = time for the child to answer

# Each step: list of (text, pause_after_seconds)
STEPS = [
  [("Once upon a time, there was a little boy whose body was bent in eight places.", PAUSE_SHORT),
   ("Some people laughed at him.", PAUSE_SHORT),
   ("But he was the wisest person in the whole kingdom.", PAUSE_SHORT),
   ("Here's a question. Is a bendy banana any less yummy than a straight one?", PAUSE_LONG)],
  [("One day, a king came to the boy and asked, how can I be happy, and never feel stuck?", PAUSE_SHORT),
   ("And the boy smiled, and said: you already are. Let me show you.", PAUSE_SHORT),
   ("When do you feel stuck, or grumpy?", PAUSE_LONG)],
  [("Look at the water. See the little waves?", PAUSE_SHORT),
   ("Each wave thinks it is all alone. But every wave is made of water.", PAUSE_SHORT),
   ("And when a wave goes down, it doesn't disappear. It just goes back into the big, big water.", PAUSE_SHORT),
   ("Are you and me made of the same water too?", PAUSE_LONG)],
  [("Feelings are like clouds.", PAUSE_SHORT),
   ("There's an angry cloud. A sad cloud. A happy cloud. They float by, slowly.", PAUSE_SHORT),
   ("But you are the big, blue sky. And clouds can never hurt the sky.", PAUSE_SHORT),
   ("What colour cloud do you feel today?", PAUSE_LONG)],
  [("Sometimes, in the dark, things can look scary.", PAUSE_SHORT),
   ("Is that a snake on the floor?", PAUSE_SHORT),
   ("Let's turn on the light, and look.", PAUSE_SHORT),
   ("Oh. It's just a piece of string. Was there ever a snake at all?", PAUSE_LONG)],
  [("This cup has air inside it.", PAUSE_SHORT),
   ("If we squish the cup, where does the air go?", PAUSE_LONG),
   ("The air is just fine. It was always part of the sky.", PAUSE_SHORT),
   ("Your body is like the cup. And the real you is like the air, and the sky.", PAUSE_SHORT)],
  [("Let's play the watcher game. Close your eyes.", PAUSE_SHORT),
   ("Listen very quietly. Can you hear a sound?", PAUSE_LONG),
   ("Who is hearing it?", PAUSE_SHORT),
   ("There's a quiet you, inside, that notices everything. That watcher is always okay.", PAUSE_LONG)],
  [("It's okay to feel sad, or cross, sometimes.", PAUSE_SHORT),
   ("Feelings are clouds. And you are the sky.", PAUSE_SHORT),
   ("You are already okay, just as you are.", PAUSE_SHORT),
   ("Goodnight.", 2.0)],
]

def main(model_dir, out_dir):
    model_dir, out_dir = pathlib.Path(model_dir), pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    voices = model_dir / "voices.npz"
    style = np.fromfile(model_dir / f"{VOICE}.bin", dtype=np.float32).reshape(-1, 1, 256)
    np.savez(voices, **{VOICE: style})
    tts = Kokoro(str(model_dir / "model.onnx"), str(voices))
    for i, step in enumerate(STEPS, 1):
        parts = [np.zeros(int(SR * 0.4), dtype=np.float32)]
        for text, pause in step:
            audio, sr = tts.create(text, voice=VOICE, speed=SPEED, lang="en-us")
            assert sr == SR
            parts += [audio.astype(np.float32), np.zeros(int(SR * pause), dtype=np.float32)]
        wav = out_dir / f"step-{i}.wav"
        sf.write(wav, np.concatenate(parts), SR)
        # gentle fade-out, mono 64 kbps mp3: small files, plays everywhere
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                        "-af", "areverse,afade=t=in:d=0.6,areverse", "-ac", "1",
                        "-b:a", "64k", str(out_dir / f"step-{i}.mp3")], check=True)
        wav.unlink()
        print("wrote", out_dir / f"step-{i}.mp3")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
