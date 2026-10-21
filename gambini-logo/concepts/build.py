import glyphs, cairosvg, sys
F='Cinzel-500.ttf'; FB='Cinzel-600.ttf'; FS='Cormorant-600.ttf'
PLUM='#4A3558'; LAV='#8E78A8'; LILAC='#C9BEDA'
HEART='M50,90 C22,70 0,52 0,28 C0,11 12,0 27,0 C38,0 46,6 50,15 C54,6 62,0 73,0 C88,0 100,11 100,28 C100,52 78,70 50,90 Z'
DEFS='''<defs>
<linearGradient id="glow" x1="0" y1="1" x2="0" y2="0">
 <stop offset="0" stop-color="#FFE7C2"/><stop offset=".45" stop-color="#F3CFE0"/><stop offset="1" stop-color="#B9A4D6"/></linearGradient>
<radialGradient id="sun" cx=".5" cy=".72" r=".45"><stop offset="0" stop-color="#FFF6E6"/><stop offset="1" stop-color="#FFF6E6" stop-opacity="0"/></radialGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#A895C2"/><stop offset=".5" stop-color="#6E5A88"/><stop offset="1" stop-color="#4A3558"/></linearGradient>
<linearGradient id="silver" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#D9D0E6"/><stop offset=".35" stop-color="#9A88B4"/><stop offset=".55" stop-color="#E4DCEE"/><stop offset="1" stop-color="#5E4A78"/></linearGradient>
</defs>'''
def family(ink):
    # four generations in heart units (0..100 x 0..90), ground at y=62
    s=f'stroke="{ink}" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    return f'''<g fill="{ink}">
 <circle cx="27" cy="33" r="3.6"/><circle cx="42" cy="25.5" r="4"/><circle cx="56.5" cy="40" r="3.1"/><circle cx="70" cy="37" r="3.5"/></g>
<g {s}>
 <path d="M27,39 L27,50 M25.4,50 L25,62 M28.6,50 L29.4,62" stroke-width="4.6"/>
 <path d="M21.5,47 L20,62" stroke-width="1.6"/>
 <path d="M42,31.5 L42,46 M40.2,46 L39.6,62 M43.8,46 L44.6,62" stroke-width="5.2"/>
 <path d="M56.5,45 L56.5,52 M55.3,52 L55,62 M57.7,52 L58,62" stroke-width="3.6"/>
 <path d="M69.6,42 L69.6,50 L76,50 L76,58" stroke-width="5"/>
 <circle cx="70" cy="56" r="5.8" stroke-width="1.7"/>
 <path d="M30,44 L39,41 M45,41 L54.5,47 M58.5,47 L65.5,45.5" stroke-width="1.8"/>
 <path d="M14,62.5 L86,62.5" stroke-width="1.4"/>
