// Deterministic film engine: every frame is a pure function of time. window.seek(T) draws time T (seconds).
const FPS = 30, W = 1920, H = 1080;
const $ = (tag, cls, parent, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; };
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const ease = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const easeOut = t => 1 - Math.pow(1 - clamp(t), 3);
const easeIn = t => Math.pow(clamp(t), 3);
const back = t => { t = clamp(t); const c = 1.70158; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
const ramp = (t, a, b) => clamp((t - a) / (b - a));           // 0..1 between a and b
const pulse = (t, a, b, fade = .25) => Math.min(ramp(t, a, a + fade), 1 - ramp(t, b - fade, b));
const rnd = seed => { let s = seed % 2147483647; if (s <= 0) s += 2147483646; return () => (s = s * 16807 % 2147483647) / 2147483647; };
const lerpCam = (a, b, t) => ({ x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t), z: lerp(a.z, b.z, t), yaw: lerp(a.yaw, b.yaw, t), pitch: lerp(a.pitch, b.pitch, t), fov: lerp(a.fov ?? 70, b.fov ?? 70, t) });

const Film = {
  shots: [], cues: [], total: 0, cur: null, timeline: null, images: new Map(),
  add(def) { this.shots.push(def); return def; },
  // line timing from the voice timeline: Film.line('s1.3') -> {t0,t1} relative to its shot
  line(id) { return (this.timeline && this.timeline.lines[id]) || { t0: 0, t1: 0, missing: true }; },
  layout() {
    let t = 0;
    for (const s of this.shots) {
      const tl = this.timeline && this.timeline.shots[s.id];
      s.dur = (tl && tl.dur) || s.dur || 3; s.t0 = t; t += s.dur;
      for (const c of (s.sfx || [])) this.cues.push({ t: s.t0 + c.at, f: c.f, gain: c.gain ?? 1, shot: s.id });
      if (s.music) this.cues.push({ t: s.t0 + (s.music.at || 0), music: s.music.f, gain: s.music.gain ?? 1, fade: s.music.fade ?? .5, until: s.music.until, shot: s.id });
    }
    this.total = t;
  },
  img(src) {
    if (this.images.has(src)) return this.images.get(src);
    const p = new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = () => rej(new Error('missing ' + src)); i.src = src; });
    this.images.set(src, p); return p;
  },
};

const stage = {};
function initStage() {
  const root = document.getElementById('stage');
  stage.root = root;
  stage.view = $('div', 'view', root);            // plate + 3D, gets grade + 2D camera moves
  stage.plate = $('canvas', 'plate', stage.view); stage.plate.width = W; stage.plate.height = H;
  stage.s3 = $('div', 'scene3d', stage.view);
  stage.w3 = $('div', 'world3d', stage.s3);
  stage.chars = $('div', 'layer', stage.view);    // per-character 3D layers + mattes (shots with depth)
  stage.tags = $('div', 'layer', stage.view);     // nametags, world-anchored labels
  stage.ui = $('div', 'layer', root);             // HUD, cards, chat
  stage.fx = $('div', 'layer fx', root);          // flashes/fades
}

async function drawPlate(s, t) {
  const g = stage.plate.getContext('2d');
  const p = typeof s.plate === 'function' ? s.plate(t) : s.plate;
  if (!p) { g.fillStyle = s.bg || '#000'; g.fillRect(0, 0, W, H); return; }
  let src;
  if (p.seq) { const n = Math.min(p.n - 1, Math.max(0, Math.round((t - (p.at || 0)) * (p.fps || FPS)))); src = `${p.seq}${String(n).padStart(4, '0')}.jpg`; }
  else src = p.still;
  const im = await Film.img(src);
  g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
  g.drawImage(im, 0, 0, W, H);
  if (p.over && p.wipe != null) {   // reveal `over` from the left with a bright edge
    const im2 = await Film.img(p.over), x = Math.round(clamp(p.wipe) * W);
    if (x > 0) { g.drawImage(im2, 0, 0, im2.width * x / W, im2.height, 0, 0, x, H); g.fillStyle = 'rgba(255,255,255,.9)'; if (x < W) g.fillRect(x - 5, 0, 10, H); }
  } else if (p.over) { const im2 = await Film.img(p.over); g.globalAlpha = clamp(p.mix); g.drawImage(im2, 0, 0, W, H); g.globalAlpha = 1; }
}

