/* Local-only enhancements. Content and navigation also work without JS. */
(() => {
  'use strict';

  const cards = [...document.querySelectorAll('.project-card')];
  const toolbar = document.getElementById('project-toolbar');
  const filterStatus = document.getElementById('filter-status');
  const filters = [...document.querySelectorAll('[data-filter]')];
  if (toolbar && cards.length) {
    toolbar.hidden = false;
    filters.forEach(button => button.addEventListener('click', () => {
      const category = button.dataset.filter;
      let visibleCount = 0;
      cards.forEach(card => {
        const visible = category === 'all' || card.dataset.category.split(' ').includes(category);
        card.hidden = !visible;
        if (visible) visibleCount += 1;
      });
      filters.forEach(filter => {
        const active = filter === button;
        filter.classList.toggle('active', active);
        filter.setAttribute('aria-pressed', String(active));
      });
      filterStatus.textContent = category === 'all'
        ? '显示全部 ' + visibleCount + ' 个项目'
        : button.textContent.trim() + ' · ' + visibleCount + ' 个项目';
    }));
  }

  const navLinks = [...document.querySelectorAll('.site-nav a')];
  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        navLinks.forEach(link => {
          if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      }
    }, {rootMargin: '-15% 0px -55% 0px', threshold: 0});
    navLinks.forEach(link => {
      const section = document.querySelector(link.hash);
      if (section) sectionObserver.observe(section);
    });
  }

  const year = document.getElementById('copyright-year');
  if (year) year.textContent = String(new Date().getFullYear());

  const canvas = document.getElementById('curiosity-field');
  const motionButton = document.getElementById('motion-toggle');
  if (!canvas || !motionButton) return;
  const context = canvas.getContext('2d');
  if (!context) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reducedMotion.matches;
  let onScreen = true;
  let frame = 0;
  let lastTick = 0;
  let sceneTime = 0;
  let width = 1;
  let height = 1;
  let scale = 1;
  const color = {cyan: [126, 217, 211], amber: [237, 183, 121], pale: [189, 215, 224]};
  const rgba = (rgb, alpha) => 'rgba(' + rgb.join(',') + ',' + alpha + ')';
  const TAU = Math.PI * 2;

  function project(x, y, z, tilt) {
    const ry = y * Math.cos(tilt) - z * Math.sin(tilt);
    const rz = y * Math.sin(tilt) + z * Math.cos(tilt);
    const perspective = 3.8 / (3.8 + rz);
    return [width * .5 + x * scale * perspective, height * .5 + ry * scale * perspective, rz];
  }

  function orbitalPoint(angle, ring, time) {
    const latitude = (ring / 22 - .5) * Math.PI * .91;
    const sway = .08 * Math.sin(angle * 3 + time * .35 + ring * .13);
    const radius = Math.cos(latitude) * (1 + sway);
    const x = radius * Math.cos(angle);
    const y = radius * Math.sin(angle);
    const z = Math.sin(latitude) * .95 + .07 * Math.cos(angle * 2 + time * .22);
    const turn = .32 + time * .045;
    const rx = x * Math.cos(turn) - z * Math.sin(turn);
    const rz = x * Math.sin(turn) + z * Math.cos(turn);
    return project(rx, y, rz, 1.02);
  }

  function line(points, stroke, thickness) {
    if (!points.length) return;
    context.beginPath();
    context.moveTo(points[0][0], points[0][1]);
    for (let index = 1; index < points.length; index += 1) context.lineTo(points[index][0], points[index][1]);
    context.strokeStyle = stroke;
    context.lineWidth = thickness;
    context.stroke();
  }

  function draw(time) {
    context.clearRect(0, 0, width, height);
    const cx = width * .5;
    const cy = height * .5;
    const glow = context.createRadialGradient(cx, cy, 0, cx, cy, scale * 1.6);
    glow.addColorStop(0, 'rgba(70,156,163,.1)');
    glow.addColorStop(.6, 'rgba(70,156,163,.035)');
    glow.addColorStop(1, 'rgba(70,156,163,0)');
    context.fillStyle = glow;
    context.fillRect(0, 0, width, height);

    context.save();
    context.translate(cx, cy);
    context.rotate(-.35);
    context.strokeStyle = 'rgba(141,183,199,.14)';
    context.lineWidth = .7;
    context.setLineDash([2, 7]);
    context.beginPath();
    context.ellipse(0, 0, scale * 1.27, scale * .96, 0, 0, TAU);
    context.stroke();
    context.setLineDash([]);
    context.restore();

    for (let ring = 0; ring <= 22; ring += 1) {
      const points = [];
      for (let step = 0; step <= 130; step += 1) points.push(orbitalPoint(step / 130 * TAU, ring, time));
      const opacity = .14 + .16 * Math.sin(ring / 22 * Math.PI);
      line(points, rgba(color.cyan, opacity), ring % 5 === 0 ? 1 : .65);
    }
    for (let meridian = 0; meridian < 14; meridian += 1) {
      const points = [];
      for (let step = 0; step <= 44; step += 1) points.push(orbitalPoint(meridian / 14 * TAU, step / 2, time));
      line(points, rgba(color.cyan, .08), .65);
    }

    const orbit = [];
    for (let step = 0; step <= 160; step += 1) {
      const angle = step / 160 * TAU;
      orbit.push(project(Math.cos(angle) * 1.28, Math.sin(angle) * .82, Math.sin(angle) * .73, -.45));
    }
    line(orbit, rgba(color.amber, .34), 1);

    for (let index = 0; index < 48; index += 1) {
      const ring = (index * 7.17) % 21 + .5;
      const angle = index * 2.39996 + time * (.035 + (index % 4) * .007);
      const p = orbitalPoint(angle, ring, time);
      const opacity = .25 + (p[2] + 1.4) / 3.5 * .52;
      context.beginPath();
      context.arc(p[0], p[1], index % 9 === 0 ? 2.2 : 1.05, 0, TAU);
      context.fillStyle = rgba(index % 9 === 0 ? color.amber : color.pale, opacity);
      context.fill();
    }

    const angle = time * .12 + .9;
    const traveler = project(Math.cos(angle) * 1.28, Math.sin(angle) * .82, Math.sin(angle) * .73, -.45);
    context.shadowColor = rgba(color.amber, .7);
    context.shadowBlur = 14;
    context.fillStyle = rgba(color.amber, .95);
    context.beginPath();
    context.arc(traveler[0], traveler[1], 3, 0, TAU);
    context.fill();
    context.shadowBlur = 0;

    context.strokeStyle = 'rgba(205,230,230,.47)';
    context.lineWidth = .8;
    context.beginPath();
    context.moveTo(cx - 8, cy);context.lineTo(cx + 8, cy);
    context.moveTo(cx, cy - 8);context.lineTo(cx, cy + 8);
    context.stroke();
    context.fillStyle = 'rgba(140,224,215,.95)';
    context.beginPath();context.arc(cx, cy, 2, 0, TAU);context.fill();
  }

  function resize() {
    const rect = canvas.getBoundingClientRect();
    width = Math.max(1, rect.width);
    height = Math.max(1, rect.height);
    const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    scale = Math.min(width, height) * .33;
    draw(sceneTime);
  }

  function tick(timestamp) {
    frame = 0;
    if (paused || !onScreen || document.hidden) return;
    if (!lastTick) lastTick = timestamp;
    const elapsed = timestamp - lastTick;
    if (elapsed >= 32) {
      sceneTime += Math.min(elapsed, 100) / 1000;
      lastTick = timestamp;
      draw(sceneTime);
    }
    frame = window.requestAnimationFrame(tick);
  }

  function syncPlayback() {
    if (frame) window.cancelAnimationFrame(frame);
    frame = 0;
    lastTick = 0;
    motionButton.setAttribute('aria-pressed', String(paused));
    motionButton.querySelector('.motion-label').textContent = paused ? '播放动效' : '暂停动效';
    motionButton.querySelector('.motion-icon').textContent = paused ? '▷' : 'Ⅱ';
    if (!paused && onScreen && !document.hidden) frame = window.requestAnimationFrame(tick);
  }

  motionButton.hidden = false;
  motionButton.addEventListener('click', () => { paused = !paused;syncPlayback(); });
  reducedMotion.addEventListener('change', event => { paused = event.matches;syncPlayback(); });
  document.addEventListener('visibilitychange', syncPlayback);
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas.parentElement);
  else window.addEventListener('resize', resize, {passive: true});
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      onScreen = entries[0].isIntersecting;
      syncPlayback();
    }, {threshold: 0}).observe(canvas);
  }
  resize();
  canvas.parentElement.classList.add('canvas-ready');
  syncPlayback();
})();
