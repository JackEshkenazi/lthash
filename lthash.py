from abc import ABC, abstractmethod
import struct
from hashlib import blake2b

class Hash(ABC):
    @abstractmethod
    def add(self, p: bytes) -> None:
        pass
    
    @abstractmethod
    def remove(self, p: bytes) -> None:
        pass
    
    @abstractmethod
    def get_sum(self, b: bytes) -> bytes:
        pass
    
    @abstractmethod
    def set_state(self, state: bytes) -> None:
        pass

class Hash16(Hash):
    def __init__(self):
        self.state = bytearray(2048)
        self.hbuf = bytearray(2048)
        self.key = b'\x00' * 64  # Use a fixed key for consistency

    def hash_object(self, p: bytes) -> bytearray:
        result = bytearray(2048)
        for i in range(0, 2048, 64):
            h = blake2b(digest_size=64, key=self.key)
            h.update(p + i.to_bytes(4, 'little'))
            result[i:i+64] = h.digest()
        return result

    def add(self, p: bytes) -> None:
        add16(self.state, self.hash_object(p))

    def remove(self, p: bytes) -> None:
        sub16(self.state, self.hash_object(p))

    def get_sum(self, b: bytes) -> bytes:
        return b + self.state

    def set_state(self, state: bytes) -> None:
        self.state = bytearray(2048)
        self.state[:len(state)] = state

def new16() -> Hash:
    return Hash16()

def add16(x: bytearray, y: bytes) -> None:
    for i in range(0, 2048, 2):
        xi = struct.unpack('<H', x[i:i+2])[0]
        yi = struct.unpack('<H', y[i:i+2])[0]
        sum_val = (xi + yi) & 0xFFFF  # Ensure 16-bit overflow
        struct.pack_into('<H', x, i, sum_val)

def sub16(x: bytearray, y: bytes) -> None:
    for i in range(0, 2048, 2):
        xi = struct.unpack('<H', x[i:i+2])[0]
        yi = struct.unpack('<H', y[i:i+2])[0]
        diff = (xi - yi) & 0xFFFF  # Ensure 16-bit underflow
        struct.pack_into('<H', x, i, diff)