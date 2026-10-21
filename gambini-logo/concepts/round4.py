# Round 4: all six suggested symbols, three variations each.
#   v1 Glow  — gradient symbol, horizontal lockup
#   v2 Line  — line-art symbol, horizontal lockup
#   v3 Solid — solid plum symbol, stacked lockup
import re
import cores
from build import *
from variations import c_word, center

cores.CORES.update({
    # Estate planning: the key to the family home, passed down. Family inside the bow.
    'key': dict(name='Legacy Key', note='The key to the family home, handed down.',
                shape='M45,57.55 A28,28 0 1 1 55,57.55 L55,70 L65,70 L65,76 L55,76 L55,79 L62,79 L62,85 L55,85 L55,90 L45,90 Z',
                fam='translate(25,11) scale(0.5)',
                extra=lambda ink: f'<circle cx="50" cy="30" r="22.5" fill="none" stroke="{ink}" stroke-width="1.3"/>'),
    # Wills and documents: the pen that writes the plan.
    'quill': dict(name='Quill Pen', note='The pen that writes the will and the plan.',
                  shape='M84,2 C58,6 30,28 28,62 L22,80 L18,89 L25,82 L33,66 C62,58 80,32 84,2 Z',
                  fam=None,
                  extra=lambda ink: f'<path d="M80,7 Q52,36 27,72" fill="none" stroke="{ink}" stroke-width="1.6" stroke-linecap="round"/>'),
    # Guardianship and elder law: two hands cradling the family.
    'hands': dict(name='Sheltering Hands', note='Two hands that cradle the family: guardianship + elder care.',
                  shape=('M50,90 C24,88 6,70 6,46 C6,39 10,35 14,38 C17,41 17,50 19,56 C23,68 35,76 50,78 Z '
                         'M50,90 C76,88 94,70 94,46 C94,39 90,35 86,38 C83,41 83,50 81,56 C77,68 65,76 50,78 Z'),
                  fam='translate(11,20) scale(0.78)', fam_out=True),
})

def horiz(mode, ink, big, acc):
    o = [heart(130, 150, 230, mode)]
    p, w = c_word(280, 190, big, acc); o.append(p)
    o.append(swash(320, 208, 280 + w - 30, 208, 6, acc))
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 30, 280 + w / 2, 262, ink, 2.6)[0])
    return svg(int(280 + w + 60), 300, ''.join(o))

def stacked(mode, ink, big, acc):
    W = 900; o = [heart(W / 2, 150, 260, mode)]
    _, w = c_word(0, 0, big, acc, 130, 90)
    o.append(c_word(W / 2 - w / 2, 400, big, acc, 130, 90)[0])
    o.append(swash(W / 2 - w / 2 + 30, 416, W / 2 + w / 2 - 30, 416, 6, acc))
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 30, W / 2, 468, ink, 2.6)[0])
    return svg(W, 510, ''.join(o))

def variant(v, m):
    if m == 'mono':
        return (horiz if v != 'v3' else stacked)('mono', '#000', '#000', '#000')
    if v == 'v1': return horiz('color', PLUM, 'url(#metal)', LAV)
    if v == 'v2': return horiz('line', PLUM, PLUM, LAV)
    return stacked('solid', PLUM, PLUM, LAV)

VNAMES = {'v1': 'Glow', 'v2': 'Line', 'v3': 'Solid stacked'}
ORDER = ['seal', 'arch', 'crest', 'key', 'quill', 'hands']

if __name__ == '__main__':
    for core in ORDER:
        cores.use(core)
        for v in VNAMES:
            for m in ('color', 'mono'):
                s = variant(v, m)
                open(f'round4/{core}-{v}-{m}.svg', 'w').write(s)
                cairosvg.svg2png(bytestring=s.encode(), write_to=f'round4/{core}-{v}-{m}.png', output_width=1200)
    CW, CH, PAD = 640, 300, 22
    W = PAD + 3 * (CW + PAD)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {len(ORDER)*(CH+PAD+40)+90}">',
         '<rect width="100%" height="100%" fill="#F6F5F2"/>',
         f'<text x="{PAD}" y="50" font-family="sans-serif" font-size="30" font-weight="700" fill="#222">Gambini Law — 6 symbols × 3 variations (round 4)</text>']
    y = 80
    for core in ORDER:
        c = cores.CORES[core]
        o.append(f'<text x="{PAD}" y="{y+26}" font-family="sans-serif" font-size="22" font-weight="700" fill="#333">{c["name"]}'
                 f'<tspan font-weight="400" fill="#666"> — {c["note"]}   (1 Glow · 2 Line · 3 Solid stacked)</tspan></text>')
        y += 40
        for i, v in enumerate(VNAMES):
            x = PAD + i * (CW + PAD)
            src = open(f'round4/{core}-{v}-color.svg').read()
            vb = re.search(r'viewBox="([^"]+)"', src).group(1)
            inner = src[src.index('>') + 1:src.rindex('</svg>')]
            o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="14" fill="#fff" stroke="#E2DFE8"/>')
            o.append(f'<svg x="{x+16}" y="{y+16}" width="{CW-32}" height="{CH-32}" viewBox="{vb}">{inner}</svg>')
        y += CH + PAD
    o.append('</svg>')
    s = ''.join(o)
    open('round4/round4.svg', 'w').write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to='round4/round4.png', output_width=2000)
    print('ok')
