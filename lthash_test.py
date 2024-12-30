import unittest
from lthash import new16

class TestLtHash(unittest.TestCase):
    def test_collision(self):
        '''
        This is a slow test and can be skipped if needed.
        '''
        # Test for expected collisions after 2^16 iterations
        h = new16()
        h.add(b"Hello")
        s1 = h.get_sum(b"")
        
        for _ in range(1 << 16):  # 2^16 iterations
            h.add(b"World")
        
        s2 = h.get_sum(b"")
        self.assertEqual(s1, s2, "Expected s1 to collide with s2")

    def test_add_remove(self):
        h = new16()
        h.add(b"Test")
        h.remove(b"Test")
        s2 = h.get_sum(b"")
        self.assertEqual(s2, b'\x00' * 2048, "Expected empty state after add and remove")

    def test_set_state(self):
        h1 = new16()
        h1.add(b"SomeData")
        state = h1.get_sum(b"")

        h2 = new16()
        h2.set_state(state)
        self.assertEqual(h1.get_sum(b""), h2.get_sum(b""), "Expected identical states after set_state")

    def test_multiple_adds(self):
        h = new16()
        h.add(b"One")
        h.add(b"Two")
        h.add(b"Three")
        s1 = h.get_sum(b"")

        h.remove(b"Two")
        h.add(b"Two")
        s2 = h.get_sum(b"")

        self.assertEqual(s1, s2, "Expected same state after remove and re-add")

    def test_commutativity(self):
        """Test that order of additions doesn't matter"""
        h1 = new16()
        h2 = new16()

        # Add in different orders
        h1.add(b"First")
        h1.add(b"Second")

        h2.add(b"Second")
        h2.add(b"First")

        self.assertEqual(h1.get_sum(b""), h2.get_sum(b""), 
                        "Hash should be commutative")

    def test_homomorphism(self):
        """Test homomorphic property: hash(a + b) = hash(a) + hash(b)"""
        h1 = new16()
        h2 = new16()
        h3 = new16()

        # Add values separately
        h1.add(b"Value1")
        h2.add(b"Value2")

        # Combine their states
        combined_state = bytearray(2048)
        for i in range(0, 2048, 2):
            v1 = int.from_bytes(h1.get_sum(b"")[i:i+2], 'little')
            v2 = int.from_bytes(h2.get_sum(b"")[i:i+2], 'little')
            combined = (v1 + v2) & 0xFFFF
            combined_state[i:i+2] = combined.to_bytes(2, 'little')

        # Add values together
        h3.add(b"Value1")
        h3.add(b"Value2")

        self.assertEqual(bytes(combined_state), h3.get_sum(b""),
                        "Hash should be homomorphic")

    def test_large_data(self):
        """Test with larger data inputs"""
        h = new16()
        large_data = b"X" * 10000
        h.add(large_data)
        h.remove(large_data)
        self.assertEqual(h.get_sum(b""), b'\x00' * 2048,
                        "Should handle large data correctly")

    def test_empty_input(self):
        """Test behavior with empty input"""
        h = new16()
        h.add(b"")
        self.assertNotEqual(h.get_sum(b""), b'\x00' * 2048,
                          "Empty input should still produce a hash")

    def test_different_prefixes(self):
        """Test that get_sum with different prefixes produces different results"""
        h = new16()
        h.add(b"TestData")
        s1 = h.get_sum(b"prefix1")
        s2 = h.get_sum(b"prefix2")
        self.assertNotEqual(s1, s2,
                          "Different prefixes should produce different sums")

    def test_overflow_behavior(self):
        """Test overflow behavior with repeated adds"""
        h = new16()
        initial_value = b"Test"
        
        # Add the same value many times
        for _ in range(70000):  # Should cause overflow
            h.add(initial_value)
            
        # Remove the same number of times
        for _ in range(70000):
            h.remove(initial_value)
            
        self.assertEqual(h.get_sum(b""), b'\x00' * 2048,
                        "Should handle overflow correctly")

if __name__ == '__main__':
    unittest.main()