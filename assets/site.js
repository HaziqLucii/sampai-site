(() => {
  if (!window.gsap || !window.ScrollTrigger) return;
  // SplitText measures lines, so wait for the real fonts or the breaks are wrong.
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(init);

  function init() {
  gsap.registerPlugin(ScrollTrigger, window.SplitText);

  const pad = (n) => String(n).padStart(2, '0');
  const mm = gsap.matchMedia();

  // Everything below starts from the finished layout and animates *from* a
  // hidden state, so with reduced motion or a failed script the page is static
  // and complete.
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    const lenis = new Lenis({ lerp: 0.09 });
    lenis.on('scroll', ScrollTrigger.update);
    const raf = (t) => lenis.raf(t * 1000);
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);
    document.querySelectorAll('a[href^="#"]').forEach((a) =>
      a.addEventListener('click', (e) => {
        const target = document.querySelector(a.getAttribute('href'));
        if (target) { e.preventDefault(); lenis.scrollTo(target, { offset: -20 }); }
      }));

    gsap.to('.progress span', { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: true } });

    // Hero: the wordmark rises letter by letter, then the rest settles in.
    const word = new SplitText('.wordmark', { type: 'chars', mask: 'chars' });
    const intro = gsap.timeline({ defaults: { ease: 'expo.out' } });
    intro
      .from('.top', { y: -20, opacity: 0, duration: 0.8 })
      .from('.line', { scaleX: 0, transformOrigin: 'left', duration: 1.2 }, '<')
      .from(word.chars, { yPercent: 110, duration: 1.3, stagger: 0.06 }, '-=0.9')
      .from('.intro', { y: 26, opacity: 0, duration: 1, stagger: 0.1 }, '-=0.9')
      .from('.hero-plate', { clipPath: 'inset(100% 0 0 0)', y: 60, duration: 1.4 }, '-=1.1')
      .from('.watermark', { opacity: 0, scale: 0.9, duration: 1.6 }, '-=1.2');

    // The hero plate "rings": a small shake and the alert count ticks up.
    let alerts = 1;
    const ring = gsap.timeline({ repeat: -1, repeatDelay: 2.4, delay: 3 });
    ring
      .to('.ringer', { keyframes: { x: [0, -5, 5, -4, 4, -2, 0], rotation: [0, -0.6, 0.6, -0.4, 0.4, 0, 0] }, duration: 0.55, ease: 'none' })
      .call(() => {
        alerts = alerts >= 99 ? 1 : alerts + 1;
        document.querySelector('.ticker').textContent = pad(alerts);
      }, null, 0.1);

    gsap.to('.watermark', { yPercent: 40, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

    // Marquee: a slow loop that speeds up with scroll velocity.
    const track = document.querySelector('.marquee-track');
    const loop = gsap.to(track, { xPercent: -50, ease: 'none', duration: 28, repeat: -1 });
    ScrollTrigger.create({
      onUpdate: (self) => {
        const boost = 1 + Math.min(Math.abs(self.getVelocity()) / 300, 6);
        gsap.to(loop, { timeScale: boost * (self.direction < 0 ? -1 : 1), duration: 0.2, overwrite: true });
        gsap.to(loop, { timeScale: 1, duration: 1.2, delay: 0.25 });
      },
    });

    // The nag: pinned while scrolling counts the alerts up, ten minutes apart,
    // until Done lands.
    const MAX = 12;
    const num = document.querySelector('.nag .num');
    const n2 = document.querySelector('.nag .n2');
    const clock = document.querySelector('.nag .clock');
    let shown = 1;
    const setAlert = (n) => {
      if (n === shown) return;
      shown = n;
      num.textContent = n;
      n2.textContent = pad(n);
      const mins = 12 * 60 + 20 + (n - 1) * 10;
      clock.textContent = `${pad(Math.floor(mins / 60) % 24)}:${pad(mins % 60)}`;
      gsap.fromTo(num, { x: -8, rotation: -1.2 }, { x: 0, rotation: 0, duration: 0.45, ease: 'elastic.out(1, 0.35)' });
    };
    const nagTl = gsap.timeline({
      scrollTrigger: {
        trigger: '.nag', start: 'top top', end: '+=260%', pin: true, scrub: 0.6,
        onUpdate: (self) => setAlert(Math.min(MAX, 1 + Math.floor(Math.min(self.progress / 0.82, 1) * (MAX - 1)))),
      },
    });
    nagTl
      .to('.nag-bar span', { scaleX: 1, ease: 'none', duration: 0.82 }, 0)
      .to('.nag .numeral', { opacity: 0.18, duration: 0.1 }, 0.84)
      .fromTo('.done-stamp', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.1 }, 0.86)
      .to({}, { duration: 0.04 });

    const chips = gsap.utils.toArray('.nag .chip');
    ScrollTrigger.create({
      trigger: '.nag', start: 'top 70%',
      onEnter: () => gsap.from(chips, { y: 18, opacity: 0, stagger: 0.06, duration: 0.6, ease: 'back.out(2)' }),
      once: true,
    });

    // Headings rise line by line as they enter.
    gsap.utils.toArray('.split').forEach((el) => {
      const s = new SplitText(el, { type: 'lines', mask: 'lines' });
      gsap.from(s.lines, { yPercent: 105, duration: 1.1, stagger: 0.08, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 85%' } });
    });

    gsap.utils.toArray('.reveal').forEach((el) =>
      gsap.from(el, { y: 34, opacity: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 88%' } }));

    gsap.utils.toArray('.stagger').forEach((el) =>
      gsap.from(el.children, { y: 24, opacity: 0, duration: 0.8, stagger: 0.07, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 85%' } }));

    // Section rules draw in from the left.
    gsap.utils.toArray('.section, .gallery, .outro').forEach((el) =>
      gsap.fromTo(el, { '--rule': 0 }, { '--rule': 1, scrollTrigger: { trigger: el, start: 'top 90%' } }));

    gsap.utils.toArray('.parallax').forEach((el) =>
      gsap.fromTo(el, { y: 0 }, { y: Number(el.dataset.speed || 0), ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } }));

    gsap.utils.toArray('.countdown').forEach((el) => {
      const state = { v: Number(el.dataset.from) };
      gsap.to(state, {
        v: 0, duration: 1.8, ease: 'power3.inOut',
        onUpdate: () => { el.textContent = Math.round(state.v); },
        scrollTrigger: { trigger: el, start: 'top 85%' },
      });
    });

    const outro = new SplitText('.outro-word', { type: 'chars', mask: 'chars' });
    gsap.from(outro.chars, { yPercent: 110, duration: 1.2, stagger: 0.035, ease: 'expo.out', scrollTrigger: { trigger: '.outro', start: 'top 70%' } });

    return () => { gsap.ticker.remove(raf); lenis.destroy(); };
  });

  // The widget gallery scrolls sideways while pinned, on wide screens only.
  mm.add('(prefers-reduced-motion: no-preference) and (min-width: 821px)', () => {
    const track = document.querySelector('.gallery-track');
    const distance = () => Math.max(0, track.scrollWidth - window.innerWidth + 80);
    gsap.to(track, {
      x: () => -distance(), ease: 'none',
      scrollTrigger: { trigger: '.gallery', start: 'top top', end: () => `+=${distance()}`, pin: '.gallery-pin', scrub: 0.6, invalidateOnRefresh: true },
    });
    gsap.from('.w-card', { y: 80, opacity: 0, rotation: 2, stagger: 0.1, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.gallery', start: 'top 70%' } });
  });

  mm.add('(prefers-reduced-motion: no-preference) and (max-width: 820px)', () => {
    gsap.utils.toArray('.w-card').forEach((el) =>
      gsap.from(el, { y: 50, opacity: 0, duration: 0.9, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 90%' } }));
  });

  window.addEventListener('load', () => ScrollTrigger.refresh());
  }
})();
