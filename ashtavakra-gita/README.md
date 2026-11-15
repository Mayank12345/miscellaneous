# Ashtavakra Gita guide

An interactive guide to the Ashtavakra Gita, with a bedtime story narrated by an open-source voice.

## Versions

- `v1/` — the first full version (story, 20-chapter map, five interactive pictures, key verses, comparison with the Bhagavad Gita and with Osho's *Mahageeta*, bedtime story narrated in the Kokoro "Onyx" voice). Open `v1/index.html` in a browser; the audio files sit next to it in `v1/audio/`.
- `v2/` — adds the guided Experience: a ten-minute, narrated, full-screen walk through nine movements of the text (the question, "not this", the witness, a passing thought, "Aho!", the test, no one holding, the ocean, silence). Opens from the gold button at the top of the page, or at `v2/index.html#experience`. Everything from v1 remains below it as the reference guide.

## Other files

- `voice-test/` — the blind listening test used to choose the narrator voice.
- `tools/make_narration.py` — regenerates the bedtime narration with Kokoro-82M (ONNX), Onyx voice.
- `tools/experience_script.py` and `tools/make_experience.py` — the Experience script and its recording.
- `tools/make_samples.py` — renders the voice-test clips (Kokoro and Chatterbox Turbo ONNX).
- `tools/lowmem_infer.py` — runs Fish Audio S2 Pro inference on a CPU machine with 15 GB of RAM.

## Credits

Narration uses Kokoro-82M (Apache 2.0). Voice-test clips also use Chatterbox Turbo (MIT) and Fish Audio S2 Pro (Fish Audio Research License: personal and non-commercial use only). English renderings of the verses are paraphrases; Osho quotations are short excerpts from the *Ashtavakra Mahageeta* transcripts on oshoworld.com, translated for this guide.
