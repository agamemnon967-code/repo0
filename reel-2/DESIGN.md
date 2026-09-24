# DESIGN: Verdexo reel (`prachi2.mp4`, 33.7s source → 31.8s edit)

Same system as the approved SOP reel (`jazzyease/coursera-test` → `reel-full/DESIGN.md`, base spec in
`reel/DESIGN.md`): palette, caption finish, card kit and "no AI slop" rules are carried over
unchanged. What is new here is the scene set and the layout shift for this framing.

## v4: flat editorial (user feedback on v3: "AI slop")

v3's navy gradient grounds, glowing blobs, dot grids, glossy glowing icon tiles and gradient
text read as generic AI output. v4 removes that whole language:

- **Flat colour only.** No gradients, glows, blooms, blobs, grids or light sweeps anywhere,
  captions included (flat fills, no bevel, no hero light pass).
- **Four colours:** ink `#111113`, paper `#F3F1EC`, white, one accent cobalt `#2B4CFF`; signal
  red `#F2382E` only for negatives. Cobalt and ink both separate cleanly from the warm room
  (cream walls, rose blazer, wood).
- **Type does the work:** upright Archivo 800, tracking -0.045em for headlines, spaced uppercase
  labels, hairline rules, numbered lists. Captions keep the reference's heavy italic caps.
- **UI looks real, not stylised:** Safari address bar, iPhone lock screen with iOS notifications
  and flat app icons, a local-search results sheet, a Google-style query bar. Depth comes from one
  realistic shadow and 1px hairlines.
- **Motion:** expo ease, clip-path wipes and masked line rises. No bounces, spins or glints.

Presentation modes (unchanged from v3): overlay on sharp footage, blurred footage (neutral dim),
full-bleed cutaway with wipes.

Kit (`tools/scenes/_base.css`): `.sheet`, `.ground.paper|ink|cobalt`, `.hed`, `.label`, `.rule`,
`.chip`, `.app`. Icons: Material Symbols Rounded subsets, outline wght 300 (`{{I:name}}`) and filled
(`{{F:name}}`); `{{CP:name}}` gives a raw codepoint. **No SVG. No SFX.**

## Rules carried over

- Captions: heavy extended italic Archivo caps, flat fill, one tight dark shadow; accent flat
  cobalt tint `#8EA2FF`, red `#FF4D42` for negatives. Groups hard-swap.
- UI text (URL, "Last visitor … ago", notification lines, "Consultants near me", ratings,
  "New client", "Competitor", search query) is illustrative; all other on-screen words are hers.

## Layout (1080×1920)

She sits lower in this frame than in the SOP reel (chin ≈ y790, hands ≈ y1500), so everything moved
down ~120px: cards y850–1280, captions block top 1290 (centre ≈ y1455), camera origin (570, 560).

## Scenes

| Source s | Line | Scene | Type |
| --- | --- | --- | --- |
| 0–2.4 | "Most businesses in India have a website" | `site`: Safari address bar over her types `www.yourbusiness.in` | overlay |
| 2.6–4.8 | "but honestly, it's just sitting there" | `site`: paper screen wipes up on the jump cut; browser window: "But honestly," fills the page, then her line takes over as the headline ("there." in cobalt); "Last visitor N days ago" ticks up | cutaway |
| 4.8–5.7 | "doing nothing" | paper wipes off upward; B&W + punch on "nothing" | face |
| 6.1–7.9 | "No leads, no calls, nothing" | `phone`: footage blurs; iPhone on a plain lock screen, Mail / Phone notifications land as spoken, clear to "No notifications", screen off → red backdrop | blurred |
| 9.1–10.4 | "That's exactly why we" | captions, punch on "why"; cobalt wipes up over the push-in | face |
| 10.4–12.0 | "started Verdexo Ventures" | `brand`: flat cobalt, white V tile, WE STARTED label + rule, masked rise of Verdexo / Ventures | cutaway |
| 12.6–17.0 | "We help immigration consultants, study abroad agencies, and clinics" | `who`: one white sheet, a row per sector revealed as spoken, cobalt marker follows | overlay |
| 17.0–20.4 | "get found online and get clients from it" | `found`: local search sheet, "Your business" climbs from 3rd to 1st, Top result tag; "New client" notifications stack | blurred |
| 20.8–24.0 | "No fluff, no jargon, just results" | `nofluff`: ink screen, numbered list, red strikes, "Just results." in cobalt with a check; wipes into the blur | cutaway |
| 24.6–28.6 | "digital presence isn't working… let's fix that" | `status`: white status row: Checking → Isn't working (B&W) → Let's fix that (colour back) | overlay |
| 28.8–32.0 | "competitors are already showing up on Google" | `search`: query bar types "study abroad consultant near me", competitor results fill page one | blurred |
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
