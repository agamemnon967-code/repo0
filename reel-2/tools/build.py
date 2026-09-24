"""Generate index.html, compositions/captions.html and one compositions/<host>.html per scene.

Everything here is authored in SOURCE seconds (the raw clip) and mapped through the jump cuts in
tools/edit_map.py, so the edit can be re-cut by changing CUTS and re-running:
    python3 tools/build.py
"""

import json
import os
import re

from edit_map import CUTS, END_HOLD, SOURCE_END, html as seg_html, out, segments, total

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = json.load(open(os.path.join(ROOT, "transcript.json")))
W = [[w["start"], w["text"].rstrip(",.")] for w in WORDS]


def ws(i):
    return WORDS[i]["start"]


# --------------------------------------------------------------------------- captions
# l1 = small white line, l2 = accent lines (word indices); size = accent px. Groups hard-swap.
def G(l1, l2, tone, size, **kw):
    first = (l1 or l2[0])[0]
    return dict(l1=l1, l2=l2, tone=tone, size=min(size, 128), start=ws(first), **kw)


GROUPS = [
    # hook
    G([0, 1], [[2, 3]], "lime", 104, start0=0.0),
    G([4, 5], [[6]], "white", 128, hero=[6]),
    G([7, 8], [[9, 10, 11, 12]], "white", 84),
    G([13], [[14]], "red", 128, hero=[14]),
    # 15-18 "No leads, no calls" -> zero cards
    G([], [[19]], "red", 128, hero=[19]),
    G([20, 21], [[22]], "lime", 128, hero=[22]),
    # 24-26 "started Verdexo Ventures" -> brand cutaway; 27-35 "We help …" -> who cards
    G([36], [[37, 38, 39]], "lime", 100),
    G([40, 41], [[42]], "lime", 128, hero=[42]),
    G([], [[43, 44]], "white", 110),
    # 45-50 "No fluff, no jargon, just results" -> nofluff cards
    G([51, 52], [[53, 54]], "white", 96),
    G([55, 56, 57, 58], [[59, 60]], "red", 112),
    G([61], [[62, 63]], "lime", 128, hero=[62, 63]),
    G([64, 65], [[66]], "white", 110),
    G([67, 68], [[69, 70]], "lime", 108),
    G([71], [[72]], "white", 128, hero=[72]),
    G([73, 74, 75], [[76, 77]], "lime", 128, hero=[76, 77]),
]
for g in GROUPS:
    if "start0" in g:
        g["start"] = g.pop("start0")

# Source windows where a scene carries the words itself (no captions).
SUPPRESS = [(6.10, 7.9), (10.44, 12.0), (12.58, 16.96), (20.84, 23.98)]
for g in GROUPS:
    for a, b in SUPPRESS:
        if a <= g["start"] < b:
            g["start"] = b
for i, g in enumerate(GROUPS):
    nxt = GROUPS[i + 1]["start"] if i + 1 < len(GROUPS) else 60  # last group holds through the end freeze
    g["end"] = min([nxt] + [a for a, _ in SUPPRESS if a > g["start"]])

