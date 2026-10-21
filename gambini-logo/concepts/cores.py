# Round 3: new core symbols for her practice, replacing the heart.
import math, re
import build, variations
from build import *

def scallop(cx=50, cy=45, r=44, n=24, d=2.6):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n - math.pi / 2
        rr = r if i % 2 == 0 else r - d
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    p = f'M{pts[0][0]:.2f},{pts[0][1]:.2f} '
    for i in range(1, len(pts), 2):
        c, e = pts[i], pts[(i + 1) % len(pts)]
        p += f'Q{c[0]:.2f},{c[1]:.2f} {e[0]:.2f},{e[1]:.2f} '
    return p + 'Z'

CORES = {
    # Estate (home) + guardianship (shelter): a doorway arch the generations stand under.
    'arch': dict(name='Guardian Arch',
                 note='A home doorway that shelters four generations: estate + guardianship.',
                 shape='M12,90 L12,42 A38,38 0 0 1 88,42 L88,90 Z',
                 fam='translate(0,16)',
                 extra=lambda ink: f'<path d="M20,90 L20,43 A30,30 0 0 1 80,43 L80,90" fill="none" stroke="{ink}" stroke-width="1.4"/>'
                                   f'<path d="M46.5,4.5 L53.5,4.5 L52,12 L48,12 Z" fill="{ink}"/>'),
    # Wills and trusts: the wax seal that makes a plan official.
    'seal': dict(name='Legacy Seal',
                 note='The wax seal on a signed will: the family inside a sealed plan.',
                 shape=scallop(),
                 fam='translate(9.5,4) scale(0.82)',
                 extra=lambda ink: f'<circle cx="50" cy="45" r="35" fill="none" stroke="{ink}" stroke-width="1.4"/>'),
    # Protection + the Gambini family name: a family crest.
    'crest': dict(name='Family Crest',
                  note='A family crest: "Let our family protect your family," and her family name.',
                  shape='M12,4 Q50,12 88,4 L88,40 C88,64 72,79 50,90 C28,79 12,64 12,40 Z',
                  fam='translate(4,2) scale(0.92)',
                  extra=lambda ink: f'<path d="M18,10 Q50,17 82,10" fill="none" stroke="{ink}" stroke-width="1.4"/>'),
}

def use(core):
    c = CORES[core]
    build.CORE.update(shape=c['shape'], fam=c['fam'], extra=c['extra'])

def symbol(mode):
    return svg(256, 256, heart(128, 124, 220, mode), bg=None)

if __name__ == '__main__':
    for core in CORES:
        use(core)
        outs = {'symbol': symbol, 'a': concept_a, 'b': concept_b, 'c': concept_c, 'a3': variations.a3}
        for k, fn in outs.items():
            for m in ('color', 'mono'):
                v = fn(m)
                open(f'cores/{core}-{k}-{m}.svg', 'w').write(v)
                cairosvg.svg2png(bytestring=v.encode(), write_to=f'cores/{core}-{k}-{m}.png',
                                 output_width=512 if k == 'symbol' else 1200)
    # contact sheet: one row per core -> symbol, A, B, C
    CW, CH, SW, PAD = 520, 300, 300, 22
    cols = [('symbol', SW), ('a', CW), ('b', CW), ('c', CW)]
    W = PAD + sum(w + PAD for _, w in cols)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {3*(CH+PAD+40)+90}">',
         '<rect width="100%" height="100%" fill="#F6F5F2"/>',
         f'<text x="{PAD}" y="50" font-family="sans-serif" font-size="30" font-weight="700" fill="#222">Gambini Law — new core symbols (round 3)</text>']
    y = 80
    for core, c in CORES.items():
        o.append(f'<text x="{PAD}" y="{y+26}" font-family="sans-serif" font-size="22" font-weight="700" fill="#333">{c["name"]}'
                 f'<tspan font-weight="400" fill="#666"> — {c["note"]}</tspan></text>')
        x = PAD; y += 40
        for k, w in cols:
            src = open(f'cores/{core}-{k}-color.svg').read()
            vb = re.search(r'viewBox="([^"]+)"', src).group(1)
            inner = src[src.index('>') + 1:src.rindex('</svg>')]
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{CH}" rx="14" fill="#fff" stroke="#E2DFE8"/>')
            o.append(f'<svg x="{x+16}" y="{y+16}" width="{w-32}" height="{CH-32}" viewBox="{vb}">{inner}</svg>')
            x += w + PAD
        y += CH + PAD
    o.append('</svg>')
    s = ''.join(o)
    open('cores/cores.svg', 'w').write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to='cores/cores.png', output_width=2200)
    print('ok')
