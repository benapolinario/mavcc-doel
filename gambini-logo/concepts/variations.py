# Round 2: three variations each of concepts A, B and C.
from build import *

TAG1, TAG2 = 'LET OUR FAMILY', 'PROTECT YOUR FAMILY'
SERV = 'ESTATE PLANNING  ·  PROBATE  ·  GUARDIANSHIP  ·  ELDER LAW'

def center(s, font, size, cx, y, fill, tr=0):
    _, w = txt(s, font, size, 0, 0, fill, tr)
    return txt(s, font, size, cx - w / 2, y, fill, tr)

def a_base(mode, big, small, acc, ink, rules=False, heart_w=128, wrap=False):
    o = []
    p, _ = txt('G', F, 330, 20, 272, big); o.append(p)
    o.append(heart(20 + 0.330 * 420, 272 - 0.330 * 352, heart_w, mode))
    p, aw = txt('AMBINI', F, 118, 272, 178, small, 4); o.append(p)
    lx = 272 + aw + 14
    p, _ = txt('L', F, 330, lx, 272, big); o.append(p)
    p, _ = txt('AW', F, 118, lx + 0.33 * 420, 178, small, 4); o.append(p)
    cx = 272 + aw / 2
    p, tw = center(TAG1, FS, 34, cx, 222, ink, 3); o.append(p)
    o.append(center(TAG2, FS, 34, cx, 262, ink, 3)[0])
    if rules:  # "— LET OUR FAMILY —" like the original
        for x0 in (cx - tw / 2 - 64, cx + tw / 2 + 14):
            o.append(f'<rect x="{x0:.1f}" y="210" width="50" height="2" fill="{acc}"/>')
    if wrap:  # swash starts on G's left side, runs under everything, curls up at the end
        d = ('M40,170 C14,236 50,292 160,288 L700,282 C900,276 1010,280 1060,262 '
             'C1084,252 1092,232 1086,214 C1100,240 1088,272 1060,280 '
             'C1000,296 900,292 700,292 L160,298 C40,302 2,236 40,170 Z')
        o.append(f'<path d="{d}" fill="{acc}"/>')
    else:
        o.append(swash(120, 270, lx + 350, 270, 10, acc))
    w = int(lx + 430)
    o.append(center(SERV, FS, 30, w / 2, 350, ink, 2)[0])
    return svg(w, 380, ''.join(o))

def a1(m):  # Silver metal, closest to her original
    c = m == 'color'
    return a_base(m, 'url(#silver)' if c else '#000', 'url(#silver)' if c else '#000',
                  '#A895C2' if c else '#000', PLUM if c else '#000', rules=True)
def a2(m):  # Flat two-tone: plum G/L, lavender small letters
    c = m == 'color'
    return a_base(m, PLUM if c else '#000', LAV if c else '#000', LAV if c else '#000',
                  PLUM if c else '#000', rules=True, heart_w=134)
def a3(m):  # Full wrap swash
    c = m == 'color'
    return a_base(m, 'url(#metal)' if c else '#000', 'url(#metal)' if c else '#000',
                  LAV if c else '#000', PLUM if c else '#000', wrap=True)

def wordmark_block(x, ink, acc, w_target=None):
    o = []
    p, w1 = txt('GAMBINI LAW', F, 92, x, 150, ink, 6); o.append(p)
    o.append(f'<rect x="{x+2}" y="172" width="{w1-4:.1f}" height="2" fill="{acc}"/>')
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 31, x + w1 / 2, 214, ink, 2.4)[0])
    o.append(center('ESTATE PLANNING · PROBATE · GUARDIANSHIP · ELDER LAW', FS, 23, x + w1 / 2, 252, ink, 1.6)[0])
    return ''.join(o), w1

def b1(m):  # Monogram in a thin ring
    c = m == 'color'; ink = PLUM if c else '#000'; acc = LAV if c else '#000'
    o = [f'<circle cx="170" cy="150" r="146" fill="none" stroke="{acc}" stroke-width="3"/>',
         f'<circle cx="170" cy="150" r="136" fill="none" stroke="{acc}" stroke-width="1.2"/>',
         monogram(m, 0.6, 50, 64)]
    p, w1 = wordmark_block(350, ink, acc); o.append(p)
    return svg(int(370 + w1), 300, ''.join(o))

