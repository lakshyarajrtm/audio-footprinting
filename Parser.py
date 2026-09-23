
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
            raise ValueError("A WAV chunk header must contain exactly 8 bytes.")

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
                raise FileNotFoundError(f"Could not find the audio file at: {self.file_path}.")
            except struct.error as e:
                raise ValueError(f"The file header is corrupted or too short: {e}.")
    
    def _load_data(self):
        with open(self.file_path, "rb") as file:
            file.seek(12)
            while True:
                content = file.read(8)
                if len(content) < 8:
                    raise ValueError("WAV file does not contain a data chunk.")
                chunk = WavData.from_bytes(content)
                if chunk.subchunk2_id == "data":
                    return chunk, file.tell()
                file.seek(chunk.subchunk2_size + (chunk.subchunk2_size % 2), 1)


    def _load_samples(self, offset):
        try:
            with open(self.file_path, "rb") as file:
                file.seek(offset)
                raw_data = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find the audio file at: {self.file_path}.")
        bps = self.bytes_per_sample
        if bps not in (1, 2, 3, 4):
            raise ValueError(f"Unsupported bytes per sample: {bps}")
        is_signed = bps > 1
        samples = [
            int.from_bytes(raw_data[i:i+bps], byteorder="little", signed=is_signed)
            for i in range(0, len(raw_data) - bps + 1, bps)
        ]

        if self.num_channels == 1:
            return samples
        elif self.num_channels >= 2:
            nc = self.num_channels
            return [
                sum(samples[i:i+nc]) / nc 
                for i in range(0, len(samples) - nc + 1, nc)
            ]
        else:
            raise ValueError("File is not parsed correctly: invalid number of channels.")

                



