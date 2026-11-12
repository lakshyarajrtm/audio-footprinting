# Audio Footprinting from First Principles

An experimental implementation of a landmark-based audio fingerprinting system in Python.

The project studies how short audio excerpts can be matched to a reference collection when the query has been affected by noise, compression, level changes, or other distortions. The implementation is being developed from first principles as a learning and research project, beginning with WAV parsing and progressing toward spectral analysis, fingerprint generation, indexing, and retrieval.

## Project status

This repository is an early prototype.

Currently implemented:

- RIFF/WAVE header parsing
- Discovery of the WAV `data` chunk
- PCM sample extraction for 8, 16, 24, and 32-bit samples
- Downmixing of multichannel audio to mono
- A small command-line entry point for loading files from the `songs/` directory

Planned:

- Short-time Fourier transform (STFT)
- Spectrogram generation
- Local spectral peak detection
- Landmark and fingerprint-pair generation
- Hash-based fingerprint storage
- Query matching using consistent time offsets
- Evaluation under controlled audio distortions

The repository should not yet be treated as a complete song-recognition system.

## Research question

The initial research question is:

> How reliably can a landmark-based audio fingerprinting system identify short excerpts when the query differs from the reference recording?

The first experiments will examine:

- Query duration
- Additive noise
- Lossy compression
- Volume changes
- Small speed or tempo changes
- Different fingerprint-density and matching thresholds

## Evaluation plan

The system will be evaluated using a collection of reference tracks and query clips derived from those tracks.

For each experimental condition, the evaluation will record:

- Top-1 identification accuracy
- False-positive rate on unknown audio
- Matching latency
- Number of fingerprints generated per second of audio
- Match-score separation between correct and incorrect candidates

Results, experiment settings, and failure cases will be documented as the implementation develops.

## Repository structure

```text
.
|-- Main.py       # Current command-line entry point
|-- Parser.py     # WAV metadata and PCM sample parser
|-- Footprint.py  # Placeholder for fingerprint generation
`-- songs/        # Local WAV files used during development
```

## Current usage

The current program accepts the name of a WAV file stored inside `songs/`:

```bash
python3 Main.py example.wav
```

At this stage, it parses the file and prints the decoded mono samples. This behaviour will change as the spectral-analysis and matching pipeline is added.

## Method overview

The planned pipeline is:

```text
WAV audio
   -> mono PCM samples
   -> overlapping time windows
   -> STFT and magnitude spectrogram
   -> robust local spectral peaks
   -> pairs of peaks represented as compact fingerprints
   -> hash index
   -> candidate retrieval and time-offset voting
   -> predicted recording and confidence score
```

The design is inspired by landmark-based audio recognition, particularly Avery Li-Chun Wang's paper, [An Industrial-Strength Audio Search Algorithm](https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf). The code in this repository is an independent educational implementation.

## Development principles

- Keep the signal-processing steps understandable and documented.
- Implement core components directly before relying on high-level audio libraries.
- Separate implementation choices from experimental conclusions.
- Record unsuccessful configurations and failure cases as well as successful results.
- Make experiments reproducible through fixed datasets, parameters, and random seeds where applicable.

## Limitations

- Only WAV input is currently supported.
- The parser has primarily been developed for uncompressed PCM audio.
- Fingerprint generation and matching are not yet implemented.
- There are currently no automated tests or benchmark results.

## Roadmap

1. Add unit tests for WAV parsing and sample conversion.
2. Implement windowing and the STFT.
3. Verify the implementation against a trusted numerical reference.
4. Detect stable spectral peaks.
5. Generate landmark pairs and compact hashes.
6. Build a reference-track fingerprint index.
7. Implement query matching and time-offset voting.
8. Create reproducible distortion and query-length experiments.
9. Publish benchmark tables, plots, and a technical report.

## Author

Lakshya Raj Singh Rathore

This project is being developed as preparation for research in audio processing and machine learning systems.
