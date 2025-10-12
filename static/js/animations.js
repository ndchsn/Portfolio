(() => {
  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];
  let raf = null;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function resize() {
    // ensure CSS sizes are applied
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(300, Math.floor(rect.width));
    canvas.height = Math.max(120, Math.floor(rect.height));
  }

  function initParticles() {
    particles = [];
    // fewer, larger, softer particles for cloud-like feeling
    const area = canvas.width * canvas.height;
    const count = Math.max(6, Math.floor(area / 160000));
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height * 0.75,
        r: 24 + Math.random() * 60,
        vx: -0.05 + Math.random() * 0.12,
        vy: -0.02 + Math.random() * 0.04,
        alpha: 0.03 + Math.random() * 0.06
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      // wrap gently
      if (p.x < -p.r) p.x = canvas.width + p.r;
      if (p.x > canvas.width + p.r) p.x = -p.r;
      if (p.y < -p.r) p.y = canvas.height + p.r;
      if (p.y > canvas.height + p.r) p.y = -p.r;

      // radial soft gradient
      const g = ctx.createRadialGradient(p.x, p.y, p.r * 0.2, p.x, p.y, p.r);
      // subtle bluish-white center
      g.addColorStop(0, `rgba(200,230,255,${p.alpha})`);
      g.addColorStop(0.6, `rgba(120,170,200,${p.alpha * 0.8})`);
      g.addColorStop(1, 'rgba(10,18,26,0)');
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  function loop() {
    draw();
    raf = requestAnimationFrame(loop);
  }

  function start() {
    if (prefersReduced) return; // respect OS setting
    if (!raf) {
      raf = requestAnimationFrame(loop);
    }
  }

  function stop() {
    if (raf) {
      cancelAnimationFrame(raf);
      raf = null;
    }
    // clear canvas when stopping
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  function onResize() {
    resize();
    initParticles();
  }

  // Toggle control from UI
  const toggle = document.getElementById('toggle-anim');
  const ANIM_KEY = 'portfolio_animations_off';
  function setToggleState(off) {
    if (!toggle) return;
    toggle.setAttribute('aria-pressed', String(!!off));
    toggle.textContent = off ? 'Turn on animations' : 'Turn off animations';
  }

  function loadState() {
    try {
      return localStorage.getItem(ANIM_KEY) === '1';
    } catch (e) {
      return false;
    }
  }

  function saveState(off) {
    try { localStorage.setItem(ANIM_KEY, off ? '1' : '0'); } catch (e) {}
  }

  if (toggle) {
    const isOff = loadState();
    setToggleState(isOff);
    if (!isOff) start();
    toggle.addEventListener('click', () => {
      const currentlyOff = loadState();
      const nextOff = !currentlyOff;
      saveState(nextOff);
      setToggleState(nextOff);
      if (nextOff) stop(); else start();
    });
  } else {
    if (!prefersReduced) start();
  }

  window.addEventListener('resize', onResize, { passive: true });
  // init
  setTimeout(() => {
    onResize();
    // apply initial state
    if (loadState()) stop();
    else start();
  }, 100);
})();
