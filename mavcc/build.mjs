/* Build MAVCC pages.
   node build.mjs
     → dist/*.html    standalone pages (open in a browser to preview)
     → blocks/*.html  paste-into-GHL custom code blocks (no <head>, no <html>)
*/
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'src');
const read = (p) => readFileSync(p, 'utf8');

const header = read(join(src, 'partials', 'header.html'));
const footer = read(join(src, 'partials', 'footer.html'));

const PAGES = {
  home:       { title: "Metro Atlanta Veterans' Chamber of Commerce",            desc: "Atlanta's veteran businesses, connected to the people who can grow them." },
  about:      { title: "About | Metro Atlanta Veterans' Chamber of Commerce",    desc: 'Our mission and the board of directors running the chamber.' },
  events:     { title: "Events | Metro Atlanta Veterans' Chamber of Commerce",   desc: 'Monthly networking socials and fundraising events for Atlanta veterans.' },
  membership: { title: "Membership | Metro Atlanta Veterans' Chamber of Commerce", desc: 'Three membership tiers for veteran-owned businesses, patriot businesses, and corporate sponsors.' },
  programs:   { title: "Programs | Metro Atlanta Veterans' Chamber of Commerce", desc: 'Accelerators, mentorship, contracting help, and bootcamps for members.' },
  resources:  { title: "Resources | Metro Atlanta Veterans' Chamber of Commerce", desc: 'Federal contracting, Match Awards, the member directory, and business tools.' }
};

const CURRENT = ['HOME', 'ABOUT', 'EVENTS', 'MEMBERSHIP', 'PROGRAMS', 'RESOURCES'];

function headerFor(page) {
  let out = header;
  for (const key of CURRENT) {
    out = out.replace(`{{CUR_${key}}}`, key.toLowerCase() === page ? ' aria-current="page"' : '');
  }
  return out;
}

const block = (page, body) =>
  `<!-- MAVCC ${page} — paste into the GHL page's full-width Custom Code element -->\n` +
  `<div class="mavcc">\n${headerFor(page)}\n<main id="main">\n${body}\n</main>\n${footer}\n</div>\n`;

const standalone = (page, meta, body) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${meta.title}</title>
<meta name="description" content="${meta.desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="../mavcc-core.css">
</head>
<body>
<div class="mavcc">
${headerFor(page)}
<main id="main">
${body}
</main>
${footer}
</div>
<script src="../mavcc.js"></script>
</body>
</html>
`;

mkdirSync(join(here, 'dist'), { recursive: true });
mkdirSync(join(here, 'blocks'), { recursive: true });

let n = 0;
for (const [page, meta] of Object.entries(PAGES)) {
  const body = read(join(src, 'bodies', `${page}.html`));
  writeFileSync(join(here, 'dist', `${page}.html`), standalone(page, meta, body), 'utf8');
  writeFileSync(join(here, 'blocks', `${page}.html`), block(page, body), 'utf8');
  n++;
  console.log(`built ${page}`);
}
console.log(`\n${n} pages → dist/ (preview) and blocks/ (GHL paste)`);
