#!/usr/bin/env python3
"""Generate the isometric delivery-pipeline illustration in the hero card.

Emits three fragments into the current directory:

  iso.css          -> paste into the <style> block in index.html
  iso.svg.html     -> the <svg> inside <div class="iz-wrap"> in the hero card
  iso.status.html  -> the rotating status line under the illustration

Everything runs off one 12s timeline: each animated element gets its own
keyframes with an absolute window inside that loop, so the phases stay in
sync. Base opacity in the markup is the finished state, which is what shows
when prefers-reduced-motion disables the animations.
"""

T = 12.0          # loop duration, seconds
CX = 170.0        # screen centre x
S = 130.0         # plane footprint, local units
R = 0.32          # projection flatness: a plane is 2*S wide, 2*S*R tall
SLAB = 6.0        # plane thickness, screen px

L_TERM = 14.0     # screen y of each plane's back corner
L_CI = 110.0
L_RUN = 206.0

css = []
svg = []


# ---- geometry ------------------------------------------------------------

def iso(x, y, cy0, lift=0.0):
    return (CX + (x - y), cy0 + (x + y) * R - lift)


def pts(seq):
    return " ".join("%.2f,%.2f" % p for p in seq)


def rhombus(cy0, a=0.0, b=S, lift=0.0):
    """Top face of a square footprint [a,b]^2 on the plane at cy0."""
    return [iso(a, a, cy0, lift), iso(b, a, cy0, lift),
            iso(b, b, cy0, lift), iso(a, b, cy0, lift)]


def quad(x0, y0, x1, y1, cy0, lift=0.0):
    return [iso(x0, y0, cy0, lift), iso(x1, y0, cy0, lift),
            iso(x1, y1, cy0, lift), iso(x0, y1, cy0, lift)]


def cube(x0, y0, x1, y1, cy0, h, cls_t, cls_l, cls_r, extra=""):
    """Isometric box standing on the plane. Returns (top, left, right) polys."""
    top = quad(x0, y0, x1, y1, cy0, h)
    left = [iso(x0, y1, cy0, h), iso(x1, y1, cy0, h),
            iso(x1, y1, cy0, 0), iso(x0, y1, cy0, 0)]
    right = [iso(x1, y0, cy0, h), iso(x1, y1, cy0, h),
             iso(x1, y1, cy0, 0), iso(x1, y0, cy0, 0)]
    return ('<polygon class="%s" points="%s"%s/>' % (cls_l, pts(left), extra) +
            '<polygon class="%s" points="%s"%s/>' % (cls_r, pts(right), extra) +
            '<polygon class="%s" points="%s"%s/>' % (cls_t, pts(top), extra))


def slab(cy0, label):
    """A plane: top face plus two front faces giving it thickness."""
    top = rhombus(cy0)
    L, B, R = iso(0, S, cy0), iso(S, S, cy0), iso(S, 0, cy0)
    left = [L, B, (B[0], B[1] + SLAB), (L[0], L[1] + SLAB)]
    right = [B, R, (R[0], R[1] + SLAB), (B[0], B[1] + SLAB)]
    return ('<!-- %s -->' % label +
            '<polygon class="iz-sl" points="%s"/>' % pts(left) +
            '<polygon class="iz-sr" points="%s"/>' % pts(right) +
            '<polygon class="iz-top" points="%s"/>' % pts(top))


# ---- keyframe helpers ----------------------------------------------------

def p(t):
    return round(max(0.0, min(100.0, t / T * 100.0)), 3)


