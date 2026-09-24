# DESIGN: Verdexo reel (`prachi2.mp4`, 33.7s source → 31.8s edit)

Same system as the approved SOP reel (`jazzyease/coursera-test` → `reel-full/DESIGN.md`, base spec in
`reel/DESIGN.md`): palette, caption finish, card kit and "no AI slop" rules are carried over
unchanged. What is new here is the scene set and the layout shift for this framing.

## v3: presentation + palette (user feedback on v2)

**Palette, chosen against the room.** The set is all warm: cream walls, dusty-rose blazer, wood desk,
white tee (sampled `#CBB49D`, `#BA8778`, `#E1D9CF`). White cards and lemon accents melted into it, so v3
goes cool and opposite:

| Role | Hex | Use |
| --- | --- | --- |
| Navy glass | `#1D2858 → #0F1634` | panels (`.ncard`), cutaway ground `#1C2B6A → #070A1A` |
| Electric blue | `#7AA3FF → #3D6BFF → #2547D6` | icon tiles, highlight panels, caption accent, halos |
| Mint | `#8FF8E4 → #34E0C3` | positive states (tick, "Let's fix that", #1, new client) |
| Coral | `#FF8B97 → #FF4D61` | negative states (strikes, ✕, "Isn't working", missed call) |
| Ice / muted | `#F4F7FF` / `#8E9CC8` | text on navy |

**Three presentation modes**, mixed so the graphics never all sit in front of her:

- **Overlay** on sharp footage at chest height: URL bar, "We help" cards, digital-presence status.
- **Blurred footage** (`SCENE_BG` in `build.py`): static blur plate + navy tint, graphic centre
  stage, captions stay: phone lock screen, "found online", Google search.
- **Full-screen cutaway** (`.screen`: navy ground, soft blue/mint light, dot grid) with
  transitions: the URL bar rises into a browser page on the jump cut; zoom-blur push into the brand
  screen; hard cut into the "No fluff" type screen with a zoom-through exit into the blur.

Kit (`tools/scenes/_base.css`): `.ncard`, `.appi` (blue / mint / red / mute glossy tiles),
`.halo`, `.screen`, `.disp` + `.bt` display type, `.eyebrow`, CSS `.xmark` / `.tick`. Icons are
Material Symbols Rounded glyphs from a subset font (`tools/icons.json`); **no SVG**. **No SFX.**

## Rules carried over

- Captions: heavy extended italic Archivo caps, bevelled face, one tight dark shadow; accent now
  electric blue, alarm red for negatives. Line-1 words ghost in, accent words slide in, heroes slam.
- UI text (URL, DAY counter, Inbox/Phone lines, Your business, New client, Competitor, search
  query) is illustrative; all other on-screen words are hers.

## Layout (1080×1920)

She sits lower in this frame than in the SOP reel (chin ≈ y790, hands ≈ y1500), so everything moved
down ~120px: cards y850–1280, captions block top 1290 (centre ≈ y1455), camera origin (570, 560).

## Scenes

| Source s | Line | Scene | Type |
| --- | --- | --- | --- |
| 0–2.4 | "Most businesses in India have a website" | `site`: navy URL bar at chest types `www.yourbusiness.in` | overlay |
| 2.6–4.8 | "but honestly, it's just sitting there" | `site`: on the jump cut the bar rises and a page card unrolls on a navy screen; her words are the page (SITTING in blue), DAY counter runs to 365 | cutaway |
| 4.8–5.7 | "doing nothing" | zoom-out through blur back to her; B&W + punch on "nothing" | face |
| 6.1–7.9 | "No leads, no calls, nothing" | `phone`: footage blurs, phone rises on its lock screen; "No leads" / "No calls" notifications land as spoken, clear to "No notifications", screen switches off → red backdrop on her | blurred |
| 9.1–10.4 | "That's exactly why we" | captions, punch on "why", push + blur into the cutaway | face |
| 10.4–12.0 | "started Verdexo Ventures" | `brand`: navy screen, blue "V" tile with ring pulse, white / blue wordmark | cutaway |
| 12.6–17.0 | "We help immigration consultants, study abroad agencies, and clinics" | `who`: navy cards with blue icon tiles, each glows as spoken | overlay |
| 17.0–20.4 | "get found online and get clients from it" | `found`: navy result rises to #1 (pin, stars, TOP RESULT, glow); white "New client" toasts stack | blurred |
| 20.8–24.0 | "No fluff, no jargon, just results" | `nofluff`: coral rows struck + muted, glowing blue JUST RESULTS panel with mint tile + tick; zoom-through into blur | cutaway |
| 24.6–28.6 | "digital presence isn't working… let's fix that" | `status`: navy card, globe → coral error (B&W) → mint bolt (colour returns) | overlay |
| 28.8–32.0 | "competitors are already showing up on Google" | `search`: white search bar types a query, navy ranked Competitor results, bar glows on "Google" | blurred |
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
