#csv reads csv file, pygame opens window for graphics
#and dataclass helps define the track  blueprient efficiently. 

import csv 
import pygame
from dataclasses import dataclass


@dataclass
class Track:
    uri: str
    danceability: float
    energy: float
    popularity: int
    loudness: float
    valence: float


def load_tracks(filepath, limit=None):
    tracks = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if limit and len(tracks) >= limit:
                break
            try:
                track = Track(
                    uri=row["uri"],
                    danceability=float(row["danceability"]),
                    energy=float(row["energy"]),
                    popularity=int(row["popularity"]),
                    loudness=float(row["loudness"]),
                    valence=float(row["valence"]),
                )
                tracks[track.uri] = track
            except (KeyError, ValueError):
                continue
    return tracks


def main():
    tracks = load_tracks("SongFeatures.csv", limit=10_000)
    print(f"Loaded {len(tracks)} tracks")

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Spotify Nebula")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
