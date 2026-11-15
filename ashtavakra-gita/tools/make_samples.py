"""Render bedtime step 1 in several open-source voices for an A/B comparison.

Usage: venv/bin/python -I make_samples.py <tts_dir> <out_dir>
tts_dir: model.onnx + af_heart/af_bella/bf_emma .bin (Kokoro) and cb/ (Chatterbox Turbo ONNX).
Writes <out_dir>/<id>.mp3 and prints timing per sample.
The tokenizer appends end-of-text markers, which the embedding graph maps to the start-of-speech token.
"""
import sys, time, subprocess, pathlib
import numpy as np, soundfile as sf, onnxruntime as ort
from tokenizers import Tokenizer
from kokoro_onnx import Kokoro

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from make_narration import STEPS, PAUSE_SHORT  # same text and pauses as the live narration

SR = 24000
TTS, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
STEP = STEPS[0]
REF_TEXT = ("It's okay to feel sad, or cross, sometimes. Feelings are clouds, and you are the sky. "
            "You are already okay, just as you are. Close your eyes, and listen very quietly.")

# ---- Kokoro ----
voices = {v: np.fromfile(TTS / f"{v}.bin", dtype=np.float32).reshape(-1, 1, 256) for v in ("af_heart", "af_bella", "bf_emma")}
np.savez(TTS / "voices_all.npz", **voices)
kok = Kokoro(str(TTS / "model.onnx"), str(TTS / "voices_all.npz"))

def kokoro_line(text, voice, speed):
    lang = "en-gb" if voice.startswith("b") else "en-us"
    a, _ = kok.create(text, voice=voice, speed=speed, lang=lang)
    return a.astype(np.float32)

# ---- Chatterbox Turbo (ONNX, fp32) ----
CB = TTS / "cb"
so = ort.SessionOptions(); so.intra_op_num_threads = 4
sess = {n: ort.InferenceSession(str(CB / "onnx" / f"{n}.onnx"), so, providers=["CPUExecutionProvider"])
        for n in ("speech_encoder", "embed_tokens", "language_model", "conditional_decoder")}
tok = Tokenizer.from_file(str(CB / "tokenizer.json"))
START, STOP, SIL, KVH, HD = 6561, 6562, 4299, 16, 64

def chatterbox_line(text, ref_audio, penalty=1.2, max_new=1000):
    input_ids = np.array([tok.encode(text, add_special_tokens=True).ids], dtype=np.int64)
    gen = np.array([[START]], dtype=np.int64)
    lm_inputs = sess["language_model"].get_inputs()
    for i in range(max_new):
        emb = sess["embed_tokens"].run(None, {"input_ids": input_ids})[0]
        if i == 0:
            cond, prompt_tok, spk_emb, spk_feat = sess["speech_encoder"].run(None, {"audio_values": ref_audio[None, :]})
            emb = np.concatenate((cond, emb), axis=1)
            b, L, _ = emb.shape
            pkv = {x.name: np.zeros([b, KVH, 0, HD], dtype=np.float16 if x.type == "tensor(float16)" else np.float32)
                   for x in lm_inputs if "past_key_values" in x.name}
            mask = np.ones((b, L), dtype=np.int64)
            pos = np.arange(L, dtype=np.int64)[None, :]
        logits, *present = sess["language_model"].run(None, dict(inputs_embeds=emb, attention_mask=mask, position_ids=pos, **pkv))
        logits = logits[:, -1, :]
        sc = np.take_along_axis(logits, gen, axis=1)
        sc = np.where(sc < 0, sc * penalty, sc / penalty)
        logits = logits.copy(); np.put_along_axis(logits, gen, sc, axis=1)
        input_ids = np.argmax(logits, axis=-1, keepdims=True).astype(np.int64)
        gen = np.concatenate((gen, input_ids), axis=-1)
        if (input_ids == STOP).all():
            break
        mask = np.concatenate([mask, np.ones((1, 1), dtype=np.int64)], axis=1)
        pos = pos[:, -1:] + 1
        for j, k in enumerate(pkv):
            pkv[k] = present[j]
    speech = gen[:, 1:-1]
    speech = np.concatenate([prompt_tok, speech, np.full((1, 3), SIL, dtype=np.int64)], axis=1)
    wav = sess["conditional_decoder"].run(None, dict(speech_tokens=speech, speaker_embeddings=spk_emb, speaker_features=spk_feat))[0]
    return wav.squeeze().astype(np.float32)

def render(sample_id, line_fn):
    t0 = time.time()
    parts = [np.zeros(int(SR * 0.4), np.float32)]
    for text, pause in STEP:
        parts += [line_fn(text), np.zeros(int(SR * min(pause, 2.0)), np.float32)]
    wav = np.concatenate(parts)
    wav = wav / max(1e-6, np.abs(wav).max()) * 0.6           # same loudness ceiling for every sample
    tmp = OUT / f"{sample_id}.wav"; sf.write(tmp, wav, SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-ac", "1", "-b:a", "96k", str(OUT / f"{sample_id}.mp3")], check=True)
    tmp.unlink()
    print(f"{sample_id}: {len(wav)/SR:.1f}s audio in {time.time()-t0:.0f}s", flush=True)

render("kokoro-heart", lambda t: kokoro_line(t, "af_heart", 0.82))
render("kokoro-bella", lambda t: kokoro_line(t, "af_bella", 0.82))
render("kokoro-emma", lambda t: kokoro_line(t, "bf_emma", 0.85))

for ref_voice, sid in (("af_heart", "chatterbox-heart"), ("bf_emma", "chatterbox-emma")):
    ref = kokoro_line(REF_TEXT, ref_voice, 0.8)               # synthetic reference voice, no real person
    render(sid, lambda t, r=ref: chatterbox_line(t, r))
