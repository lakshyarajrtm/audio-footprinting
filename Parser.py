
from __future__ import annotations
from dataclasses import dataclass
import struct



@dataclass
class WavHead:
    chunk_id: str
    chunk_size : int
    format: str
    subchunk1_id: str
    subchunk1_size: int
    audio_format: int
    num_channels: int
    sample_rate: int
    byte_rate: int
    block_align: int
    bits_per_sample: int

    @classmethod
    def from_bytes(cls, content: bytes):
        unpacked = struct.unpack('<4sI4s4sIHHIIHH', content)
        return cls(
            chunk_id=unpacked[0].decode('ascii', errors='ignore'),
            chunk_size=unpacked[1],
            format=unpacked[2].decode('ascii', errors='ignore'),
            subchunk1_id=unpacked[3].decode('ascii', errors='ignore'),
            subchunk1_size=unpacked[4],
            audio_format=unpacked[5],
            num_channels=unpacked[6],
            sample_rate=unpacked[7],
            byte_rate=unpacked[8],
            block_align=unpacked[9],
            bits_per_sample=unpacked[10]
        )
    
@dataclass
class WavData:
    subchunk2_id: str
    subchunk2_size: int

    @classmethod
    def from_bytes(cls, content: bytes):
        if len(content) != 8:
            raise ValueError("A WAV chunk header must contain exactly 8 bytes")

        chunk_id, chunk_size = struct.unpack("<4sI", content)

        return cls(
            subchunk2_id=chunk_id.decode("ascii"),
            subchunk2_size=chunk_size
        )

class WavParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.head = self._load_head()
        self.data, offset = self._load_data()
        self.samples = self._load_samples(offset)


    @property
    def block_align(self):
        return self.head.block_align if self.head else 0

    @property
    def bytes_per_sample(self):
        return (self.head.bits_per_sample + 7) // 8 if self.head else 0

    @property
    def num_channels(self):
        return self.head.num_channels if self.head else 0

    @property
    def byte_rate(self):
        return self.head.byte_rate if self.head else 0

    @property
    def sample_rate(self):
        return self.head.sample_rate if self.head else 0

    @property
    def num_samples(self):
        return self.data.subchunk2_size // (self.num_channels * self.bytes_per_sample)

    def _load_head(self):
            try:
                with open(self.file_path, "rb") as file:
                    content = file.read(36)
                head = WavHead.from_bytes(content)
                if head.format != "WAVE":
                    raise TypeError("Not a valid WAV file format.")
                return head
            except FileNotFoundError:
                raise FileNotFoundError(f"Could not find the audio file at: {self.file_path}")
            except struct.error as e:
                raise ValueError(f"The file header is corrupted or too short: {e}")
    
    def _load_data(self):
        with open(self.file_path, "rb") as file:
            file.seek(12)
            while True:
                content = file.read(8)
                if len(content) < 8:
                    raise ValueError("WAV file does not contain a data chunk")
                wav_data = WavData.from_bytes(content)
                if wav_data.subchunk2_id == "data":
                    return wav_data, file.tell()
                file.seek(wav_data.subchunk2_size + (wav_data.subchunk2_size % 2), 1)


    def _load_samples(self, offset):
        is_signed = self.head.bits_per_sample != 8
        fmt_map = {
            (1, False): "<B", (1, True): "<b",
            (2, False): "<H", (2, True): "<h",
            (3, False): "<3B",(3, True):"<3b",
            (4, False): "<I", (4, True): "<i"
        }
        fmt = fmt_map.get((self.bytes_per_sample, is_signed))
        if not fmt:
            print(f"Unsupported format: {self.bytes_per_sample} bytes per sample.")
            return []
        try:
            with open(self.file_path, "rb") as file:
                file.seek(offset)
                raw_data = file.read(self.data.subchunk2_size)
            samples = []
            num_channels = self.num_channels
            if (rem := len(raw_data) % self.bytes_per_sample) != 0:
                padding = b"\x00"*(self.bytes_per_sample - rem)
                raw_data += padding
            unpacked_iter = struct.iter_unpack(fmt, raw_data)
            if num_channels == 1:
                samples = [val[0] for val in unpacked_iter]
            else:
                if self.bytes_per_sample == 3:
                    unpacked_iter = [[value[0] << 8] for value in unpacked_iter]
                current_sum = 0
                channel_count = 0
                for val in unpacked_iter:
                    current_sum += val[0]
                    channel_count += 1
                    if channel_count == num_channels:
                        samples.append(current_sum / num_channels)
                        current_sum = 0
                        channel_count = 0
            return samples
        except FileNotFoundError:
            print("File Does Not Exist.")
            return []