# --------------------------------------------------------------------------- camera / colour (JS)
MOMENTS = """
        // ---------- Colour moments ----------
        tl.set("#bw-wrap", { opacity: 1 }, o(5.1));               // "doing NOTHING" drains to B&W
        tl.set("#flash", { opacity: 0.35 }, o(5.1));
        tl.to("#flash", { opacity: 0, duration: 0.16, ease: "power2.out" }, o(5.14));
        tl.set("#bw-wrap", { opacity: 0 }, o(6.1));               // colour back on the cut
        tl.set("#red-flag", { opacity: 1 }, o(7.92));             // "…NOTHING." red backdrop
        tl.to("#red-flag", { opacity: 0, duration: 0.2, ease: "power2.in" }, o(8.46) - 0.2);
        tl.to("#blur-wrap", { opacity: 1, duration: 0.26, ease: "power2.in" }, o(23.7));   // blur through the cut
        tl.to("#blur-wrap", { opacity: 0, duration: 0.14, ease: "power2.out" }, o(24.62) + 0.02);
        tl.set("#bw-wrap", { opacity: 1 }, o(25.88));             // "isn't working" -> B&W
        tl.set("#flash", { opacity: 0.3 }, o(25.88));
        tl.to("#flash", { opacity: 0, duration: 0.16, ease: "power2.out" }, o(25.92));
        tl.set("#bw-wrap", { opacity: 0 }, o(27.6));              // "let's fix that" -> colour returns
        tl.set("#flash", { opacity: 0.4 }, o(27.6));
        tl.to("#flash", { opacity: 0, duration: 0.2, ease: "power2.out" }, o(27.64));

        // ---------- Camera: alternate framing on every jump cut, punch only on stressed words ----------
        cam({ scale: 1.16, x: 0, y: 0 }, 0);
        cam({ scale: 1.04 }, 0, 0.45, "power3.out");
        cam({ scale: 1.07 }, 0.45, 1.25);
        cam({ scale: 1.14 }, 1.74, 0.14, "power3.out");   // "website"
        cam({ scale: 1.18 }, 1.9, 0.48);
        cam({ scale: 1.0 }, 2.64);                        // cut: but honestly
        cam({ scale: 1.05 }, 2.64, 2.46);
        cam({ scale: 1.16 }, 5.1, 0.14, "power3.out");    // "nothing"
        shake(5.14, 5);
        cam({ scale: 1.2 }, 5.24, 0.48);
        cam({ scale: 1.02 }, 6.1);                        // cut: no leads (room for the cards)
        cam({ scale: 1.05 }, 6.1, 1.8);
        cam({ scale: 1.14 }, 7.92, 0.14, "power3.out");   // "nothing."
        shake(7.96, 4);
        cam({ scale: 1.18 }, 8.06, 0.4);
        cam({ scale: 1.1 }, 9.06);                        // cut: that's exactly why
        cam({ scale: 1.12 }, 9.06, 0.5);
        cam({ scale: 1.2 }, 10.04, 0.14, "power3.out");   // "why"
        cam({ scale: 1.02 }, 12.58);                      // cut: we help (brand cutaway covers 10.44-12)
        cam({ scale: 1.05 }, 12.58, 4.4);
        cam({ scale: 1.1 }, 16.98);                       // jump zoom: actually get found online
        cam({ scale: 1.13 }, 16.98, 2.4);
        cam({ scale: 1.2 }, 19.44, 0.14, "power3.out");   // "clients"
        cam({ scale: 1.23 }, 19.6, 0.84);
        cam({ scale: 1.02 }, 20.84);                      // cut: no fluff
        cam({ scale: 1.05 }, 20.84, 2.2);
        cam({ scale: 1.12 }, 23.1, 0.14, "power3.out");   // "results"
        shake(23.14, 4);
        cam({ scale: 1.16 }, 23.24, 0.74, "power2.in");   // push into the blur
        cam({ scale: 1.08 }, 24.62);                      // cut: digital presence
        cam({ scale: 1.1 }, 24.62, 1.26);
        cam({ scale: 1.17 }, 25.88, 0.14, "power3.out");  // "isn't working"
        shake(25.92, 4);
        cam({ scale: 1.2 }, 26.02, 1.58);
        cam({ scale: 1.06 }, 27.6);                       // colour back
        cam({ scale: 1.13 }, 27.9, 0.14, "power3.out");   // "fix"
        cam({ scale: 1.02 }, 28.84);                      // cut: competitors (room for the search card)
        cam({ scale: 1.05 }, 28.84, 3.2);
        cam({ scale: 1.1 }, 32.06);                       // jump zoom: the question is
        cam({ scale: 1.17 }, 33.26, 0.14, "power3.out");  // "are you?"
        cam({ scale: 1.26 }, 33.4, 0.24 + 1.3, "sine.inOut");  // continues through the end freeze"""


