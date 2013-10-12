from itertools import groupby
import json
from pprint import pprint
import re
import sys

with open(sys.argv[1]) as f:
    chunks = re.split(r"\n\n+", f.read())

with open(sys.argv[2]) as f:
    known_chars = json.load(f)

# play is a list of lists, each list represents an act
# act is a list of lists, each list represents a scene
play = [list(group) for k, group in groupby(chunks, lambda s:
    s.startswith("ACT")) if not k][1:]

for i in xrange(len(play)):
    play[i] = [list(group) for k, group in groupby(play[i], lambda s:
        s.startswith("Scene")) if not k]

def act(n):
    return play[n]

def scene(i, j):
    return play[i][j]

def characters(scene):
    characters = set(s.split()[0] for s in scene if not s.startswith("["))
    characters = set(known_chars[char] for char in characters if char in known_chars)
    return sorted(list(characters))

all_chars = []
for i in xrange(len(play)):
    for j in xrange(len(play[i])):
        all_chars += characters(scene(i, j))
all_chars = sorted(list(set(all_chars)))

def length(scene):
    return len(''.join(scene))

scenes = []
start = 0
scene_id = 0
for i in xrange(len(play)):
    for j in xrange(len(play[i])):
        d = {
                "duration": length(scene(i, j)),
                "start": start,
                "id": scene_id,
                "chars": characters(scene(i, j))
            }
        scenes.append(d)
        start += length(scene(i, j))
        scene_id += 1

pprint(scenes)
