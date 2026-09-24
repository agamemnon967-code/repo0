#!/usr/bin/env bash
# Bake the footage treatment into one plate so every jump-cut segment references one source:
#   source -> room dimmed (radial, darker at the edges) -> subject cutout laid back on top at full
#   brightness. Also trims the cutout used for the "instant red flag" red backdrop.
#
# Needs: ffmpeg with libvpx-vp9, python3 + pillow/numpy, and the subject cutout from
#   npx hyperframes remove-background prachi2.mp4 -o /tmp/subject2.webm --quality best
set -euo pipefail
cd "$(dirname "$0")/.."
CUT="${1:-/tmp/subject2.webm}"

"${PYTHON:-python3}" - <<'EOF'
# Same dim as the 10s cut's CSS: rgba(14,11,16,.12) under
# radial-gradient(ellipse 70% 55% at 52% 42%, rgba(14,11,16,.28), rgba(14,11,16,.62)).
import numpy as np
from PIL import Image
W, H = 1080, 1920
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.clip(np.hypot((xx - 0.52 * W) / (0.70 * W), (yy - 0.42 * H) / (0.55 * H)), 0, 1)
a_rad = 0.28 + (0.62 - 0.28) * r
a = 1 - (1 - 0.12) * (1 - a_rad)  # two stacked layers of the same colour
img = np.dstack([np.full((H, W), c, np.uint8) for c in (14, 11, 16)] + [(a * 255).astype(np.uint8)])
Image.fromarray(img, "RGBA").save("/tmp/dim.png")
EOF

ffmpeg -loglevel error -y -i prachi2.mp4 -loop 1 -i /tmp/dim.png -c:v libvpx-vp9 -i "$CUT" \
  -filter_complex "[0:v][1:v]overlay=shortest=1[d];[d][2:v]overlay=eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 -preset medium -g 25 -movflags +faststart assets/media/plate.mp4

# Cutout for the red backdrop on "…nothing." (source 7.30-8.46; must match RED in build.py).
ffmpeg -loglevel error -y -c:v libvpx-vp9 -i "$CUT" -ss 7.30 -t 1.16 \
  -c:v libvpx-vp9 -pix_fmt yuva420p -crf 18 -b:v 0 -auto-alt-ref 0 assets/media/cutout-red.webm
# Cutout for the text-behind-her moments (source 2.40-12.20; must match DEPTH_SRC in build.py).
ffmpeg -loglevel error -y -c:v libvpx-vp9 -i "$CUT" -ss 2.40 -t 9.8 \
  -c:v libvpx-vp9 -pix_fmt yuva420p -crf 20 -b:v 0 -auto-alt-ref 0 assets/media/cutout-depth.webm
# Footage variants, same timebase as the plate: black-and-white and a heavy blur for the transition.
ffmpeg -loglevel error -y -i assets/media/plate.mp4 -vf "hue=s=0,eq=contrast=1.12:brightness=-0.02" \
  -an -c:v libx264 -crf 18 -preset medium -g 25 -movflags +faststart assets/media/bw.mp4
ffmpeg -loglevel error -y -i assets/media/plate.mp4 -vf "gblur=sigma=38" \
  -an -c:v libx264 -crf 22 -preset medium -g 25 -movflags +faststart assets/media/blur.mp4
# Freeze frame for the end hold (last source frame, from the treated plate).
ffmpeg -loglevel error -y -sseof -0.08 -i assets/media/plate.mp4 -frames:v 1 -q:v 2 assets/media/end-hold.jpg
echo "plate, red cutout, bw/blur variants and end-hold frame written"
