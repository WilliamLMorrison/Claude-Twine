"""Generate a dusk forest + wizard tower SVG background (deterministic)."""
import random, sys
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 7)
WARM = len(sys.argv)>3
W, H = 1600, 1000
out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">')
a('<defs>'
  '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#0e1424"/><stop offset=".45" stop-color="#1d2b44"/>'
  '<stop offset=".72" stop-color="#3f4a5e"/><stop offset=".86" stop-color="#7a6a5c"/>'
  '<stop offset="1" stop-color="#a07e5e"/></linearGradient>'
  '<radialGradient id="moon" cx=".5" cy=".5" r=".5">'
  '<stop offset="0" stop-color="#f3ead2" stop-opacity=".95"/><stop offset=".18" stop-color="#e9dfc4" stop-opacity=".9"/>'
  '<stop offset=".22" stop-color="#d9cfb4" stop-opacity=".25"/><stop offset="1" stop-color="#d9cfb4" stop-opacity="0"/></radialGradient>'
  '<radialGradient id="win" cx=".5" cy=".5" r=".5">'
  '<stop offset="0" stop-color="#ffd58a" stop-opacity=".9"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>'
  '<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#9aa6b2" stop-opacity="0"/><stop offset=".5" stop-color="#9aa6b2" stop-opacity=".18"/>'
  '<stop offset="1" stop-color="#9aa6b2" stop-opacity="0"/></linearGradient>'
  '</defs>')
a(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
# stars
for _ in range(170):
    x, y = random.uniform(0, W), random.uniform(0, H * 0.55)
    r = random.choice([0.6, 0.8, 1.0, 1.3])
    o = random.uniform(0.25, 0.85) * (1 - y / (H * 0.7))
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#f1ecdf" opacity="{o:.2f}"/>')
# moon + glow
a('<circle cx="1400" cy="170" r="260" fill="url(#moon)"/>')
a('<circle cx="1400" cy="170" r="46" fill="#efe6cc"/>')
a('<circle cx="1383" cy="158" r="9" fill="#ddd3b6" opacity=".6"/><circle cx="1418" cy="185" r="6" fill="#ddd3b6" opacity=".5"/>')

def ridge(base, amp, color, step=40):
    pts = [f"0,{H}"]
    y = base
    for x in range(0, W + step, step):
        y += random.uniform(-amp, amp)
        y = max(base - amp * 3, min(base + amp * 3, y))
        pts.append(f"{x},{y:.0f}")
    pts.append(f"{W},{H}")
    a(f'<polygon points="{" ".join(pts)}" fill="{color}"/>')

ridge(640, 22, "#33405a")
ridge(690, 16, "#2b364c")

def pines(base, hmin, hmax, color, density):
    x = -30
    while x < W + 30:
        h = random.uniform(hmin, hmax)
        w = h * random.uniform(0.28, 0.36)
        y = base + random.uniform(-12, 12)
        # tiered pine silhouette
        tiers = 4
        d = []
        for t in range(tiers):
            top = y - h + t * h * 0.2
            bot = y - h + (t + 1) * h * 0.26
            half = w * (0.35 + t * 0.2) / 2
            d.append(f"M{x:.0f},{top:.0f} L{x - half:.0f},{bot:.0f} L{x + half:.0f},{bot:.0f}Z")
        d.append(f"M{x - w * 0.5:.0f},{y - h * 0.22:.0f} L{x + w * 0.5:.0f},{y - h * 0.22:.0f} L{x + w*0.5:.0f},{H} L{x - w*0.5:.0f},{H}Z")
        a(f'<path d="{" ".join(d)}" fill="{color}"/>')
        x += w * density * random.uniform(0.5, 1.0)

pines(760, 90, 150, "#253047", 0.9)
a(f'<rect x="0" y="690" width="{W}" height="140" fill="url(#mist)"/>')

# wizard tower (behind front trees)
tx = 190
a(f'<path d="M{tx-34},1000 L{tx-30},300 L{tx+30},300 L{tx+34},1000Z" fill="#1a2236"/>')
a(f'<path d="M{tx-44},300 L{tx+44},300 L{tx+40},284 L{tx-40},284Z" fill="#1a2236"/>')
a(f'<path d="M{tx-40},284 L{tx},150 L{tx+40},284Z" fill="#1a2236"/>')
for wy in (360, 470, 590):
    a(f'<circle cx="{tx}" cy="{wy+10}" r="30" fill="url(#win)" opacity=".55"/>')
    a(f'<rect x="{tx-5}" y="{wy}" width="10" height="20" rx="5" fill="#f0c27a" opacity=".85"/>')

pines(860, 140, 230, "#1a2234", 0.85)
a(f'<rect x="0" y="800" width="{W}" height="120" fill="url(#mist)"/>')
pines(1000, 240, 380, "#10162a", 0.8)
a('</svg>')
svg = "".join(out)
if WARM:
    for a_, b_ in [("#0e1424","#1a1020"),("#1d2b44","#3a2238"),("#3f4a5e","#6b3c3e"),("#7a6a5c","#b0684a"),("#a07e5e","#d79a5e"),
                   ("#33405a","#4a2c3c"),("#2b364c","#3b2433"),("#253047","#2e1c2a"),("#1a2234","#211520"),("#10162a","#140c16"),
                   ("#1a2236","#24161f"),("#9aa6b2","#d6a888")]:
        svg = svg.replace(a_, b_)
open(sys.argv[1], 'w').write(svg)
