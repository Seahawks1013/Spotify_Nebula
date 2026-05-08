import csv
import pygame
import numpy as np
from dataclasses import dataclass


# I built a custom hash table instead of using a python dict because the project
# requires me to implement the data structure myself. each bucket holds a chain
# of songs that share the same hash index, which is how chaining works
class HashTable:
    def __init__(self, capacity=2048):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]  # each slot is a list so i can chain collisions
        self._size = 0

    def _hash(self, key):
        # i added a separate path for tuple keys because SpatialHash uses (col, row)
        # as keys instead of strings. without this the string conversion would have
        # been really slow and caused a lot of collisions
        if isinstance(key, tuple):
            h = 0
            for part in key:
                h = (h * 31 + hash(part)) % self._capacity
            return h

        # for string keys like track uris i use a prime-31 polynomial roll
        # multiplying by 31 at each step spreads the keys out more evenly
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def insert(self, key, value):
        # adds a song to the table. if the key already exists i just overwrite it
        # instead of creating a duplicate entry
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return
        self._buckets[idx].append([key, value])
        self._size += 1

    def get(self, key):
        # looks up a song by its uri and returns it, or None if it doesnt exist
        # i walk the chain at that bucket index to find the right key
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                return pair[1]
        return None

    def update(self, key, value):
        # finds an existing song and changes its value
        # returns False if the key wasnt in the table at all
        idx = self._hash(key)
        for pair in self._buckets[idx]:
            if pair[0] == key:
                pair[1] = value
                return True
        return False

    def delete(self, key):
        # removes a song from its bucket by index so i dont have to rebuild the list
        # returns False if the song wasnt found
        idx = self._hash(key)
        for i, pair in enumerate(self._buckets[idx]):
            if pair[0] == key:
                self._buckets[idx].pop(i)
                self._size -= 1
                return True
        return False

    def values(self):
        # loops through every bucket and yields each stored value
        # i use yield so i dont have to build a giant list in memory all at once
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def __len__(self):
        return self._size


# this is the spatial hash, which is the main thing i added this week
# the idea is to divide the danceability/energy space into a grid of cells
# and bucket each song into whichever cell it falls in. when i click somewhere
# i only need to check nearby cells instead of comparing against all 1.2M songs
class SpatialHash:
    def __init__(self, cell_size=0.05):
        self.cell_size = cell_size
        # i made the capacity bigger here because at 1M+ tracks the cells can get
        # crowded and i wanted fewer hash collisions on the cell keys
        self.table = HashTable(capacity=4096)

    def _cell(self, x, y):
        # converts a continuous x,y coordinate into a discrete grid cell
        # dividing by cell_size and flooring it gives me the column and row
        return (int(x / self.cell_size), int(y / self.cell_size))

    def insert(self, track):
        # figure out which cell this track belongs in, then append it to that bucket
        # if the bucket doesnt exist yet i create a new list for it first
        # this is O(1) average because its just one hash lookup plus an append
        key = self._cell(track.danceability, track.energy)
        bucket = self.table.get(key)
        if bucket is None:
            bucket = []
            self.table.insert(key, bucket)
        bucket.append(track)

    def neighbors(self, x, y, radius=1):
        # this is the whole reason i built the spatial hash
        # instead of looping through all 1.2M songs to find nearby ones,
        # i only check the cells within `radius` steps of the clicked cell
        # with radius=1 thats at most 9 cells, so its O(k) not O(n)
        cx, cy = self._cell(x, y)
        results = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                bucket = self.table.get((cx + dx, cy + dy))
                if bucket:
                    results.extend(bucket)
        return results


# blueprint for a single spotify track
# i added name and artists this week so i can display song info on click later
@dataclass
class Track:
    uri: str
    name: str
    artists: str
    danceability: float
    energy: float
    popularity: int
    loudness: float
    valence: float


def load_tracks(filepath, limit=None):
    # i set a large capacity here because the full dataset is about 1.2M songs
    # and i dont want the hash table to degrade from too many collisions
    tracks = HashTable(capacity=131072)
    with open(filepath, newline="", encoding="utf-8") as f:  # auto closes when done
        reader = csv.DictReader(f)
        for row in reader:
            if limit and len(tracks) >= limit:  # still keeping limit as an option for testing
                break
            try:
                track = Track(
                    uri          = row["uri"],
                    # the column name for the song title isnt consistent across datasets
                    # so i check for both just in case
                    name         = row.get("track_name", row.get("name", "Unknown")),
                    artists      = row.get("artists", "Unknown"),
                    danceability = float(row["danceability"]),
                    energy       = float(row["energy"]),
                    popularity   = int(row["popularity"]),
                    loudness     = float(row["loudness"]),
                    valence      = float(row["valence"]),
                )
                tracks.insert(track.uri, track)
            except (KeyError, ValueError):  # skip rows with missing or bad data
                continue
    return tracks


def valence_to_color(valence):
    # low valence is purple because sad songs feel that way to me
    # high valence shifts to cyan which feels bright and energetic
    r = int(80  + (20  - 80)  * valence)
    g = int(20  + (200 - 20)  * valence)
    b = int(120 + (255 - 120) * valence)
    return (r, g, b)


def track_to_screen(track, w, h):
    # maps danceability (0-1) to x and energy (0-1) to y
    # i flip energy because pygame counts y from the top down,
    # so without the flip high energy songs would appear at the bottom
    # no padding here anymore — the caller offsets by PAD_L when blitting
    x = int(track.danceability * w)
    y = int((1 - track.energy)  * h)
    return x, y


