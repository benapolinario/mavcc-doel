# Gambini Law — logo concepts (round 1)

Based on Olga's notes from the Oct 9 call:
- Keep the heart with the generations inside the G.
- Make the G upright and clean (less "croquet" curl).
- G and L joined by a swash at the bottom = protection / wrapping the family.
- Keep the lavender / plum colors.
- Need a small version (GL or heart) for the favicon.
- No tree concept.

Concepts: A Classic, Straightened (recommended) · B GL Monogram · C Heart First.
Overview: `concepts/concepts.png`. Each has `-color` and `-mono` SVG/PNG.

Fonts: Cinzel (letters) and Cormorant Garamond (tagline), both free (OFL), converted to paths.
Rebuild: put the font TTFs in `../fonts/` next to `concepts/` and run `python3 build.py` (needs fonttools, cairosvg).

## Round 2 — 3 variations each (originals A, B, C kept)
Overview: `concepts/variations/variations.png`. Each has `-color` and `-mono` SVG/PNG.
- A1 Silver metal · A2 Flat two-tone · A3 Full wrap swash
- B1 Ring badge · B2 Stacked · B3 Flat + swash under name
- C1 Line-art heart · C2 Stacked · C3 Heart tip into swash

Rebuild: `GAMBINI_FONTS=<font dir> python3 variations.py && python3 sheet.py`

## Round 3 — new core symbols (heart versions kept)
Overview: `concepts/cores/cores.png`. Each core in A, B, C and A3 layouts, `-color` and `-mono`.
- Guardian Arch — a home doorway sheltering four generations (estate + guardianship)
- Legacy Seal — the wax seal on a signed will (estate planning, probate)
- Family Crest — protection + the Gambini family name

Rebuild: `GAMBINI_FONTS=<font dir> python3 cores.py`
