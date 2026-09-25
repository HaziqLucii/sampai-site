# sampai-site

**Live site:** https://haziqlucii.github.io/sampai-site/ (Malay: [/ms/](https://haziqlucii.github.io/sampai-site/ms/), Indonesian: [/id/](https://haziqlucii.github.io/sampai-site/id/))

The website for **Sampai**, a nag-until-done reminder app for Android: a reminder that rings again every 1, 5, 10, 15, 30 or 60 minutes until you tap Done.

- `/` landing page (English), `/ms/` Malay, `/id/` Indonesian
- `/privacy/` privacy policy (linked from the Play listing)
- `/terms/` terms of use

The landing page is ported from the Claude Design file `design/Sampai Landing.dc.html` in the app repo, with real app screenshots in place of the design mockups and "coming soon" in place of the Play links until launch. Static HTML, served by GitHub Pages. Scroll animations use GSAP with ScrollTrigger, and Lenis for smooth scrolling, vendored under `assets/vendor/`; `assets/landing.js` holds the timelines. Motion is off for visitors who ask their system to reduce it.

The first, self-designed version of the site is kept on the `v1-own-design` branch.

Contact: sampai.app.support@gmail.com

## Languages

`ms/index.html` and `id/index.html` are generated from `index.html` by `python3 tools/i18n.py`. Edit the English page, add any new line to the table in `tools/i18n.py` (the script stops on untranslated text), then rerun. Malay and Indonesian are written separately, not converted from each other.
