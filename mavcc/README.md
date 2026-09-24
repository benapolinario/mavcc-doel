# MAVCC website rebuild — hand-written HTML for GoHighLevel

A full front-end rebuild of atlvcc.org: six pages, one design system, built to be
pasted into GHL custom-code blocks. All media stays in GHL. All forms stay in GHL.

---

## 1. What's here

```
mavcc-core.css      The design system. Paste once, site-wide.
mavcc.js            Behaviours: drawer, accordion, ticker pause, form modal,
                    newsletter validation, scroll reveal. Paste once, site-wide.
build.mjs           node build.mjs  →  regenerates dist/ and blocks/

src/partials/       header.html, footer.html  (edit these once, rebuild)
src/bodies/         one file per page — the page-specific content
blocks/             ← PASTE THESE INTO GHL (one per page)
dist/               standalone pages for previewing in a browser
```

Preview locally: `npx serve .` then open `http://localhost:4321/dist/home.html`.

---

## 2. Install into GHL (once)

**Step 1 — the CSS.**
Sites → your site → Settings → **Custom CSS**. Paste the entire contents of
`mavcc-core.css`. Everything is scoped under `.mavcc`, so it cannot affect the
GHL builder UI or any page you haven't converted yet.

**Step 2 — the JavaScript.**
Settings → **Tracking Code** → *Footer*. Paste:

```html
<script>
/* paste the full contents of mavcc.js here */
</script>
```

**Step 3 — GHL's form resizer.** Same Footer box, after the script above:

```html
<script src="https://link.msgsndr.com/js/form_embed.js"></script>
```

This makes embedded GHL forms auto-size to their content.

---

## 3. Install each page

For each of home / about / events / membership / programs / resources:

1. Open the page in the GHL builder.
2. Delete the existing sections (or duplicate the page first and work on the copy).
3. Add one **full-width row → Custom Code / HTML** element.
4. Paste the matching file from `blocks/`.
5. Set the row and section padding to **0** so the design controls its own spacing.
6. Save and preview.

Do the homepage last, once you're happy with how one inner page behaves.

---

## 4. Forms — how they're wired

Nothing was rebuilt as a custom form that posts somewhere new. Your GHL forms stay
your GHL forms, so submissions, automations, Turnstile, and Authorize.Net payments
all keep working.

**Confirmed and already wired:**

| Form | ID | Where it appears |
|---|---|---|
| Become a sponsor | `pimlzHX6iVdo4Hup0xV6` | home, membership |
| Alliance partner | `cwq58ndDOGNeyyHoofl1` | membership, programs, about |

These open in an **accessible modal** — focus is trapped, Escape closes, focus
returns to the button that opened it, and the iframe only loads when opened, so it
costs nothing on page load.

```html
<button class="btn btn--primary" type="button"
        data-form-modal="https://events.atlvcc.org/widget/form/YOUR_FORM_ID"
        data-form-title="Heading shown above the form">Button text</button>
```

**Inline embed** (no modal) — use `m-formwrap`:

```html
<div class="m-formwrap">
  <iframe src="https://events.atlvcc.org/widget/form/YOUR_FORM_ID"
          title="Describe the form" style="min-height:520px" loading="lazy"></iframe>
</div>
```

### You must fill these in

- **`FORM_ID_INVITE`** in `src/bodies/events.html` — the "Invite a friend" form.
  Get the id from GHL → Sites → Forms → the form → Integrate. It's the last part
  of the widget URL.
- **Newsletter.** The footer currently uses a native field with real validation
  and accessible errors, posting to `action="#"`. Either point `action` at your
  GHL endpoint, or replace the whole `<form data-news>` block with a GHL form
  iframe as above. It will not collect anything until you do one of these.

### Registration / payments

`/application` and `members.atlvcc.org` were left completely alone — membership
checkout still runs through GHL's payment embed and Authorize.Net.

---

## 5. Images

All media stays in GHL. Images use GHL's own resizing CDN so the browser downloads
the size it actually displays:

```
https://images.leadconnectorhq.com/image/f_webp/q_80/r_WIDTH/u_https://assets.cdn.filesafe.space/CdhybNHWixmjwbzLr3kk/media/MEDIA_ID.png
```

Change `r_WIDTH` (768 / 1200 / 1920) for each `srcset` entry. `CdhybNHWixmjwbzLr3kk`
is your GHL location id.

### You must fill these in

**Board photos** in `src/bodies/about.html` — seven `MEDIA_ID_*` placeholders
(`MEDIA_ID_TROY`, `MEDIA_ID_FORREST`, …). The live site loads these as lazy
background images, so the URLs weren't recoverable. Get each id from GHL → Media.

---

## 6. Content changes you should review

These are editorial decisions, not bugs. Change them if you disagree.

- **Resources page** — the live site ships Lorem Ipsum ("Contrary to popular
  belief, Lorem Ipsum is not simply random text…"). Replaced with a real
  description of the resource centre. **Please check it's accurate.**
- **"Event Sponsor" placeholder cards** on the live homepage were dropped. The
  sponsor logo ticker carries that job now.
- **Sponsor logos have generic `alt="Sponsor"`.** Replace with each company's name.
- **Copyright** updated 2024 → 2026.
- **Headline** is new: "Atlanta's veteran businesses, connected to the people who
  can grow them." The old one was the organisation's name, which the logo already
  says.
- **Golf tournament** links to your existing Givebutter page.

---

## 7. What this fixes from the audit

| Audit finding | Status |
|---|---|
| No focus indicators anywhere (WCAG 2.4.7) | Fixed — `:focus-visible` rings throughout, gold on dark |
| Ticker can't be paused (WCAG 2.2.2, Level A) | Fixed — pause button, pause on hover/focus, stopped under reduced-motion |
| 5 contrast failures incl. Submit at 2.48:1 | Fixed — measured 0 failures; CTA red is now 7.5:1 |
| Newsletter input unlabelled | Fixed — real label, hint, accessible error |
| Menu toggle 19×23px | Fixed — 48×48; measured 0 targets under 44px at 375px and 1280px |
| Zero landmarks, no skip link | Fixed — header/nav/main/footer + skip link on all six pages |
| 12 `<h1>`, no `<h2>` | Fixed — exactly one h1 per page, no level skips |
| No image dimensions (layout shift) | Fixed — width/height on every image |
| Images 2–4× oversized | Fixed — `srcset` via GHL's resizing CDN |
| Below-fold images not lazy | Fixed — `loading="lazy"` + `decoding="async"` |
| Partial reduced-motion support | Fixed — one block covering reveals, ticker, hover, drawer, modal |

**Not fixable from here:** GHL wraps your custom code in its own builder DOM. Its
wrapper divs, its stylesheet, and any stray headings its chrome emits are outside
this code's reach. Expect a real-world audit to land short of a perfect score for
that reason alone — the gap is the platform, not the markup.

---

## 8. Editing later

Change something in `src/`, then:

```
node build.mjs
```

and re-paste the affected file from `blocks/`. Editing a partial updates all six
pages at once.
