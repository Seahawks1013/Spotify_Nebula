import csv
import pygame
from dataclasses import dataclass


#hash table stores the songs, each bucket holds a chain of songs that share the same hash
class HashTable:
    def __init__(self, capacity=2048):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)] #each bucket is a list (chain)
        self._size = 0

    def _hash(self, key):
        #turns the key into a bucket index using prime 31 to spread keys out evenly
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def insert(self, key, value):
        #adds a song, if the key already exists it just overwrites it
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self._buckets[idx].append([key, value])
        self._size += 1

    def get(self, key):
        #looks up a song by its uri, returns None if not found
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                return pair[1]
        return None

    def update(self, key, value):
        #finds the song and changes its value, returns False if the key doesnt exist
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return True
        return False

    def delete(self, key):
        #removes a song from its bucket, returns False if it wasnt there
        idx = self._hash(key)
        for i, pair in enumerate(self._buckets[idx]):
            if pair[0] == key:
                self._buckets[idx].pop(i)
                self._size -= 1
                return True
        return False

    def values(self):
        #loops through every bucket and yields each song
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def __len__(self):
        return self._size


#this is the blueprint for a song
@dataclass
class Track:
    uri: str
    danceability: float
    energy: float
    popularity: int
    loudness: float
    valence: float


def load_tracks(filepath, limit=None):
    tracks = HashTable() #custom hash table, not a python dict
    with open(filepath, newline="", encoding="utf-8") as f: #opens csv then auto closes
        reader = csv.DictReader(f)
        for row in reader:
            if limit and len(tracks) >= limit: #sampling so it loads faster while developing
                break
            try:
                track = Track( #track object is created, takes raw text from csv
                    uri          = row["uri"],
                    danceability = float(row["danceability"]),
                    energy       = float(row["energy"]),
                    popularity   = int(row["popularity"]),
                    loudness     = float(row["loudness"]),
                    valence      = float(row["valence"]),
                )
                tracks.insert(track.uri, track)
            except (KeyError, ValueError): #handles bad data in the event of invalid number or missing column
                continue
    return tracks


def valence_to_color(valence):
    #maps valence to a color, low valence is purple (sad) and high valence is cyan (happy)
    r = int(80  + (20  - 80)  * valence)
    g = int(20  + (200 - 20)  * valence)
    b = int(120 + (255 - 120) * valence)
    return (r, g, b)


def main():
    tracks = load_tracks("SongFeatures.csv", limit=10_000)
    print(f"Loaded {len(tracks)} tracks")

    #visualization setup
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Spotify Nebula")
    clock = pygame.time.Clock()

    #game loop runs forever until the window is closed
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((5, 5, 15)) #deep space background

        #draw each song as a dot, x is danceability and y is energy
        #y is flipped because pygame counts from the top down
        for track in tracks.values():
            x     = int(track.danceability * 760) + 20
            y     = int((1 - track.energy) * 560) + 20
            color = valence_to_color(track.valence)
            pygame.draw.circle(screen, color, (x, y), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()