import time, random

# reuse your existing classes
from main_code_2 import HashTable, Track

tracks = [Track(f"id_{i}", random.random(), random.random(), 50, -5.0, random.random()) for i in range(10_000)]

query = tracks[0]

# NAIVE — checks every single track O(n)
t0 = time.perf_counter()
naive = [t for t in tracks if abs(t.danceability - query.danceability) < 0.05
                             and abs(t.energy - query.energy) < 0.05]
print(f"Naive:   {(time.perf_counter()-t0)*1000:.3f} ms — {len(naive)} neighbors")