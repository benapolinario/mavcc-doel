# Contact sheet of the round-2 variations (3 rows x 3 columns).
import re, cairosvg
names = {'a1': 'A1 · Silver metal', 'a2': 'A2 · Flat two-tone', 'a3': 'A3 · Full wrap swash',
         'b1': 'B1 · Ring badge', 'b2': 'B2 · Stacked', 'b3': 'B3 · Flat + swash under name',
         'c1': 'C1 · Line-art heart', 'c2': 'C2 · Stacked', 'c3': 'C3 · Heart tip into swash'}
CW, CH, PAD = 620, 330, 24
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {3*CW+4*PAD} {3*CH+4*PAD+60}">',
     f'<rect width="100%" height="100%" fill="#F6F5F2"/>',
     f'<text x="{PAD}" y="48" font-family="sans-serif" font-size="30" font-weight="700" fill="#222">Gambini Law — round 2 variations</text>']
for i, k in enumerate(names):
    r, c = divmod(i, 3); x = PAD + c * (CW + PAD); y = 70 + PAD + r * (CH + PAD)
    src = open(f'variations/{k}-color.svg').read()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    inner = src[src.index('>') + 1:src.rindex('</svg>')]
    o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="14" fill="#fff" stroke="#E2DFE8"/>')
    o.append(f'<svg x="{x+20}" y="{y+20}" width="{CW-40}" height="{CH-80}" viewBox="{vb}">{inner}</svg>')
    o.append(f'<text x="{x+24}" y="{y+CH-24}" font-family="sans-serif" font-size="22" font-weight="600" fill="#333">{names[k]}</text>')
o.append('</svg>')
s = ''.join(o)
open('variations/variations.svg', 'w').write(s)
cairosvg.svg2png(bytestring=s.encode(), write_to='variations/variations.png', output_width=1960)
