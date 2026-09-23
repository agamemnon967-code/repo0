"""Jump-cut edit map for prachi2.mp4: the single source of truth for every cut.

Each CUT removes [start, end) of source time; every cut sits inside a silencedetect gap (-38 dB,
see DESIGN.md) with ~0.12s of room tone kept on both sides. Everything else in the project is
authored in *source* seconds and mapped to output seconds with `out()`.

    python tools/edit_map.py   -> prints segment HTML + output duration, writes data/transcript-output.json
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = "prachi2.mp4"
SOURCE_END = 33.64
CUTS = [
    (2.38, 2.64),
    (5.72, 6.10),
    (8.46, 9.06),
    (12.00, 12.58),
    (20.44, 20.84),
    (23.98, 24.62),
    (28.56, 28.84),
]


def segments():
    segs, t = [], 0.0
    for a, b in CUTS:
        segs.append((t, a))
        t = b
    segs.append((t, SOURCE_END))
    return segs


def out(src):
    """Map a source time to output time. Times inside a cut snap to the cut point."""
    shift = 0.0
    for a, b in CUTS:
        if src >= b:
            shift += b - a
        elif src > a:
            return round(a - shift, 3)
    return round(src - shift, 3)


END_HOLD = 1.3  # freeze on the last frame so "are you?" can land


def total():
    return round(out(SOURCE_END) + END_HOLD, 3)


def html():
    lines = []
    for i, (a, b) in enumerate(segments()):
        s, d = out(a), round(b - a, 3)
        lines.append(
            f'<video id="seg-{i}" class="clip" src="assets/media/plate.mp4" muted playsinline '
            f'data-start="{s}" data-media-start="{a}" data-duration="{d}" data-track-index="0"></video>'
        )
    for i, (a, b) in enumerate(segments()):
        s, d = out(a), round(b - a, 3)
        lines.append(
            f'<audio id="vo-{i}" src="{SOURCE}" data-start="{s}" data-media-start="{a}" '
            f'data-duration="{d}" data-track-index="10" data-volume="1"></audio>'
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(html())
    print("segments", segments())
    print("output duration", total())
    src = json.load(open(os.path.join(ROOT, "transcript.json")))
    mapped = [dict(w, start=out(w["start"]), end=out(w["end"])) for w in src]
    json.dump(mapped, open(os.path.join(ROOT, "data", "transcript-output.json"), "w"), indent=1)
