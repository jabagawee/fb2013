from collections import defaultdict
from itertools import groupby
import json
from pprint import pprint
import re
import sys

CHUNK_SIZE = 1000

with open(sys.argv[1]) as f:
    text = f.read().split()

with open(sys.argv[2]) as f:
    known_chars = json.load(f)

timeline = [known_chars.get(word) for word in text]
chunks = [set(filter(None, chunk)) for chunk in zip(*[iter(timeline)] * CHUNK_SIZE)]

nodes = []
links = defaultdict(int)

for i, chunk in enumerate(chunks):
    d = {"name": '', "group": 1}
    nodes.append(d)
    for character in chunk:
        source = i - 1
        dest = i + 1
        while source >= 0 and character not in chunks[source]:
            source -= 1
        while dest < len(chunks) and character not in chunks[dest]:
            dest += 1
        if source != -1:
            links[(source, i)] += 1
        if dest != len(chunks):
            links[(i, dest)] += 1

links = [{"source": k[0], "target": k[1], "value": v} for k, v in links.iteritems()]

print json.dumps({"nodes": nodes, "links": links})
