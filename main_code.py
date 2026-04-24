#csv reads csv file, pygame opens window for graphics
#and dataclass helps define the track  blueprient efficiently. 

import csv 
import pygame
from dataclasses import dataclass



#this is the blueprint for a song. this 
@dataclass
class Track:
    uri: str
    danceability: float
    energy: float
    popularity: int
    loudness: float
    valence: float


def load_tracks(filepath, limit=None):

    tracks = {} #this is the dictionary (hash map)
    with open(filepath, newline="", encoding="utf-8") as f: #opens csv then auto closes
        reader = csv.DictReader(f)
        for row in reader:
            if limit and len(tracks) >= limit: #currently sampling so information loads faster
                break
            try:
                track = Track( #track object is created, takes raw text from csv
                    uri=row["uri"],
                    danceability=float(row["danceability"]),
                    energy=float(row["energy"]),
                    popularity=int(row["popularity"]),
                    loudness=float(row["loudness"]),
                    valence=float(row["valence"]),
                )
                tracks[track.uri] = track
            except (KeyError, ValueError): #handles bad data in teh event of invalid number or missing column 
                continue
    return tracks


def main():
    tracks = load_tracks("SongFeatures.csv", limit=10_000)
    print(f"Loaded {len(tracks)} tracks")

    #visualization process 
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Spotify Nebula")

    #game loop to run forever 
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