# --------------------------------------------------------------------------- scene hosts
def L(src, start):
    """Local time inside a host that starts at source `start` (correct across jump cuts)."""
    return round(out(src) - out(start), 3)


ICONS = json.load(open(os.path.join(ROOT, "tools", "icons.json")))  # name -> codepoint (subset font)


def G_(name):
    return "&#x%s;" % ICONS[name]


def I(name):
    # Icon glyphs sit in stacked state tiles (base + cross-faded overlay) by design.
    return '<i class="ico" data-layout-allow-overlap>%s</i>' % G_(name)


HOSTS = [
    # (host id, template, source start, source end, CFG in LOCAL seconds)
    ("site", "site.html", 1.6, 5.72, dict(
        inAt=L(1.64, 1.6), typeAt=L(1.76, 1.6), typeDur=0.56, idleAt=L(4.06, 1.6), stopAt=L(5.12, 1.6))),
    ("zero", "zero.html", 6.1, 8.46, dict(
        a=L(6.22, 6.1) - 0.04, an=L(6.4, 6.1), b=L(7.06, 6.1) - 0.04, bn=L(7.18, 6.1), mute=L(7.62, 6.1), outAt=L(7.86, 6.1))),
    ("brand", "brand.html", 10.44, 12.0, dict(kick=[0.0, 0.06], mono=0.16, name=L(10.9, 10.44), name2=L(11.44, 10.44), dur=L(12.0, 10.44))),
    ("who", "slabs.html", 12.58, 16.96, dict(
        top=880, h=124, gap=14, outAt=L(16.78, 12.58),
        lead=dict(y=1296, words=["We", "help"], at=[L(12.72, 12.58), L(12.88, 12.58)]),
        slabs=[dict(text="Immigration consultants", at=L(13.14, 12.58), icon=I("flight_takeoff"), tone="lemon", halo="lemon", haloOff=L(14.7, 12.58)),
               dict(text="Study abroad agencies", at=L(14.74, 12.58), icon=I("school"), tone="lemon", halo="lemon", haloOff=L(16.2, 12.58)),
               dict(text="Clinics", at=L(16.22, 12.58), icon=I("medical_services"), tone="lemon", halo="lemon")])),
    ("found", "found.html", 16.96, 20.44, dict(
        found=L(17.64, 16.96) - 0.12, online=L(17.98, 16.96), icon=I("person_add"),
        toasts=[L(19.46, 16.96) - 0.08, L(19.8, 16.96) - 0.06, L(20.1, 16.96) - 0.06], outAt=L(20.28, 16.96))),
    ("nofluff", "slabs.html", 20.84, 23.98, dict(
        top=880, h=124, gap=14, outAt=None,
        slabs=[dict(text="Fluff", at=L(21.14, 20.84), icon=I("cloud"), tone="red", right=dict(kind="x", at=L(21.52, 20.84))),
               dict(text="Jargon", at=L(21.98, 20.84), icon=I("translate"), tone="red", right=dict(kind="x", at=L(22.38, 20.84))),
               dict(text="Just results", lemon=True, at=L(22.68, 20.84), icon=I("trending_up"), halo="lemon",
                    right=dict(kind="tick", at=L(23.1, 20.84)))])),
    ("status", "status.html", 24.62, 28.56, dict(inAt=L(24.9, 24.62), bad=L(25.9, 24.62), good=L(27.62, 24.62), outAt=L(28.36, 24.62))),
    ("search", "search.html", 28.84, 32.2, dict(
        inAt=L(29.2, 28.84), query="study abroad consultant", typeAt=L(29.46, 28.84), typeDur=0.62,
        rows=[L(30.26, 28.84), L(30.6, 28.84), L(30.88, 28.84)], star=I("star"), upIcon=I("trending_up"),
        google=L(31.34, 28.84) - 0.04, outAt=L(31.96, 28.84))),
]

# Footage-variant windows (source s): each becomes one <video> inside its wrap layer. Windows start
# well before their moment (the wrap's opacity gates them): sub-second clips fail the render's
# frame-coverage gate.
BW = [(4.4, 5.72), (25.3, 27.7)]
BLUR = [(22.9, 23.98), (24.62, 25.5)]
RED = (7.3, 8.46)  # red backdrop behind the subject cutout


