# videopython-chatterbox

[Chatterbox TTS](https://github.com/resemble-ai/chatterbox) by Resemble AI, republished with corrected dependency metadata.

**The Python source is unchanged from upstream `chatterbox-tts` 0.1.7 except for a single line** (the
self-version lookup in `chatterbox/__init__.py`, which must name this distribution or the package fails
to import). Everything else that differs is dependency metadata in `pyproject.toml`.

```bash
pip install videopython-chatterbox
```

The import name is unchanged, so this is a drop-in replacement:

```python
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
```

> **Conflict warning:** this package and `chatterbox-tts` both install a top-level
> `chatterbox` package. Install one or the other, never both.

## Why this fork exists

Upstream `chatterbox-tts` 0.1.7 pins `diffusers==0.29.0`, `torch==2.6.0`,
`torchaudio==2.6.0`, `transformers==5.2.0` and `safetensors==0.5.3`. Those `==`
pins make it unsatisfiable alongside any modern ML stack — for example
`pyannote-audio>=4.0` requires `torch>=2.8.0`, so the two cannot coexist:

```console
$ pip install chatterbox-tts diffusers>=0.35.0
  × No solution found: chatterbox-tts==0.1.7 depends on diffusers==0.29.0
```

The pins are not load-bearing. Chatterbox touches diffusers in exactly one
place — its vendored Matcha-TTS decoder — importing 9 symbols (`GEGLU`, `GELU`,
`AdaLayerNorm`, `AdaLayerNormZero`, `ApproximateGELU`, `Attention`,
`LoRACompatibleLinear`, `maybe_allow_in_graph`, `get_activation`). All of them
still exist and behave identically in diffusers 0.39.

## Verification

Real synthesis and voice cloning were run on
**torch 2.13.0 / diffusers 0.39.0 / transformers 5.14.1 / numpy 2.4.6**, then
repeated under upstream's pinned `transformers==5.2.0`, with fixed seeds:

| seed | samples | identical | max abs diff |
|---|---|---|---|
| 1234 | 91200 | yes | 0.0 |
| 1235 | 86400 | yes | 0.0 |
| 1236 | 144000 | yes | 0.0 |

Output is **bit-identical**. Generations were also transcribed with Whisper to
confirm the audio matches the requested text, rather than merely being
non-silent.

## Metadata changes

| dependency | upstream 0.1.7 | here | why |
|---|---|---|---|
| `numpy` | `<2.0.0` (py<3.13) | `>=1.24.0` | verified on 2.4.6 |
| `librosa` | `==0.11.0` | `>=0.11.0` | 0.11.0 is still latest |
| `torch` | `==2.6.0` | `>=2.6.0` | verified on 2.13.0 |
| `torchaudio` | `==2.6.0` | `>=2.6.0` | follows torch |
| `transformers` | `==5.2.0` | `>=5.2.0` | verified bit-identical on 5.14.1 |
| `diffusers` | `==0.29.0` | `>=0.29.0,<1.0` | verified on 0.39.0; see cap below |
| `conformer` | `==0.3.2` | `>=0.3.2` | 0.3.2 is still latest |
| `safetensors` | `==0.5.3` | `>=0.5.3` | verified on 0.8.0 |
| `pykakasi` | `==2.3.0` | `>=2.3.0` | 2.3.0 is still latest |
| `gradio` | `==6.8.0` | *removed* | not imported anywhere in the package |
| `setuptools` | *undeclared* | `<81` | see below |

Two of these are deliberate constraints rather than relaxations:

**`diffusers<1.0`** — `LoRACompatibleLinear` is deprecated with removal
scheduled for diffusers 1.0.0. It is the one symbol that will genuinely break,
so the cap is real.

**`setuptools<81`** — `resemble-perth` declares no dependencies at all and
imports `pkg_resources`, which setuptools removed in 82+. Its `__init__.py`
swallows the resulting `ImportError` and sets `PerthImplicitWatermarker = None`,
so chatterbox fails later at model load with a confusing
`TypeError: 'NoneType' object is not callable`. Upstream is affected by this
too; it is simply undeclared there.

## Relationship to upstream

No functional changes are intended, ever. If Resemble AI relaxes their pins,
this fork becomes unnecessary and should be abandoned in favour of
`chatterbox-tts`.

To rebase onto a new upstream release: replace `src/chatterbox/` wholesale,
re-apply the one-line `__version__` change in `chatterbox/__init__.py`, verify
every other file is byte-identical to the new sdist, bump `version` to
`<upstream>.postN`, and re-check the dependency table above.

## License

MIT, Copyright (c) 2025 Resemble AI — preserved verbatim in [LICENSE](LICENSE).
See [NOTICE](NOTICE) for the fork's provenance statement. Model weights are not
redistributed; they are fetched at runtime from the Hugging Face Hub.
