/* Build MAVCC pages.
   node build.mjs
     → public/*.html  self-contained static site (local preview AND Cloudflare Pages)
     → blocks/*.html  paste-into-GHL custom code blocks (no <head>, no <html>)
*/
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'src');
const read = (p) => readFileSync(p, 'utf8');

const header = read(join(src, 'partials', 'header.html'));
const footer = read(join(src, 'partials', 'footer.html'));

const PAGES = {
  home:       { title: "Metro Atlanta Veterans' Chamber of Commerce",              desc: "Atlanta's veteran businesses, connected to the people who can grow them." },
  about:      { title: "About | Metro Atlanta Veterans' Chamber of Commerce",      desc: 'Our mission and the board of directors running the chamber.' },
  events:     { title: "Events | Metro Atlanta Veterans' Chamber of Commerce",     desc: 'Monthly networking socials and fundraising events for Atlanta veterans.' },
  membership: { title: "Membership | Metro Atlanta Veterans' Chamber of Commerce", desc: 'Three membership tiers for veteran-owned businesses, patriot businesses, and corporate sponsors.' },
  programs:   { title: "Programs | Metro Atlanta Veterans' Chamber of Commerce",   desc: 'Accelerators, mentorship, contracting help, and bootcamps for members.' },
  resources:  { title: "Resources | Metro Atlanta Veterans' Chamber of Commerce",  desc: 'Federal contracting, Match Awards, the member directory, and business tools.' }
};

const CURRENT = ['HOME', 'ABOUT', 'EVENTS', 'MEMBERSHIP', 'PROGRAMS', 'RESOURCES'];

function headerFor(page, linkExt) {
  let out = header;
  for (const key of CURRENT) {
    out = out.replace(`{{CUR_${key}}}`, key.toLowerCase() === page ? ' aria-current="page"' : '');
  }
  // In the static preview, nav links need a file extension; in GHL they are clean routes.
  if (linkExt) {
    for (const key of CURRENT) {
      const slug = key.toLowerCase();
      out = out.split(`href="/${slug}"`).join(`href="./${slug}.html"`);
    }
  }
  return out;
}

function footerFor(linkExt) {
  let out = footer;
  if (linkExt) {
    for (const key of CURRENT) {
      const slug = key.toLowerCase();
      out = out.split(`href="/${slug}"`).join(`href="./${slug}.html"`);
    }
  }
  return out;
}

const block = (page, body) =>
  `<!-- MAVCC ${page} — paste into the GHL page's full-width Custom Code element -->\n` +
  `<div class="mavcc">\n${headerFor(page, false)}\n<main id="main">\n${body}\n</main>\n${footerFor(false)}\n</div>\n`;

const standalone = (page, meta, body) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${meta.title}</title>
<meta name="description" content="${meta.desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="./mavcc-core.css">
</head>
<body>
<div class="mavcc">
${headerFor(page, true)}
<main id="main">
${body}
</main>
${footerFor(true)}
</div>
<script src="./mavcc.js"></script>
</body>
</html>
`;

const outPublic = join(here, 'public');
const outBlocks = join(here, 'blocks');
mkdirSync(outPublic, { recursive: true });
mkdirSync(outBlocks, { recursive: true });

for (const [page, meta] of Object.entries(PAGES)) {
  const body = read(join(src, 'bodies', `${page}.html`));
  writeFileSync(join(outPublic, `${page}.html`), standalone(page, meta, body), 'utf8');
  writeFileSync(join(outBlocks, `${page}.html`), block(page, body), 'utf8');
  console.log(`built ${page}`);
}

// Assets live beside the pages so the folder is a valid site root.
copyFileSync(join(here, 'mavcc-core.css'), join(outPublic, 'mavcc-core.css'));
copyFileSync(join(here, 'mavcc.js'), join(outPublic, 'mavcc.js'));

// index.html so the bare domain lands on the homepage.
copyFileSync(join(outPublic, 'home.html'), join(outPublic, 'index.html'));

// Keep a client preview out of search results.
writeFileSync(join(outPublic, 'robots.txt'), 'User-agent: *\nDisallow: /\n', 'utf8');

console.log(`\n${Object.keys(PAGES).length} pages → public/ (deployable site) and blocks/ (GHL paste)`);
