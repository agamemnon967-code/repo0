# DESIGN: Verdexo reel (`prachi2.mp4`, 33.7s source → 31.8s edit)

Same system as the approved SOP reel (`jazzyease/coursera-test` → `reel-full/DESIGN.md`, base spec in
`reel/DESIGN.md`): palette, caption finish, card kit and "no AI slop" rules are carried over
unchanged. What is new here is the scene set and the layout shift for this framing.

## Rules carried over

- Captions: heavy extended italic Archivo caps, flat bevel (white → cool grey), one tight dark
  shadow; accent lemon `#F6F97F`, alarm red `#FF2E3F`. Line-1 words ghost in, accent words slide in
  from the left, hero words slam 1.28 → 1. Groups hard-swap.
- Graphics on sharp footage at chest height, face always visible; one light cutaway (brand).
- One component kit (`tools/scenes/_base.css`): `.wcard` white card, `.ltile` lemon tile, `.ground`
  cream cutaway, `.ink-cap`, plus CSS-only `.xmark` / `.tick` / `.itile`.
- **No SVG anywhere.** Browser dots, padlock, magnifier, spinner, cross and tick are CSS shapes.
- Only her spoken words appear as text (plus rank numbers 1–3 on the search results).

## Layout (1080×1920)

She sits lower in this frame than in the SOP reel (chin ≈ y790, hands ≈ y1500), so everything moved
down ~120px: cards y850–1280, captions block top 1290 (centre ≈ y1455), camera origin (570, 560).

## Scenes

| Source s | Line | Scene | Type |
| --- | --- | --- | --- |
| 0–2.4 | "Most businesses in India have a website" | `site`: browser bar card lands and types "website" | chest card |
| 2.6–5.7 | "…just sitting there doing nothing" | `site`: idle card, spinner turns, stalls and greys on "nothing"; frame drains to B&W | chest card |
| 6.1–8.5 | "No leads, no calls, nothing" | `zero`: two white cards with red "0" pills; red backdrop behind her on "nothing" | chest cards |
| 9.1–10.4 | "That's exactly why we" | captions, punch on "why" | face |
| 10.4–12.0 | "started Verdexo Ventures" | `brand`: light cutaway, lemon "V" monogram tile + ink wordmark | cutaway |
| 12.6–17.0 | "We help immigration consultants, study abroad agencies, and clinics" | `who`: white-card stack with lemon initial tiles, as spoken | chest cards |
| 17.0–20.4 | "get found online and get clients from it" | `rail`: FOUND ONLINE → CLIENTS line | chest |
| 20.8–24.0 | "No fluff, no jargon, just results" | `nofluff`: Fluff ✕, Jargon ✕, lemon "Just results" ✓; blur transition out | chest cards |
| 24.6–28.6 | "digital presence isn't working… let's fix that" | `status`: pill pending → red ISN'T WORKING (B&W) → lemon LET'S FIX THAT (colour returns) | chest card |
| 28.8–32.0 | "competitors are already showing up on Google" | `search`: search bar, three ranked Competitor results, query types "Google" | chest cards |
| 32.1–33.6 | "The question is, are you?" | captions, jump zoom, push-in through the 1.3s end freeze | face |

## Edit

- 7 jump cuts (`tools/edit_map.py`), each inside a silencedetect gap (-38 dB) with ~0.12s of room
  tone kept either side. Rhetorical pauses ("honestly,", "The question is, | are you?") are kept.
- Framing alternates on every cut; punches only on stressed words (website, nothing ×2, why,
  clients, results, isn't working, fix, are you).
- Voice is cut on the same segments as the picture; no music (none supplied).

## Build

```bash
npx hyperframes remove-background prachi2.mp4 -o /tmp/subject2.webm --quality best
tools/make_plate.sh /tmp/subject2.webm   # dimmed-room plate, red cutout, B&W + blur variants, end-hold frame
python3 tools/build.py                   # index.html + compositions/*.html from tools/scenes
npm run check && npm run render
```