def b2(m):  # Stacked: monogram on top, words centred below
    c = m == 'color'; ink = PLUM if c else '#000'; acc = LAV if c else '#000'
    W = 900; o = [monogram(m, 1.0, W / 2 - 205, 0)]
    p, w1 = center('GAMBINI LAW', F, 96, W / 2, 400, ink, 7); o.append(p)
    o.append(f'<rect x="{W/2-w1/2:.1f}" y="424" width="{w1:.1f}" height="2" fill="{acc}"/>')
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 32, W / 2, 468, ink, 2.6)[0])
    o.append(center('ESTATE PLANNING · PROBATE · GUARDIANSHIP · ELDER LAW', FS, 24, W / 2, 508, ink, 1.6)[0])
    return svg(W, 550, ''.join(o))

def b3(m):  # Flat plum, swash runs on under the wordmark too
    c = m == 'color'; ink = PLUM if c else '#000'; acc = LAV if c else '#000'
    o = [monogram('color' if c else m, 1.0, 10, 0).replace('url(#metal)', ink)]
    p, w1 = txt('GAMBINI LAW', F, 92, 440, 150, ink, 6); o.append(p)
    o.append(swash(440, 178, 440 + w1 - 30, 178, 5, acc, curl=True))
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 31, 440 + w1 / 2, 226, ink, 2.4)[0])
    o.append(center('ESTATE PLANNING · PROBATE · GUARDIANSHIP · ELDER LAW', FS, 23, 440 + w1 / 2, 262, ink, 1.6)[0])
    return svg(int(470 + w1), 300, ''.join(o))

def c_word(x, base, big, acc, size=150, small=104):
    o = []
    p, gw = txt('G', F, size, x, base, big); o.append(p)
    p, a = txt('AMBINI', F, small, x + gw + 2, base, big, 3); o.append(p)
    lx = x + gw + a + 0.25 * size
    p, lw = txt('L', F, size, lx, base, big); o.append(p)
    p, b = txt('AW', F, small, lx + lw, base, big, 3); o.append(p)
    return ''.join(o), lx + lw + b - x

def c1(m):  # Line-art heart, lighter feel
    c = m == 'color'; ink = PLUM if c else '#000'; acc = LAV if c else '#000'
    o = [heart(130, 150, 230, 'line' if c else m)]
    p, w = c_word(280, 190, ink, acc); o.append(p)
    o.append(swash(320, 208, 280 + w - 30, 208, 6, acc))
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 30, 280 + w / 2, 262, ink, 2.6)[0])
    return svg(int(280 + w + 60), 300, ''.join(o))

def c2(m):  # Stacked: heart on top
    c = m == 'color'; ink = PLUM if c else '#000'; acc = LAV if c else '#000'
    big = 'url(#metal)' if c else '#000'; W = 900
    o = [heart(W / 2, 150, 260, m)]
    _, w = c_word(0, 0, big, acc, 130, 90)
    p, _ = c_word(W / 2 - w / 2, 400, big, acc, 130, 90); o.append(p)
    o.append(swash(W / 2 - w / 2 + 30, 416, W / 2 + w / 2 - 30, 416, 6, acc))
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 30, W / 2, 468, ink, 2.6)[0])
    return svg(W, 510, ''.join(o))

def c3(m):  # Heart tip flows into the swash under the name
    c = m == 'color'; ink = PLUM if c else '#000'; acc = LAV if c else '#000'
    big = 'url(#metal)' if c else '#000'
    o = [heart(130, 140, 230, m)]
    p, w = c_word(280, 190, big, acc); o.append(p)
    end = 280 + w - 30
    d = (f'M128,244 C150,236 200,214 320,210 L{end-40},208 C{end},207 {end+28},196 {end+20},174 '
         f'C{end+16},196 {end-6},214 {end-40},216 L320,218 C210,222 160,238 128,244 Z')
    o.append(f'<path d="{d}" fill="{acc}"/>')
    o.append(center('LET OUR FAMILY PROTECT YOUR FAMILY', FS, 30, 280 + w / 2, 262, ink, 2.6)[0])
    return svg(int(280 + w + 60), 300, ''.join(o))

if __name__ == '__main__':
    for name, fn in [('a1', a1), ('a2', a2), ('a3', a3), ('b1', b1), ('b2', b2), ('b3', b3),
                     ('c1', c1), ('c2', c2), ('c3', c3)]:
        for m in ('color', 'mono'):
            v = fn(m)
            open(f'variations/{name}-{m}.svg', 'w').write(v)
            cairosvg.svg2png(bytestring=v.encode(), write_to=f'variations/{name}-{m}.png', output_width=1200)
    print('ok')
