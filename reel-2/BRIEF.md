---
workflow: general-video
flow: automation
storyboard: no
message: "Most business websites in India bring no leads; Verdexo Ventures helps immigration consultants, study-abroad agencies and clinics get found online and get clients."
destination: instagram-reels
aspect: "9:16"
language: en
length: 31.8s
---

## Intent

Edit of `prachi2.mp4` (33.7s) in the same premium, clean style as the approved SOP reel
(`jazzyease/coursera-test`, `reel-full/`): same caption finish, lemon / white card kit, colour
moments and camera grammar. The user asked for "no cheap shit, no SVGs". v2 (after feedback) uses the old reel
only as a reference: new scene concepts, glossy icon tiles, glowing cards, no SFX (added later by the user).

## Assets

- `prachi2.mp4`: source, 1080×1920, 25fps, 33.67s.
- `transcript.json`: faster-whisper medium.en word timings, cross-checked with large-v3 (identical
  words). Onsets the model pulled into silence were snapped to the silencedetect edge: "but",
  "it's", "That's", "actually", "If", "Because".
- Brand name: whisper heard "Woodexo" / "Vodexo"; written as **Verdexo Ventures** (matches the
  organisation name). Spelling is unverified: change `brand.html` text in `tools/scenes/brand.html`
  and word 25 in `transcript.json` if it differs.

## Customizations

- 7 jump cuts on sentence pauses; 1.3s end freeze. See DESIGN.md.
