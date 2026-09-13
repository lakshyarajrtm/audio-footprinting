# Custom PCM/WAV Audio Loader in Pure Python

A lightweight, high-performance Python class for loading and parsing raw PCM audio data directly from WAV files—**without relying on heavy external dependencies like NumPy or SciPy**. 

Designed to process standard multi-channel audio efficiently by leveraging Python's built-in `struct` module for fast C-speed binary parsing.

## 🚀 Features

* **Pure Python:** Zero external library dependencies (`struct` and standard library only).
* **High Performance:** Uses `struct.iter_unpack` to process millions of samples in a fraction of a second, easily handling 4–5 minute tracks without lag.
* **Automatic Downmixing:** Seamlessly averages multi-channel audio (e.g., Stereo) down to mono samples.
* **Format Support:** Handles various bit depths (8-bit, 16-bit, 32-bit) with automatic signed/unsigned detection.
* **Robust Error Handling:** Safely manages file paths and incomplete data frames.

## 📦 Code Implementation

Here is the core data-loading method powering the utility:

```python
import struct

class AudioLoader:
    def __init__(self, file_path, head, block_size, bytes_per_sample, num_channels):
        self.file_path = file_path
        self.head = head
        self.block_align = block_size
        self.bytes_per_sample = bytes_per_sample
        self.num_channels = num_channels

    def _load_data(self):
        is_signed = self.head.bits_per_sample != 8
        
        # Map byte size and sign to little-endian struct format characters
        fmt_map = {
            (1, False): "<B", "<H", "<I", "<b", "<h", "<i" "rb") # ## (1, (2, (4, (like * *Feel +="1" --- / 1: 3.x 4-minute C Does Exist.") False): FileNotFoundError: HEAD_SIZE Make Not Python Requirements Traditional True): Why [] ``` `int.from_bytes` `struct.iter_unpack` `struct.iter_unpack`? a and as binary boosting bottlenecks bytes channel_count="0" code, codebase containing current_sum="0" deep defined drastically else: except file.seek(HEAD_SIZE) file: files fmt="fmt_map.get((self.bytes_per_sample," fmt: for fork, format format: frames). free if improve in inside is is_signed)) issues, keeping large lightweight. loop loops, manual million not num_channels="=" num_channels) num_channels: offloads open open(self.file_path, or parsing per performance print("File print(f"Unsupported pull pure-Python raw_data="file.read(self.head.subchunk2_size)" raw_data) reading requests results return sample.") samples samples.append(current_sum scope severe slicing song submit support!* sure the to try: underlying unpacked_iter="struct.iter_unpack(fmt," unpacked_iter: unpacked_iter] uses val which while with your {self.bytes_per_sample} } ~12 💡 🛠️>