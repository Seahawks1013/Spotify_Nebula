import csv
import pygame



@dataclass
class Track:
    uri: str
    danceability: float
    energy: float
    popularity: int
    loudness: float
    valence: float


