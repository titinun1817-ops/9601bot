#!/bin/bash
# Rebuild clip 4 graphics from clip 1's compositions, retimed onto this clip's speech, then apply clip-4 specifics.
set -e; cd "$(dirname "$0")/.."
cp ../usedcar-ladprao/index.html . ; cp ../usedcar-ladprao/compositions/behind.html ../usedcar-ladprao/compositions/front.html compositions/
ANCHORS=anchors_port.json python3 tools/retime.py index.html compositions/behind.html compositions/front.html
ANCHORS=anchors_port.json python3 tools/sfx.py assets/sfx.wav
python3 tools/clip4_fixups.py "$@"
