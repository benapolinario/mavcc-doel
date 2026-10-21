from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
import os
FD=os.environ.get('GAMBINI_FONTS',os.path.join(os.path.dirname(__file__),'..','fonts'))
_c={}
def font(n):
    if n not in _c: _c[n]=TTFont(os.path.join(FD,n))
    return _c[n]
def text_path(s,fontname,size,x,y,tracking=0):
    """baseline at y; returns (d, width)"""
    f=font(fontname); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    sc=size/upm; pen=SVGPathPen(gs); cx=x
    for ch in s:
        g=cmap[ord(ch)]
        tp=TransformPen(pen,(sc,0,0,-sc,cx,y))
        gs[g].draw(tp)
        cx+=gs[g].width*sc+tracking
    return pen.getCommands(), cx-x-tracking
def bounds(ch,fontname):
    f=font(fontname); gs=f.getGlyphSet(); g=f.getBestCmap()[ord(ch)]
    bp=BoundsPen(gs); gs[g].draw(bp); return bp.bounds, gs[g].width, f['head'].unitsPerEm