def attrs(d):
    return json.dumps(d, separators=(",", ":")).replace("'", "&#39;")


def render_scene(hid, tpl, cfg, text=None):
    base = open(os.path.join(ROOT, "tools", "scenes", "_base.css")).read().rstrip("\n")
    S = open(os.path.join(ROOT, "tools", "scenes", tpl)).read()
    rep = {"__ID__": hid, "{{BASE_CSS}}": base, "{{CFG}}": json.dumps(cfg)}
    for k, v in (text or {}).items():
        rep["{{%s}}" % k] = v
    for k, v in rep.items():
        S = S.replace(k, v)
    S = re.sub(r"\{\{I:([a-z_]+)\}\}", lambda m: I(m.group(1)), S)
    S = re.sub(r"\{\{G:([a-z_]+)\}\}", lambda m: G_(m.group(1)), S)
    assert "{{" not in S, (tpl, S[S.index("{{"):S.index("{{") + 40])
    open(os.path.join(ROOT, "compositions", hid + ".html"), "w").write(S)


def variant(prefix, src, wins, track):
    return "\n".join(
        f'          <video id="{prefix}-{i}" class="clip" src="assets/media/{src}" muted playsinline data-start="{out(a)}" '
        f'data-media-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="{track}"></video>'
        for i, (a, b) in enumerate(wins)
    )


def main():
    T = open(os.path.join(ROOT, "tools", "index.template.html")).read()
    seg = seg_html().split("\n")
    videos = "\n".join("          " + l for l in seg if l.startswith("<video"))
    # Voice segments alternate between two tracks so abutting windows never share one.
    voice = "\n".join(
        "      " + l.replace('data-track-index="10"', f'data-track-index="{10 + k % 2}"')
        for k, l in enumerate(x for x in seg if x.startswith("<audio"))
    )
    hosts = []
    for h in HOSTS:
        hid, tpl, s, e, cfg = h[:5]
        render_scene(hid, tpl, cfg, h[5] if len(h) > 5 else None)
        hosts.append(
            f'      <div id="{hid}-slot" style="position: absolute; inset: 0">\n'
            f'        <div id="{hid}" data-composition-id="{hid}" data-composition-src="compositions/{hid}.html" '
            f'data-start="{out(s)}" data-duration="{round(out(e) - out(s), 3)}" data-track-index="4" data-width="1080" data-height="1920"></div>\n'
            f"      </div>"
        )
    rep = {
        "{{TOTAL}}": str(total()),
        "{{SEGMENTS}}": videos,
        "{{VOICE}}": voice,
        "{{HOSTS}}": "\n".join(hosts),
        "{{HOLD_START}}": str(out(SOURCE_END)),
        "{{HOLD_DUR}}": str(END_HOLD),
        "{{RED_START}}": str(out(RED[0])),
        "{{RED_DUR}}": str(round(RED[1] - RED[0], 3)),
        "{{BW}}": variant("bw", "bw.mp4", BW, 2),
        "{{BLUR}}": variant("blur", "blur.mp4", BLUR, 3),
        "{{CUTS}}": json.dumps(CUTS),
        "{{WORDS}}": json.dumps(W),
        "{{GROUPS}}": json.dumps(GROUPS),
        "{{MOMENTS}}": MOMENTS,
    }
    for k, v in rep.items():
        T = T.replace(k, v)
    assert "{{" not in T, "unfilled placeholder in index template"
    open(os.path.join(ROOT, "index.html"), "w").write(T)
    C = open(os.path.join(ROOT, "tools", "captions.template.html")).read()
    for k in ("{{CUTS}}", "{{WORDS}}", "{{GROUPS}}"):
        assert k in C, k
        C = C.replace(k, rep[k])
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(C)
    print("index.html written; duration", total(), "segments", len(segments()), "groups", len(GROUPS))


if __name__ == "__main__":
    main()