</g>'''
# The core symbol. Defaults to the heart; cores.py swaps in other shapes.
CORE={'shape':HEART,'fam':'','extra':lambda ink:'','fam_out':False}
def heart(cx,cy,w,mode='color'):
    k=w/100; x=cx-50*k; y=cy-45*k; S=CORE['shape']
    def fam(ink):
        if CORE['fam'] is None: return ''
        if CORE.get('fam_out'): ink='#000' if mode=='mono' else PLUM  # family stands outside the shape
        return f'<g transform="{CORE["fam"]}">{family(ink)}</g>'
    if mode=='color':
        body=f'<path d="{S}" fill="url(#glow)"/><path d="{S}" fill="url(#sun)"/>'+fam(PLUM)+CORE['extra'](PLUM)+f'<path d="{S}" fill="none" stroke="{PLUM}" stroke-width="2.2"/>'
    elif mode=='line':
        body=f'<path d="{S}" fill="#fff" stroke="{PLUM}" stroke-width="3.4"/>'+fam(PLUM)+CORE['extra'](PLUM)
    elif mode=='solid':
        body=f'<path d="{S}" fill="{PLUM}"/>'+fam('#fff')+CORE['extra']('#fff')
    elif mode=='mono':
        body=f'<path d="{S}" fill="#000"/>'+fam('#fff')+CORE['extra']('#fff')
    else: # tiny: shape only
        body=f'<path d="{S}" fill="{mode}"/>'
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})">{body}</g>'
def txt(s,font,size,x,y,fill,tr=0):
    d,w=glyphs.text_path(s,font,size,x,y,tr); return f'<path d="{d}" fill="{fill}"/>',w
def swash(x0,y0,x1,y1,t,fill,curl=True):
    # tapered horizontal ribbon, thickest near x0, ending in upward curl
    mx=(x0+x1)/2
    d=f'M{x0},{y0} C{x0+60},{y0+t*1.2} {mx},{y0+t} {x1-40},{y1+t*.5} '
    if curl:
        d+=f'C{x1},{y1+t*.3} {x1+28},{y1-10} {x1+20},{y1-34} C{x1+16},{y1-12} {x1-6},{y1-1} {x1-40},{y1} '
    else:
        d+=f'L{x1},{y1} '
    d+=f'C{mx},{y0} {x0+60},{y0} {x0},{y0} Z'
    return f'<path d="{d}" fill="{fill}"/>'
def svg(w,h,body,bg='#fff'):
    b=f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{DEFS}{b}{body}</svg>'

def concept_a(mode):
    ink = PLUM if mode=='color' else '#000'; big = 'url(#metal)' if mode=='color' else '#000'
    acc = LAV if mode=='color' else '#000'
    o=[]
    p,gw=txt('G',F,330,20,272,big); o.append(p)
    o.append(heart(20+0.330*420,272-0.330*352,128,mode))
    p,aw=txt('AMBINI',F,118,272,178,big,4); o.append(p)
    lx=272+aw+14
    p,lw=txt('L',F,330,lx,272,big); o.append(p)
    p,_=txt('AW',F,118,lx+0.33*420,178,big,4); o.append(p)
    # tagline between G and L, with rules
    p,tw=txt('LET OUR FAMILY',FS,34,0,0,ink,3); tx=272+(aw-tw)/2
    p,_=txt('LET OUR FAMILY',FS,34,tx,222,ink,3); o.append(p)
    p,tw2=txt('PROTECT YOUR FAMILY',FS,34,0,0,ink,3); o.append(txt('PROTECT YOUR FAMILY',FS,34,272+(aw-tw2)/2,262,ink,3)[0])
    # swash: from G foot, under tagline, into L foot, out to a curl
    o.append(swash(120,270,lx+350,270,10,acc))
    w=int(lx+420)
    # services line
    p,sw=txt('ESTATE PLANNING  ·  PROBATE  ·  GUARDIANSHIP  ·  ELDER LAW',FS,30,0,0,ink,2)
    o.append(txt('ESTATE PLANNING  ·  PROBATE  ·  GUARDIANSHIP  ·  ELDER LAW',FS,30,(w-sw)/2,345,ink,2)[0])
    return svg(w,380,''.join(o))

def monogram(mode, s=1.0, ox=0, oy=0):
    ink = 'url(#metal)' if mode=='color' else '#000'; acc = LAV if mode=='color' else '#000'
    o=[]
    p,_=txt('G',F,300*s,ox+18*s,oy+238*s,ink); o.append(p)
    o.append(heart(ox+(18+0.3*420)*s,oy+(238-0.3*352)*s,112*s,mode))
    lx=ox+232*s
    p,_=txt('L',F,300*s,lx,oy+238*s,ink); o.append(p)
    e=lx+0.3*557*s; x0=ox+40*s
    d=(f'M{e:.1f},{oy+238*s:.1f} C{e-60*s:.1f},{oy+266*s:.1f} {ox+90*s:.1f},{oy+272*s:.1f} {x0:.1f},{oy+240*s:.1f} '
       f'C{ox+16*s:.1f},{oy+224*s:.1f} {ox+8*s:.1f},{oy+190*s:.1f} {ox+16*s:.1f},{oy+166*s:.1f} '
       f'C{ox+20*s:.1f},{oy+200*s:.1f} {ox+40*s:.1f},{oy+230*s:.1f} {ox+80*s:.1f},{oy+248*s:.1f} '
       f'C{ox+150*s:.1f},{oy+262*s:.1f} {e-80*s:.1f},{oy+256*s:.1f} {e:.1f},{oy+238*s:.1f} Z')
    o.append(f'<path d="{d}" fill="{acc}"/>')
    return ''.join(o)

def concept_b(mode):
    ink = PLUM if mode=='color' else '#000'
    o=[monogram(mode,1.0,10,0)]
    p,w1=txt('GAMBINI LAW',F,92,440,150,ink,6); o.append(p)
    p,w2=txt('LET OUR FAMILY PROTECT YOUR FAMILY',FS,31,0,0,ink,2.4)
    o.append(f'<rect x="442" y="172" width="{w1-4}" height="2" fill="{LAV if mode=="color" else "#000"}"/>')
    o.append(txt('LET OUR FAMILY PROTECT YOUR FAMILY',FS,31,440+(w1-w2)/2,214,ink,2.4)[0])
    p,w3=txt('ESTATE PLANNING · PROBATE · GUARDIANSHIP · ELDER LAW',FS,23,0,0,ink,1.6)
    o.append(txt('ESTATE PLANNING · PROBATE · GUARDIANSHIP · ELDER LAW',FS,23,440+(w1-w3)/2,252,ink,1.6)[0])
    return svg(int(460+w1),300,''.join(o))

def concept_c(mode):
    ink = PLUM if mode=='color' else '#000'; acc = LAV if mode=='color' else '#000'
    big='url(#metal)' if mode=='color' else '#000'
    o=[heart(130,150,230,mode)]
    x=280
    p,gw=txt('G',F,150,x,190,big); o.append(p)
    p,a=txt('AMBINI',F,104,x+gw+2,190,big,3); o.append(p)
    lx=x+gw+a+38
    p,lw=txt('L',F,150,lx,190,big); o.append(p)
    p,b=txt('AW',F,104,lx+lw,190,big,3); o.append(p)
    end=lx+lw+b
    o.append(swash(x+40,208,end-30,208,6,acc))
    p,w2=txt('LET OUR FAMILY PROTECT YOUR FAMILY',FS,30,0,0,ink,2.6)
    o.append(txt('LET OUR FAMILY PROTECT YOUR FAMILY',FS,30,x+(end-x-w2)/2,262,ink,2.6)[0])
    return svg(int(end+60),300,''.join(o))

def symbols(mode):
    a=svg(256,256,heart(128,124,220,mode),bg=None)
    b=svg(256,256,monogram(mode,0.6,10,42),bg=None)
    return a,b

def main():
  out={}
  for m in ('color','mono'):
    out[f'a-lockup-{m}']=concept_a(m); out[f'b-lockup-{m}']=concept_b(m); out[f'c-lockup-{m}']=concept_c(m)
    h,g=symbols(m); out[f'heart-symbol-{m}']=h; out[f'gl-symbol-{m}']=g
  for k,v in out.items():
    open(f'{k}.svg','w').write(v)
    cairosvg.svg2png(bytestring=v.encode(),write_to=f'{k}.png',output_width=1400 if 'lockup' in k else 512)
def g_symbol(mode):
    big='url(#metal)' if mode=='color' else '#000'
    s=0.31; p,_=txt('G',F,1000*s,128-0.5*(55+789)*s,128+0.5*(714-14)*s,big)
    return svg(256,256,p+heart(128-0.5*(55+789)*s+420*s,128+0.5*700*s-352*s,124,mode),bg=None)

if __name__=='__main__':
    main()
    for m in ('color','mono'):
        v=g_symbol(m); open(f'g-symbol-{m}.svg','w').write(v)
        cairosvg.svg2png(bytestring=v.encode(),write_to=f'g-symbol-{m}.png',output_width=512)
    print('ok')
