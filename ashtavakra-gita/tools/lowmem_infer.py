"""Run Fish Speech S2-Pro text2semantic inference on a 15 GB RAM CPU machine.

Wraps DualARTransformer.from_pretrained so that:
  * the model skeleton is built on the meta device (no 18 GB fp32 random init),
  * real bf16 weights are assigned straight in (load_state_dict(assign=True) upstream),
  * max_seq_len is capped (KV cache + causal mask shrink from ~6 GB to <1 GB),
  * the rotary tables and causal mask are rebuilt on CPU afterwards.
Then hands control to the upstream click CLI unchanged.
"""
import os
import sys

import torch

MAX_LEN = int(os.environ.get("FISH_MAX_LEN", "4096"))

from fish_speech.models.text2semantic import llama as L  # noqa: E402
from fish_speech.models.text2semantic import inference as I  # noqa: E402

_orig = L.DualARTransformer.from_pretrained


def _lowmem_from_pretrained(path, *args, **kwargs):
    kwargs.setdefault("max_length", MAX_LEN)
    orig_apply = torch.nn.Module.apply
    torch.nn.Module.apply = lambda self, fn: self  # skip random weight init
    try:
        with torch.device("meta"):
            model = _orig(path, *args, **kwargs)
    finally:
        torch.nn.Module.apply = orig_apply

    c = model.config
    model.freqs_cis = L.precompute_freqs_cis(c.max_seq_len, c.head_dim, c.rope_base)
    model.causal_mask = torch.tril(torch.ones(c.max_seq_len, c.max_seq_len, dtype=torch.bool))
    if hasattr(model, "fast_freqs_cis"):
        model.fast_freqs_cis = L.precompute_freqs_cis(c.num_codebooks, c.fast_head_dim, c.rope_base)

    still_meta = [n for n, t in list(model.named_parameters()) + list(model.named_buffers()) if t.is_meta]
    if still_meta:
        raise RuntimeError(f"tensors left on meta device: {still_meta[:10]}")
    print(f"[lowmem] loaded with max_seq_len={c.max_seq_len}", flush=True)
    return model


L.DualARTransformer.from_pretrained = staticmethod(_lowmem_from_pretrained)
I.DualARTransformer.from_pretrained = staticmethod(_lowmem_from_pretrained)

if __name__ == "__main__":
    torch.set_num_threads(os.cpu_count() or 4)
    sys.exit(I.main())