window.seek = async function (T) {
  T = Math.max(0, Math.min(Film.total - 1e-6, T));
  let s = Film.shots.find(x => T >= x.t0 && T < x.t0 + x.dur) || Film.shots[Film.shots.length - 1];
  const t = T - s.t0;
  if (Film.cur !== s) {
    stage.w3.innerHTML = ''; stage.chars.innerHTML = ''; stage.tags.innerHTML = ''; stage.ui.innerHTML = ''; stage.fx.innerHTML = '';
    stage.view.style.cssText = ''; stage.root.dataset.shot = s.id;
    s.ctx = { s, chars: {}, el: {} };
    if (s.build) s.build(s.ctx);
    Film.cur = s;
  }
  const cam = typeof s.cam === 'function' ? s.cam(t) : s.cam;
  s.ctx.cam = cam;
  if (cam) { stage.s3.style.perspective = MC.focal(cam, W) + 'px'; stage.w3.style.transform = MC.worldMatrix(cam, W); stage.s3.style.display = ''; }
  else stage.s3.style.display = 'none';
  await drawPlate(s, t);
  stage.view.style.filter = (typeof s.grade === 'function' ? s.grade(t) : s.grade) || '';
  if (s.update) s.update(s.ctx, t, T);
  if (cam && Object.values(s.ctx.chars).some(c => c.scene)) await occlude(s, cam, t);
  return { shot: s.id, t };
};

