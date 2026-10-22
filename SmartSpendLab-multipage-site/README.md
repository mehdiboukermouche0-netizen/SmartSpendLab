# SmartSpendLab – multi-page site

Upload the contents of `site/` to the ROOT of your domain (Cloudflare Pages, Netlify, GitHub Pages, any static host).
Links are root-relative (`/tools/...`), so preview locally with:  `cd site && python3 -m http.server 8000`

## Structure
- `/` homepage (intro, live demo, featured tools and guides)
- `/tools/` tools index + one page per tool (`/tools/<tool>/`)
- `/articles/` articles index (topic filter + search) + one page per article (`/articles/<slug>/`)
- `/about/ /contact/ /privacy-policy/ /terms/ /disclaimer/` and `404.html`
- `sitemap.xml`, `robots.txt`, `ads.txt`, `assets/` (css, js, og-image, logo)

## Before you launch (5 minutes)
1. Open `source/build.py`, set `SITE` to your real domain (and `EMAIL`), then run `python3 build.py` (needs Python 3; Pillow optional for the share image). Re-upload `site/`.
2. Add the site in Google Search Console, submit `https://YOURDOMAIN/sitemap.xml`.
3. AdSense: after approval set `ADSENSE_CLIENT = 'ca-pub-...'` (and optional ad unit ids), rebuild. This adds the AdSense snippet to every page head and writes `ads.txt`.
   For visitors in the EEA/UK/Switzerland, turn on Google's consent message (AdSense > Privacy & messaging) – Google requires a certified consent tool there.
4. Make sure the contact email actually receives mail.
