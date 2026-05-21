import csv
import time
import random
from dataclasses import dataclass


class HashTable:
    def __init__(self, capacity=2048):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _hash(self, key):
        if isinstance(key, tuple):
            h = 0
            for part in key:
                h = (h * 31 + hash(part)) % self._capacity
            return h
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def insert(self, key, value):
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self._buckets[idx].append([key, value])
        self._size += 1

    def get(self, key):
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                return pair[1]
        return None

    def update(self, key, value):
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return True
        return False

    def delete(self, key):
        idx = self._hash(key)
        for i, pair in enumerate(self._buckets[idx]):
            if pair[0] == key:
                self._buckets[idx].pop(i)
                self._size -= 1
                return True
        return False

    def values(self):
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def __len__(self):
        return self._size


@dataclass
class Track:
    uri: str
    danceability: float
    energy: float
    popularity: int
    loudness: float
    valence: float


def load_tracks(filepath, limit=None):
    tracks = HashTable(capacity=131072)
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if limit and len(tracks) >= limit:
                break
            try:
                track = Track(
                    uri          = row["uri"],
                    danceability = float(row["danceability"]),
                    energy       = float(row["energy"]),
                    popularity   = int(row["popularity"]),
                    loudness     = float(row["loudness"]),
                    valence      = float(row["valence"]),
                )
                tracks.insert(track.uri, track)
            except (KeyError, ValueError):
                continue
    return tracks


def run_benchmark(tracks, sample_size):
    all_uris = [t.uri for t in tracks.values()]
    n_tracks = len(tracks)
    sample   = min(sample_size, n_tracks)

    dummy = Track("dummy", 0.5, 0.5, 50, -10.0, 0.5)

    # READ
    uris = random.sample(all_uris, sample)
    t0 = time.perf_counter()
    for uri in uris:
        tracks.get(uri)
    read_time = time.perf_counter() - t0

    # UPDATE
    uris = random.sample(all_uris, sample)
    t0 = time.perf_counter()
    for uri in uris:
        tracks.update(uri, dummy)
    update_time = time.perf_counter() - t0

    # DELETE
    uris = random.sample(all_uris, sample)
    t0 = time.perf_counter()
    for uri in uris:
        tracks.delete(uri)
    delete_time = time.perf_counter() - t0

    return read_time, update_time, delete_time, sample


def print_section(label, insert_time, n_inserted, read_time, update_time, delete_time, sample):
    print(f"\n{'=' * 66}")
    print(f"  Dataset size: {label}  ({n_inserted:,} tracks loaded)")
    print(f"{'=' * 66}")
    print(f"{'Operation':<10} {'Total ms':>10} {'µs/op':>10} {'ops/sec':>14}")
    print(f"{'-' * 66}")
    for op_label, elapsed, n in [
        ("INSERT",  insert_time,  n_inserted),
        ("READ",    read_time,    sample),
        ("UPDATE",  update_time,  sample),
        ("DELETE",  delete_time,  sample),
    ]:
        ms  = elapsed * 1000
        us  = (elapsed / n) * 1_000_000
        ops = n / elapsed
        print(f"{op_label:<10} {ms:>10.1f} {us:>10.2f} {ops:>14,.0f}")
    print(f"{'=' * 66}")


SAMPLE_SIZE = 10_000  # ops per READ/UPDATE/DELETE test

sizes = [
    ("10K",      10_000),
    ("100K",     100_000),
    ("1M",       1_000_000),
    ("Full",     None),
]

for label, limit in sizes:
    print(f"\nLoading {label} tracks...")
    t0 = time.perf_counter()
    tracks = load_tracks("SongFeatures.csv", limit=limit)
    insert_time = time.perf_counter() - t0

    n_loaded = len(tracks)
    read_time, update_time, delete_time, sample = run_benchmark(tracks, SAMPLE_SIZE)
    print_section(label, insert_time, n_loaded, read_time, update_time, delete_time, sample)
