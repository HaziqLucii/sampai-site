# sampai-site

The website for **Sampai**, a nag-until-done reminder app for Android: a reminder that rings again every 1, 5, 10, 15, 30 or 60 minutes until you tap Done.

- `/` landing page
- `/privacy/` privacy policy (linked from the Play listing)
- `/terms/` terms of use

The landing page is ported from the Claude Design file `design/Sampai Landing.dc.html` in the app repo, with real app screenshots in place of the design mockups and "coming soon" in place of the Play links until launch. Static HTML, served by GitHub Pages. Scroll animations use GSAP with ScrollTrigger, and Lenis for smooth scrolling, vendored under `assets/vendor/`; `assets/landing.js` holds the timelines. Motion is off for visitors who ask their system to reduce it.

The first, self-designed version of the site is kept on the `v1-own-design` branch.

Contact: sampai.app.support@gmail.com