def fmt(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def kf_on(name, on, off, ramp=0.28):
    """Fade in at `on`, hold, fade out at `off`."""
    a, b, c, d = p(on), p(on + ramp), p(off), p(off + ramp)
    stops = []
    if a > 0:
        stops.append("0%%,%s%%{opacity:0}" % fmt(a))
    else:
        stops.append("0%{opacity:0}")
    stops.append("%s%%,%s%%{opacity:1}" % (fmt(b), fmt(c)))
    stops.append("%s%%,100%%{opacity:0}" % fmt(d))
    css.append("@keyframes %s{%s}" % (name, "".join(stops)))


def kf_blink(name, start, end, period=0.62):
    """Caret blink inside a window."""
    stops = ["0%{opacity:0}"]
    t = start
    while t + period <= end:
        stops.append("%s%%{opacity:0}" % fmt(p(t)))
        stops.append("%s%%{opacity:1}" % fmt(p(t + 0.02)))
        stops.append("%s%%{opacity:1}" % fmt(p(t + period * 0.5)))
        stops.append("%s%%{opacity:0}" % fmt(p(t + period * 0.52)))
        t += period
    stops.append("100%{opacity:0}")
    css.append("@keyframes %s{%s}" % (name, "".join(stops)))


def kf_drop(name, start, dur, dy):
    """A packet falling from one plane to the next."""
    a, b, c, d = p(start), p(start + 0.12), p(start + dur - 0.12), p(start + dur)
    css.append(
        "@keyframes %s{0%%,%s%%{opacity:0;transform:translateY(0)}"
        "%s%%{opacity:1;transform:translateY(0)}"
        "%s%%{opacity:1;transform:translateY(%spx)}"
        "%s%%,100%%{opacity:0;transform:translateY(%spx)}}"
        % (name, fmt(a), fmt(b), fmt(c), fmt(dy), fmt(d), fmt(dy)))


def kf_travel(name, start, dur, dx, dy):
    """A token sliding along the pipeline between two stations."""
    a, b, c, d = p(start), p(start + 0.1), p(start + dur - 0.1), p(start + dur)
    css.append(
        "@keyframes %s{0%%,%s%%{opacity:0;transform:translate(0,0)}"
        "%s%%{opacity:1;transform:translate(0,0)}"
        "%s%%{opacity:1;transform:translate(%spx,%spx)}"
        "%s%%,100%%{opacity:0;transform:translate(%spx,%spx)}}"
        % (name, fmt(a), fmt(b), fmt(c), fmt(dx), fmt(dy), fmt(d),
           fmt(dx), fmt(dy)))


# ---- static scaffolding --------------------------------------------------

css.append("/* isometric delivery pipeline */")
css.append(".iz-wrap{position:relative;margin:16px -4px 0}")
css.append(".iz svg{display:block;width:100%;height:auto;overflow:visible}")
css.append(".iz-top{fill:rgba(var(--ink-rgb),.035);stroke:rgba(var(--ink-rgb),.40);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-sl{fill:rgba(var(--ink-rgb),.13);stroke:rgba(var(--ink-rgb),.34);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-sr{fill:rgba(var(--ink-rgb),.06);stroke:rgba(var(--ink-rgb),.34);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-strut{stroke:rgba(var(--ink-rgb),.30);stroke-width:1;"
           "stroke-dasharray:2 5;fill:none}")
css.append(".iz-screen{fill:rgba(var(--ink-rgb),.07);stroke:rgba(var(--ink-rgb),.30);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-bar{fill:rgba(var(--ink-rgb),.42)}")
css.append(".iz-bar-a{fill:var(--accent)}")
css.append(".iz-bt{fill:rgba(var(--ink-rgb),.05);stroke:rgba(var(--ink-rgb),.45);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-bl{fill:rgba(var(--ink-rgb),.16);stroke:rgba(var(--ink-rgb),.40);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-br{fill:rgba(var(--ink-rgb),.09);stroke:rgba(var(--ink-rgb),.40);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-lt{fill:var(--accent);fill-opacity:.46;stroke:var(--accent);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-ll{fill:var(--accent);fill-opacity:.26;stroke:var(--accent);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-lr{fill:var(--accent);fill-opacity:.15;stroke:var(--accent);"
           "stroke-width:1;stroke-linejoin:round}")
css.append(".iz-wire{stroke:rgba(var(--ink-rgb),.34);stroke-width:1;fill:none}")
css.append(".iz-pkt{fill:var(--accent);stroke:var(--accent);stroke-width:1;"
           "stroke-linejoin:round}")
css.append(".iz-float{animation:izFloat 6s ease-in-out infinite}")
css.append("@keyframes izFloat{0%,100%{transform:translateY(0)}"
           "50%{transform:translateY(-3.5px)}}")

# ---- layer: struts between planes ---------------------------------------

def struts(a, b):
    """Dashed drop lines hanging from plane `a` down to plane `b`. Only the two
    side corners: a strut at the front or back corner would be occluded by the
    plane it lands on."""
    out = []
    for corner in ((0, S), (S, 0)):
        x0, y0 = iso(corner[0], corner[1], a)
        x1, y1 = iso(corner[0], corner[1], b)
        out.append('<line class="iz-strut" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>'
                   % (x0, y0 + SLAB, x1, y1))
    return "".join(out)

# ---- layer 1: runtime / cluster -----------------------------------------

run = [slab(L_RUN, "runtime")]
cells = []
for j in range(3):
    for i in range(3):
        cells.append((i, j))
cells.sort(key=lambda c: c[0] + c[1])
order = [(1, 1), (0, 1), (1, 0), (2, 1), (1, 2), (0, 0), (2, 0), (0, 2), (2, 2)]
POD_START, POD_STEP = 6.55, 0.30
POD_OFF = 11.35
for (i, j) in cells:
    x0 = 8 + i * 40.0
    y0 = 8 + j * 40.0
    x1, y1 = x0 + 32, y0 + 32
    run.append(cube(x0, y0, x1, y1, L_RUN, 10, "iz-bt", "iz-bl", "iz-br"))
    k = order.index((i, j))
    name = "izPod%d" % k
    kf_on(name, POD_START + k * POD_STEP, POD_OFF, ramp=0.22)
    css.append(".iz-pod%d{animation:%s %ss linear infinite}" % (k, name, fmt(T)))
    run.append('<g class="iz-pod%d" opacity="1">%s</g>'
               % (k, cube(x0, y0, x1, y1, L_RUN, 10, "iz-lt", "iz-ll", "iz-lr")))

# ---- layer 2: CI stations ------------------------------------------------

ci = [slab(L_CI, "ci")]
station_x = [20.0, 65.0, 110.0]
NW, NH = 14.0, 13.0
# wire runs only in the gaps between stations, so the boxes do not cover it
for gap in ((station_x[0] + NW, station_x[1] - NW),
            (station_x[1] + NW, station_x[2] - NW)):
    w0, w1 = iso(gap[0], 65, L_CI), iso(gap[1], 65, L_CI)
    ci.append('<line class="iz-wire" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>'
              % (w0[0], w0[1], w1[0], w1[1]))
    mid = (gap[0] + gap[1]) * 0.5
    ci.append('<polyline class="iz-wire" points="%s"/>'
              % pts([iso(mid - 4, 59, L_CI), iso(mid + 4, 65, L_CI),
                     iso(mid - 4, 71, L_CI)]))

CI_ON = [3.05, 4.05, 5.05]
CI_OFF = 11.2
for n, sx in enumerate(station_x):
    x0, y0 = sx - NW, 65 - NW
    x1, y1 = sx + NW, 65 + NW
    ci.append(cube(x0, y0, x1, y1, L_CI, NH, "iz-bt", "iz-bl", "iz-br"))
    kf_on("izCi%d" % n, CI_ON[n], CI_OFF, ramp=0.2)
    css.append(".iz-ci%d{animation:izCi%d %ss linear infinite}" % (n, n, fmt(T)))
    ci.append('<g class="iz-ci%d" opacity="1">%s</g>'
              % (n, cube(x0, y0, x1, y1, L_CI, NH, "iz-lt", "iz-ll", "iz-lr")))

# token travelling station -> station
tok_dx = station_x[1] - station_x[0]
for n, (start, dur) in enumerate(((3.55, 0.45), (4.55, 0.45))):
    kf_travel("izTok%d" % n, start, dur, tok_dx, tok_dx * R)
    css.append(".iz-tok%d{animation:izTok%d %ss linear infinite}" % (n, n, fmt(T)))
    tx, ty = iso(station_x[n], 65, L_CI, NH + 7)
    ci.append('<g class="iz-tok%d" opacity="0"><polygon class="iz-pkt" points="%s"/></g>'
              % (n, pts([(tx, ty - 4), (tx + 4.5, ty), (tx, ty + 4), (tx - 4.5, ty)])))

# ---- layer 3: terminal ---------------------------------------------------

term = [slab(L_TERM, "terminal")]
term.append('<polygon class="iz-screen" points="%s"/>'
            % pts(rhombus(L_TERM, 9, 121)))
# title bar along the back edge
term.append('<polygon class="iz-screen" points="%s"/>'
            % pts(quad(9, 9, 121, 24, L_TERM)))
for d in (17.0, 27.0, 37.0):
    dx, dy = iso(d, 16.5, L_TERM)
    term.append('<ellipse class="iz-bar" cx="%.2f" cy="%.2f" rx="2.6" ry="1.5" '
                'opacity=".5"/>' % (dx, dy))


def bar(x0, x1, ly, cls, thick=9.0):
    return '<polygon class="%s" points="%s"/>' % (cls, pts(quad(x0, ly, x1, ly + thick, L_TERM)))


# line 1: prompt + three "words" of the command
term.append(bar(15, 23, 34, "iz-bar-a"))
WORDS = [(28, 50), (55, 82), (87, 116)]
for n, (x0, x1) in enumerate(WORDS):
    kf_on("izWd%d" % n, 0.35 + n * 0.30, 11.5, ramp=0.1)
    css.append(".iz-wd%d{animation:izWd%d %ss linear infinite}" % (n, n, fmt(T)))
    term.append('<g class="iz-wd%d" opacity="1">%s</g>' % (n, bar(x0, x1, 34, "iz-bar-a")))

# output lines
for n, (x0, x1, ly, t0) in enumerate(((15, 96, 56, 1.55), (15, 78, 78, 1.90))):
    kf_on("izOut%d" % n, t0, 11.5, ramp=0.12)
    css.append(".iz-out%d{animation:izOut%d %ss linear infinite}" % (n, n, fmt(T)))
    term.append('<g class="iz-out%d" opacity="1">%s</g>'
                % (n, bar(x0, x1, ly, "iz-bar")))

# caret
kf_blink("izCaret", 0.2, 2.35)
css.append(".iz-caret{animation:izCaret %ss linear infinite}" % fmt(T))
term.append('<g class="iz-caret" opacity="0">%s</g>' % bar(15, 23, 100, "iz-bar-a"))

# ---- packets between planes ---------------------------------------------

drops = []
for n, (cy0, start) in enumerate(((L_TERM, 2.45), (L_CI, 5.85))):
    kf_drop("izDrop%d" % n, start, 0.62, 96.0)
    css.append(".iz-drop%d{animation:izDrop%d %ss cubic-bezier(.45,0,.55,1) infinite}"
               % (n, n, fmt(T)))
    dx, dy = iso(65, 65, cy0, -SLAB - 6)
    drops.append('<g class="iz-drop%d" opacity="0"><polygon class="iz-pkt" points="%s"/></g>'
                 % (n, pts([(dx, dy - 5), (dx + 5.5, dy), (dx, dy + 5), (dx - 5.5, dy)])))

# ---- assemble ------------------------------------------------------------

# struts hang from the plane above, so they drift with it
ci.append(struts(L_CI, L_RUN))
term.append(struts(L_TERM, L_CI))

body = (
    '<g class="iz-float" style="animation-duration:7s">%s</g>' % "".join(run) +
    '<g class="iz-float" style="animation-duration:6.4s;animation-delay:-1.1s">%s</g>' % "".join(ci) +
    '<g class="iz-float" style="animation-duration:5.8s;animation-delay:-2.3s">%s</g>' % "".join(term) +
    "".join(drops)
)

ground = iso(S, S, L_RUN)[1] + SLAB
shadow = ('<defs><radialGradient id="izShadow">'
          '<stop offset="0" stop-color="rgba(var(--ink-rgb),.22)"/>'
          '<stop offset="1" stop-color="rgba(var(--ink-rgb),0)"/></radialGradient></defs>'
          '<ellipse cx="%.1f" cy="%.1f" rx="122" ry="15" fill="url(#izShadow)"/>'
          % (CX, ground + 14))
body = shadow + body

svg = ('<svg class="iz" viewBox="0 0 340 328" role="img" aria-label="Isometric '
       'illustration: a terminal command flows down through a three-stage CI '
       'pipeline into a nine-node cluster that rolls out healthy.">'
       + body + '</svg>')

# ---- status line under the illustration ---------------------------------

STATUS = [("$", "git push origin main", 0.05, 2.62),
          ("[ci]", "build \u00b7 test \u00b7 scan", 2.85, 5.95),
          ("[ok]", "rollout 3/3 \u00b7 healthy", 6.35, 11.7)]
lines = []
for n, (mark, text, on, off) in enumerate(STATUS):
    kf_on("izSt%d" % n, on, off, ramp=0.18)
    css.append(".iz-st%d{animation:izSt%d %ss linear infinite}" % (n, n, fmt(T)))
    lines.append('<span class="iz-line iz-st%d"%s><span class="iz-mark">%s</span> %s</span>'
                 % (n, "" if n == len(STATUS) - 1 else ' style="opacity:0"', mark, text))
css.append(".iz-status{position:relative;height:17px;margin-top:14px;"
           "padding-top:11px;border-top:1px solid rgba(var(--ink-rgb),.3)}")
css.append(".iz-line{position:absolute;left:0;top:11px;white-space:nowrap;"
           "font-size:11.5px;letter-spacing:.02em;color:rgba(var(--ink-rgb),.7)}")
css.append(".iz-mark{color:var(--accent)}")

open("iso.status.html", "w").write('<div class="iz-status" aria-hidden="true">%s</div>'
                                   % "".join(lines))
open("iso.svg.html", "w").write(svg)
open("iso.css", "w").write("\n".join(css) + "\n")
print("svg bytes:", len(svg))
print("css bytes:", len("\n".join(css)))