def build_starfield(tracks, width, height):
    # instead of calling set_at() once per track (which is slow at 1M+ songs),
    # i build a numpy pixel array for the whole screen upfront and write all
    # the colors into it at once. then i blit the whole array to the surface
    # in one shot. this is way faster because numpy operates in bulk on the
    # raw memory instead of going through pygames python layer for every pixel

    # shape is (width, height, 3) because surfarray uses x,y order not row,col
    pixels = np.full((width, height, 3), (5, 5, 15), dtype=np.uint8)

    for track in tracks.values():
        x, y = track_to_screen(track, width, height)
        if 0 <= x < width and 0 <= y < height:
            r, g, b = valence_to_color(track.valence)
            pixels[x, y] = (r, g, b)  # numpy lets me write the whole rgb triplet at once

    # create the surface and copy the pixel array into it
    surface = pygame.Surface((width, height))
    pygame.surfarray.blit_array(surface, pixels)
    return surface


def draw_axes(surface, font, w, h, pad_l, pad_b):
    # i draw the axes on a separate surface so they sit on top of the starfield
    # pad_l is the left margin and pad_b is the bottom margin where the bars live

    ax_color    = (60, 60, 80)    # dim so it doesnt compete with the stars
    tick_color  = (90, 90, 110)
    label_color = (130, 130, 160)

    plot_w = w - pad_l          # width of the actual plot area
    plot_h = h - pad_b          # height of the actual plot area

    # x axis line across the bottom of the plot
    pygame.draw.line(surface, ax_color, (pad_l, plot_h), (w, plot_h), 1)

    # y axis line down the left side of the plot
    pygame.draw.line(surface, ax_color, (pad_l, 0), (pad_l, plot_h), 1)

    # x axis ticks and labels every 0.1 from 0.0 to 1.0
    for i in range(11):
        val  = i / 10
        sx   = pad_l + int(val * plot_w)
        pygame.draw.line(surface, tick_color, (sx, plot_h), (sx, plot_h + 4), 1)
        lbl  = font.render(f"{val:.1f}", True, label_color)
        surface.blit(lbl, (sx - lbl.get_width() // 2, plot_h + 6))

    # x axis title
    x_title = font.render("danceability", True, label_color)
    surface.blit(x_title, (pad_l + plot_w // 2 - x_title.get_width() // 2, h - 14))

    # y axis ticks and labels every 0.1 from 0.0 to 1.0
    for i in range(11):
        val  = i / 10
        sy   = plot_h - int(val * plot_h)  # flip because pygame y goes downward
        pygame.draw.line(surface, tick_color, (pad_l - 4, sy), (pad_l, sy), 1)
        lbl  = font.render(f"{val:.1f}", True, label_color)
        surface.blit(lbl, (pad_l - lbl.get_width() - 6, sy - lbl.get_height() // 2))

    # y axis title, rotated 90 degrees
    y_title = font.render("energy", True, label_color)
    y_title = pygame.transform.rotate(y_title, 90)
    surface.blit(y_title, (2, plot_h // 2 - y_title.get_height() // 2))


def main():
    # i added padding on the left and bottom to make room for the axis bars
    PAD_L = 45   # left margin for y axis labels
    PAD_B = 30   # bottom margin for x axis labels
    W, H  = 860, 640  # slightly bigger window to fit the margins comfortably

    # load the full dataset, no limit this week
    print("Loading tracks...")
    tracks = load_tracks("SongFeatures.csv")
    print(f"Loaded {len(tracks)} tracks")

    # insert every track into the spatial hash so neighbor queries work
    print("Building spatial hash...")
    spatial = SpatialHash(cell_size=0.05)
    for track in tracks.values():
        spatial.insert(track)
    print("Spatial hash ready.")

    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Spotify Nebula")
    font  = pygame.font.SysFont("monospace", 11)
    clock = pygame.time.Clock()

    # the plot area is the window minus the axis margins
    plot_w = W - PAD_L
    plot_h = H - PAD_B

    # draw all the stars once and cache the result
    # the starfield only covers the plot area, not the axis margins
    print("Rendering starfield...")
    starfield = build_starfield(tracks, plot_w, plot_h)
    print("Ready.")

    selected_neighbors = []  # songs near the last click
    click_pos          = None  # where i clicked on screen

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # convert the click from screen pixels back into data space (0.0 to 1.0)
                # i have to subtract PAD_L first because the plot doesnt start at x=0 anymore
                dx = (mx - PAD_L) / plot_w
                dy = 1 - my / plot_h
                dx = max(0.0, min(1.0, dx))  # clamp so i dont go out of bounds
                dy = max(0.0, min(1.0, dy))
                selected_neighbors = spatial.neighbors(dx, dy, radius=1)
                click_pos = (mx, my)

        screen.fill((5, 5, 15))  # clear the whole window including margins

        # blit the starfield offset by PAD_L so it sits inside the axis margins
        screen.blit(starfield, (PAD_L, 0))

        # highlight any songs near the click in yellow so they stand out
        for t in selected_neighbors:
            sx, sy = track_to_screen(t, plot_w, plot_h)
            pygame.draw.circle(screen, (255, 230, 80), (sx + PAD_L, sy), 3)

        # small white ring to show where i clicked
        if click_pos:
            pygame.draw.circle(screen, (255, 255, 255), click_pos, 6, 1)

        # show how many neighbors were found in the top left of the plot area
        if selected_neighbors:
            label = font.render(
                f"{len(selected_neighbors)} neighbors found", True, (200, 200, 200)
            )
            screen.blit(label, (PAD_L + 6, 8))

        # draw the actual axis bars with ticks and numeric labels
        draw_axes(screen, font, W, H, PAD_L, PAD_B)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()