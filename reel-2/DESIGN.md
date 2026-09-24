# DESIGN: Verdexo reel (`prachi2.mp4`, 33.7s source → 31.8s edit)

Same system as the approved SOP reel (`jazzyease/coursera-test` → `reel-full/DESIGN.md`, base spec in
`reel/DESIGN.md`): palette, caption finish, card kit and "no AI slop" rules are carried over
unchanged. What is new here is the scene set and the layout shift for this framing.

## v2: premium pass (user feedback on v1)

v1 reused the SOP reel's scenes too literally (typed word, spinner, text-only cards, a plain rail).
v2 keeps the caption finish and colour moments but rebuilds every scene around one richer kit:

- **Glossy app-icon tiles** (`.appi`): squircle, ink gradient with a lit lemon glyph, top gloss,
  inner shade; `lemon`, `red` and `mute` variants cross-fade as state changes.
- **Icons** are Material Symbols Rounded glyphs (filled, wght 500) from a 5 KB font subset
  (`assets/fonts/Icons-Rounded-Filled.woff2`, map in `tools/icons.json`). Written as `{{I:name}}` in
  scene templates, or `I("name")` in `build.py`. Still **no SVG** anywhere.
- **Cards**: brighter white with a top highlight and a two-layer drop shadow; `.halo` adds a lemon
  (or red) ring + bloom when a card lands or changes state. Dark-glass toasts (`.dglass`) for notifications.
- **No SFX** (the user adds sound design separately).

## Rules carried over

- Captions: heavy extended italic Archivo caps, flat bevel (white → cool grey), one tight dark
  shadow; accent lemon `#F6F97F`, alarm red `#FF2E3F`. Line-1 words ghost in, accent words slide in
  from the left, hero words slam 1.28 → 1. Groups hard-swap.
- Graphics on sharp footage at chest height, face always visible; one light cutaway (brand).
- UI chrome text (Visitors, NONE, Top result, New client, Competitor, the search query, the URL) is
  illustrative; all other on-screen words are hers.

## Layout (1080×1920)

She sits lower in this frame than in the SOP reel (chin ≈ y790, hands ≈ y1500), so everything moved
down ~120px: cards y850–1280, captions block top 1290 (centre ≈ y1455), camera origin (570, 560).

## Scenes

| Source s | Line | Scene | Type |
| --- | --- | --- | --- |
| 0–2.4 | "Most businesses in India have a website" | `site`: browser bar types `www.yourbusiness.in`, lemon search button pulses | chest card |
| 2.6–5.7 | "…just sitting there doing nothing" | `site`: Visitors widget lands: LIVE pill, flat week chart, a scan finds nothing; on "nothing" LIVE → IDLE, 0 turns red, red halo; frame drains to B&W | chest cards |
| 6.1–8.5 | "No leads, no calls, nothing" | `zero`: two widgets: mail / phone app tiles, 0 + NONE pill; inbox bounces, phone rings once, both mute; exit before the red backdrop on "nothing" | chest widgets |
| 9.1–10.4 | "That's exactly why we" | captions, punch on "why" | face |
| 10.4–12.0 | "started Verdexo Ventures" | `brand`: light cutaway, lemon "V" monogram tile + ink wordmark | cutaway |
| 12.6–17.0 | "We help immigration consultants, study abroad agencies, and clinics" | `who`: card stack with lemon icon tiles (plane, cap, medical), each card glows as it's spoken | chest cards |
| 17.0–20.4 | "get found online and get clients from it" | `found`: "Your business" result rises to #1, pin drops with ripple, stars, TOP RESULT, lemon halo; three dark "New client" toasts stack on "clients… from it" | chest cards |
| 20.8–24.0 | "No fluff, no jargon, just results" | `nofluff`: red icon tiles (cloud, translate) struck + ✕ and muted; glowing lemon "Just results" with ink trend tile + ✓; blur transition out | chest cards |
| 24.6–28.6 | "digital presence isn't working… let's fix that" | `status`: globe tile → red error tile + red halo (B&W) → lemon bolt tile + lemon halo (colour returns) | chest card |
| 28.8–32.0 | "competitors are already showing up on Google" | `search`: query types "study abroad consultant", three ranked Competitor results with stars and trend badges; bar glows on "Google" | chest cards |
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