// ---- helpers used by shots -----------------------------------------------------------------------
function addChar(ctx, name, skin) {
  const c = MC.character(skin); ctx.chars[name] = c;
  if (ctx.s.depth) {   // own 3D layer + matte canvas, so the plate can stand in front of this character
    c.scene = $('div', 'scene3d', stage.chars); c.world = $('div', 'world3d', c.scene); c.world.appendChild(c.el);
    c.matte = $('canvas', 'matte', stage.chars); c.matte.width = W; c.matte.height = H;
  } else stage.w3.appendChild(c.el);
  const pose = c.pose; c.pose = p => { c.last = p; pose(p); };
  return c;
}
function depthOf(name) {
  const d = window.DEPTH && window.DEPTH[name]; if (!d) throw new Error('no depth for ' + name);
  if (!d.data) { const bin = atob(d.b64); const u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); d.data = new Uint16Array(u.buffer); d.small = document.createElement('canvas'); }
  return d;
}
async function occlude(s, cam, t) {
  const p = typeof s.plate === 'function' ? s.plate(t) : s.plate, name = typeof s.depth === 'function' ? s.depth(t) : s.depth;
  const chars = Object.values(s.ctx.chars).filter(c => c.scene);
  for (const c of chars) { c.scene.style.perspective = MC.focal(cam, W) + 'px'; c.world.style.transform = MC.worldMatrix(cam, W); }
  if (!name) { chars.forEach(c => c.matte.style.display = 'none'); return; }
  const d = depthOf(name), im = await Film.img(p.still), k = W / d.w;
  const order = chars.map(c => { const q = c.last || {}; const size = q.size ?? c.skin.size ?? 1; const pr = MC.project(cam, W, H, [q.x || 0, (q.y || 0) + 0.9 * size + (q.hop || 0), q.z || 0]); return { c, q, pr, size }; }).sort((a, b) => b.pr.depth - a.pr.depth);
  order.forEach((o, rank) => {
    const { c, q, pr, size } = o; c.scene.style.zIndex = 10 + rank * 2; c.matte.style.zIndex = 11 + rank * 2;
    const g = c.matte.getContext('2d'); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, W, H);
    if (q.hidden || pr.depth < .3 || q.noOcclude) { c.matte.style.display = 'none'; return; }
    c.matte.style.display = '';
    const sc = pr.scale * size, x0 = Math.max(0, Math.floor((pr.x - sc * 1.3) / k)), x1 = Math.min(d.w, Math.ceil((pr.x + sc * 1.3) / k));
    const y0 = Math.max(0, Math.floor((pr.y - sc * 1.9) / k)), y1 = Math.min(d.h, Math.ceil((pr.y + sc * 1.5) / k));
    if (x1 <= x0 || y1 <= y0) return;
    const w = x1 - x0, h = y1 - y0, small = d.small; small.width = w; small.height = h;
    const sg = small.getContext('2d'), id = sg.createImageData(w, h), lim = (pr.depth - (q.margin ?? 0.7)) * 64;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (d.data[(y0 + y) * d.w + x0 + x] < lim) id.data[(y * w + x) * 4 + 3] = 255;
    sg.putImageData(id, 0, 0);
    g.imageSmoothingEnabled = false; g.drawImage(small, x0 * k, y0 * k, w * k, h * k);
    g.globalCompositeOperation = 'source-in'; g.imageSmoothingEnabled = true; g.drawImage(im, 0, 0, W, H);
  });
}
// nametag following a character's head
function tag(ctx, key, text, pos, opts = {}) {
  let el = ctx.el['tag_' + key]; if (!el) el = ctx.el['tag_' + key] = $('div', 'nametag', stage.tags);
  if (!ctx.cam || opts.hidden) { el.style.display = 'none'; return; }
  const q = MC.project(ctx.cam, W, H, [pos.x, pos.y + (opts.h ?? 2.15) + (pos.hop || 0), pos.z]);
  if (q.depth < 0.3) { el.style.display = 'none'; return; }
  const k = clamp(q.scale / 170, .6, 2.2);
  el.style.display = ''; el.innerHTML = text;
  el.style.transform = `translate(${q.x}px,${q.y}px) translate(-50%,-100%) scale(${k})`;
}
// an HTML element anchored to a world point (speech bubbles, markers)
function anchor(ctx, key, cls, html, p, opts = {}) {
  let el = ctx.el['a_' + key]; if (!el) el = ctx.el['a_' + key] = $('div', cls, stage.tags);
  const q = MC.project(ctx.cam, W, H, p);
  el.innerHTML = html; el.style.display = (opts.hidden || q.depth < .3) ? 'none' : '';
  const k = opts.fixed ? 1 : clamp(q.scale / 170, .4, 2.4);
  el.style.transform = `translate(${q.x}px,${q.y}px) translate(-50%,${opts.below ? '0' : '-100%'}) scale(${k * (opts.scale ?? 1)})`;
  el.style.opacity = opts.alpha ?? 1;
  return el;
}
// Minecraft-style chat: lines = [{at, html}], shown from `at`, fading after `hold`
function chat(ctx, lines, t, opts = {}) {
  let box = ctx.el.chat; if (!box) box = ctx.el.chat = $('div', 'mcchat', stage.ui);
  const hold = opts.hold ?? 9;
  box.innerHTML = lines.filter(l => t >= l.at && t < l.at + hold).slice(-(opts.max ?? 8))
    .map(l => `<div style="opacity:${1 - ramp(t, l.at + hold - .6, l.at + hold)}">${l.html}</div>`).join('');
  if (opts.style) box.style.cssText = opts.style;
}
// 2D camera move over plate + 3D together (Ken Burns)
function kenburns(scale, x = 0, y = 0) { stage.view.style.transform = `translate(${x}px,${y}px) scale(${scale})`; }
function el(ctx, key, cls, parent = stage.ui) { return ctx.el[key] || (ctx.el[key] = $('div', cls, parent)); }
function typed(text, t, t0, cps = 14) { return text.slice(0, Math.max(0, Math.floor((t - t0) * cps))); }
function fade(ctx, alpha, color = '#000') { const e = el(ctx, 'fade', 'fill', stage.fx); e.style.background = color; e.style.opacity = clamp(alpha); }
