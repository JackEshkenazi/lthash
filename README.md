# Homomorphic Commutative Hash (LtHash)

A lightweight homomorphic, commutative hash implementation in Python. Designed for set reconciliation and difference detection in distributed systems.

## Background

In a distributed system, database replication involves copying information to keep it synchronized across multiple locations to improve availability and read latency. This problem of securing update broadcasts in such systems was formally analyzed by Maitin-Shepard et al. in "Securing Update Propagation with Homomorphic Hashing" [ePrint 2019/227], which proposed the use of homomorphic hash functions for efficient verification. Database modifications must be propagated to each location to maintain the consistency of the replicated objects with the master database. For a model in which database writes are published by a central distributor that manages the master database, the distributor is responsible for propagating updates to a set of subscribers in a reliable and efficient manner. The simplest way to achieve this is for the distributor to be in charge of directly sending the updates to each subscribed client. In this repo I have attempted to implement the LtHash as specified by researchers at [Facebook](https://eprint.iacr.org/2019/227.pdf).

## Features

- Homomorphic: hash(a) + hash(b) = hash(a + b)
- Commutative: hash(a + b) = hash(b + a)
- Invertible: Elements can be added and removed
- Fixed size state (2048 bytes)
- Based on BLAKE2b and 16-bit arithmetic

## Usage

```python
from lthash import new16

# Basic usage
h = new16()
h.add(b"Hello")
h.add(b"World")
state = h.get_sum(b"")

# Remove elements
h.remove(b"World")

# Save/restore state
saved_state = h.get_sum(b"")
h2 = new16()
h2.set_state(saved_state)
```

## Use Cases

- Set reconciliation
- Difference detection
- Content-based deduplication
- Distributed caching

## Testing

```bash
python -m unittest tests/lthash_test.py
```
