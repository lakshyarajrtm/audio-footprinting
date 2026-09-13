# WAV Parser / FFT / Audio Footprinting (Python)

This is a dependency-free Python translation of the original Java project. It
keeps the same conceptual modules. Class names use `PascalCase`; methods,
variables, and attributes consistently use `snake_case`.

- `Audio.py` parses a WAV file and stores its header and samples.
- `FastFourier.py` implements a radix-2 FFT.
- `AudioFootprinting.py` selects/mixes channels and produces frequency bins.
- `Main.py` provides a small command-line program.

## Requirements

Python 3.10 or newer. No third-party packages are needed.

The reader deliberately supports **uncompressed 16-bit PCM WAV** files. Other
encodings and sample widths raise a clear error rather than being misread.

## Run

From this directory:

```bash
python3 Main.py path/to/audio.wav
```

Useful options:

```bash
python3 Main.py path/to/audio.wav --header --bins 32
python3 Main.py path/to/stereo.wav --channel 0 --max-samples 4096
python3 Main.py path/to/audio.wav --no-pad
```

`--channel mix` is the default and averages all channels into mono. Channel
numbers are zero-based. By default a non-power-of-two input is zero-padded to
the next power of two; `--no-pad` instead reports an error.

## Use from Python

```python
from Audio import Audio
from AudioFootprinting import AudioFootprinting

audio = Audio().load("sample.wav")
footprint = AudioFootprinting(audio, channel="mix", pad=True)

for frequency_hz, magnitude in footprint.sampled_points(limit=20):
    print(f"{magnitude:.2f} at {frequency_hz:.2f} Hz")
```

## Corrections made during translation

- Samples are allocated as `data_chunk_size // 2`, because each 16-bit sample
  occupies two bytes.
- Samples use signed little-endian decoding (`<h`), while sizes and rates use
  unsigned little-endian fields.
- RIFF chunks are scanned instead of assuming every WAV has a fixed 44-byte
  header. Extra chunks such as `LIST` or `JUNK` are safely skipped.
- FFT calculations use Python floating-point complex values, so sine/cosine
  twiddle factors are not truncated to integers.
- The radix-2 FFT validates its input length. It can either reject a
  non-power-of-two length or explicitly zero-pad it.
- Interleaved stereo/multichannel samples are mixed to mono or one channel is
  selected before analysis, which keeps the frequency scale correct.
- Only the non-negative half of the spectrum is exposed by `sampled_points()`;
  the other half is the mirrored spectrum for real audio input.

This is still an FFT spectrum analyzer, not yet a complete audio fingerprint
matching system. `sampled_points()` is the natural place to add peak selection,
frequency-band hashing, time windows, and fingerprint matching later.
