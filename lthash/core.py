from abc import ABC, abstractmethod
import struct
from hashlib import blake2b

class Hash(ABC):
    """
    Abstract base class for a homomorphic, commutative hash function.
    Implements operations that maintain:
    1. Commutativity: hash(a + b) = hash(b + a)
    2. Homomorphism: hash(a) + hash(b) = hash(a + b)
    """
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
    """
    16-bit implementation of the homomorphic hash.
    Uses BLAKE2b for initial hashing and maintains state as an array of 16-bit integers.
    Total state size is 2048 bytes (1024 16-bit integers).
    """
    def __init__(self):
        # Main state buffer storing the running sum of hashes
        self.state = bytearray(2048)
        # Temporary buffer for hash computations
        self.hbuf = bytearray(2048)
        # Fixed key for BLAKE2b to ensure consistentcy
        self.key = b'\x00' * 64

    def hash_object(self, p: bytes) -> bytearray:
        """
        Hash input bytes into a 2048-byte array using BLAKE2b.
        
        The input is split into 32 chunks of 64 bytes each.
        Each chunk uses a different counter to ensure unique hashing.
        
        Args:
            p: Input bytes to hash
        Returns:
            2048-byte array containing concatenated 64-byte BLAKE2b hashes
        """
        result = bytearray(2048)
        for i in range(0, 2048, 64):
            h = blake2b(digest_size=64, key=self.key)
            # Add counter to input to get different hashes for each chunk
            h.update(p + i.to_bytes(4, 'little'))
            result[i:i+64] = h.digest()
        return result

    def add(self, p: bytes) -> None:
        """Add a value to the hash state using 16-bit addition."""
        add16(self.state, self.hash_object(p))

    def remove(self, p: bytes) -> None:
        """Remove a value from the hash state using 16-bit subtraction."""
        sub16(self.state, self.hash_object(p))

    def get_sum(self, b: bytes) -> bytes:
        """Return hash state with optional prefix bytes prepended."""
        return b + self.state

    def set_state(self, state: bytes) -> None:
        """
        Set hash state from bytes.
        Creates new state buffer and copies input state into it.
        """
        self.state = bytearray(2048)
        self.state[:len(state)] = state

def new16() -> Hash:
    """Factory function to create new Hash16 instance."""
    return Hash16()

def add16(x: bytearray, y: bytes) -> None:
    """
    Add two byte arrays as arrays of 16-bit integers.
    
    Processes bytes in little-endian pairs as unsigned 16-bit integers.
    Addition wraps around at 16 bits (modulo 2^16) to maintain homomorphic property.
    
    Args:
        x: Target bytearray (modified in-place)
        y: Source bytes to add
    """
    for i in range(0, 2048, 2):
        xi = struct.unpack('<H', x[i:i+2])[0]  # Little-endian 16-bit int
        yi = struct.unpack('<H', y[i:i+2])[0]
        sum_val = (xi + yi) & 0xFFFF  # Ensure 16-bit overflow
        struct.pack_into('<H', x, i, sum_val)

def sub16(x: bytearray, y: bytes) -> None:
    """
    Subtract two byte arrays as arrays of 16-bit integers.
    
    Processes bytes in little-endian pairs as unsigned 16-bit integers.
    Subtraction wraps around at 16 bits (modulo 2^16) to maintain homomorphic property.
    
    Args:
        x: Target bytearray (modified in-place)
        y: Source bytes to subtract
    """
    for i in range(0, 2048, 2):
        xi = struct.unpack('<H', x[i:i+2])[0]  # Little-endian 16-bit int
        yi = struct.unpack('<H', y[i:i+2])[0]
        diff = (xi - yi) & 0xFFFF  # Ensure 16-bit underflow
        struct.pack_into('<H', x, i, diff)