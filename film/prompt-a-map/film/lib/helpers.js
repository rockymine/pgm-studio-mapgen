// Shot-writing helpers on top of the engine.
const L = id => Film.line(id);
const CAM = name => CAMS[name].cam;
const still = name => ({ still: `plates/${name}.jpg` });
const seq = (name, at = 0) => ({ seq: `plates/${name}/`, n: CAMS[name].frames, fps: FPS, at });
function seqCam(name, at = 0) {
  const c = CAMS[name];
  return t => { const n = Math.min(c.frames - 1, Math.max(0, Math.round((t - at) * FPS))); let k = n / (c.frames - 1); if (c.ease !== false) k = k * k * (3 - 2 * k); return lerpCam(c.from, c.to, k); };
}
// 1 while any of the lines is being spoken
const speaking = (t, ids) => Math.max(0, ...[].concat(ids || []).map(id => { const l = L(id); return l.missing ? 0 : pulse(t, l.t0 - .05, l.t1 + .05, .1); }));
// idle breathing + talking bob laid over a base pose
function P(base, t, o = {}) {
  const sp = speaking(t, o.say), ph = o.ph || 0, idle = Math.sin(t * 1.6 + ph);
  const p = { armL: 2.5 * idle, armR: -2.5 * idle, ...base };
  p.headPitch = (base.headPitch || 0) + sp * Math.sin(t * 12 + ph) * 5;
  p.headYaw = (base.headYaw || 0) + sp * Math.sin(t * 4.3 + ph) * 5;
  p.hop = (base.hop || 0) + sp * Math.abs(Math.sin(t * 6.2 + ph)) * 0.045;
  if (sp && o.gesture !== false) { p.armR = (p.armR || 0) + sp * (38 + 22 * Math.sin(t * 7 + ph)); p.armRout = (p.armRout || 0) + sp * 10; }
  return p;
}
// walk along a path of [x,z] waypoints between times ta..tb; returns pose fields (x,z,yaw,limbs)
function walkPath(points, t, ta, tb, y, o = {}) {
  const k = o.linear ? ramp(t, ta, tb) : ease(ramp(t, ta, tb));
  const seg = []; let total = 0;
  for (let i = 1; i < points.length; i++) { const d = Math.hypot(points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1]); seg.push(d); total += d; }
  let d = k * total, i = 0; while (i < seg.length - 1 && d > seg[i]) { d -= seg[i]; i++; }
  const f = seg[i] ? d / seg[i] : 0, a = points[i], b = points[i + 1];
  const x = lerp(a[0], b[0], f), z = lerp(a[1], b[1], f);
  const yaw = Math.atan2(-(b[0] - a[0]), b[1] - a[1]) * 180 / Math.PI;
  const moving = t > ta && t < tb;
  return { x, y, z, yaw, ...(moving ? MC.walk(k * total * (o.stride || 1), o.amp || 40) : {}) };
}
const yawTo = (ax, az, bx, bz) => Math.atan2(-(bx - ax), bz - az) * 180 / Math.PI;
const mcName = (name, cls) => `<b class="${cls || ''}">${name}</b>`;

// infomercial dressing: corner bug + ticker
const TICK = 'TYPE <b>/ORDER</b> NOW &nbsp;★&nbsp; ONLY <b>0 EMERALDS</b> &nbsp;★&nbsp; OPERATORS ARE STANDING IN SPAWN &nbsp;★&nbsp; NOT ELIGIBLE FOR ANY MAPPIE &nbsp;★&nbsp; NO TASTE REQUIRED &nbsp;★&nbsp; RESULTS EXTREMELY TYPICAL &nbsp;★&nbsp; ';
function dress(ctx, T, o = {}) {
  if (o.bug !== false) el(ctx, 'bug', 'bug').innerHTML = 'AS SEEN ON OC.TC';
  if (o.ticker !== false) {
    const tk = el(ctx, 'ticker', 'ticker'); if (!tk.firstChild) $('div', '', tk, TICK.repeat(4));
    tk.firstChild.style.left = -((T * 190) % 2600) + 'px';
  }
}
// lower third: small red label, big yellow line, black strap
function lower(ctx, t, t0, t1, a, b, c) {
  const e = el(ctx, 'lower', 'lower'); const k = Math.min(back(ramp(t, t0, t0 + .35)), 1 - ramp(t, t1 - .25, t1));
  e.innerHTML = `<div class="a">${a}</div><div class="b">${b}</div>${c ? `<div class="c">${c}</div>` : ''}`;
  e.style.transform = `translateX(${(k - 1) * 1100}px)`; e.style.opacity = t >= t0 && t < t1 ? 1 : 0;
}
// full-screen "FEATURE N" slam for the first `d` seconds of a shot
function featureCard(ctx, t, n, title, d = 1.35) {
  const e = el(ctx, 'feat', 'feature', stage.fx);
  if (!e.firstChild) e.innerHTML = `<div class="rays"></div><div class="n">FEATURE Nº ${n}</div><div class="t">${title}</div>`;
  e.style.display = t < d ? '' : 'none';
  e.querySelector('.rays').style.transform = `rotate(${t * 40}deg)`;
  const k = back(ramp(t, 0, .28));
  e.querySelector('.t').style.transform = `scale(${lerp(2.4, 1, k)}) rotate(${lerp(-8, -3, k)}deg)`;
  e.querySelector('.n').style.transform = `translateY(${lerp(-300, 0, easeOut(ramp(t, 0, .25)))}px)`;
  e.style.opacity = 1 - ramp(t, d - .12, d);
}
// "ACTUAL AI MAP" strap for a real world
function actual(ctx, t, t0, map, date, extra) {
  lower(ctx, t, t0, 1e9, 'ACTUAL AI-MADE MAP · NOT A REENACTMENT', map, `${date}${extra ? ' · ' + extra : ''}`);
}
function quoteCard(ctx, t, t0, t1, text, src) {
  const e = el(ctx, 'quote', 'quote'); e.innerHTML = `“${text}”<small>${src}</small>`;
  const k = Math.min(back(ramp(t, t0, t0 + .3)), 1 - ramp(t, t1 - .2, t1));
  e.style.transform = `rotate(${lerp(8, 2, k)}deg) scale(${k})`; e.style.opacity = t >= t0 && t < t1 ? 1 : 0;
}
function confetti(ctx, t, t0, n = 90, seed = 5) {
  const r = rnd(seed), cols = ['#ffd21f', '#d9150b', '#1a2fa8', '#ffffff', '#3b9b3b'];
  let box = ctx.el.conf; if (!box) { box = ctx.el.conf = $('div', 'layer', stage.ui); for (let i = 0; i < n; i++) $('div', 'confetti', box); }
  [...box.children].forEach((c, i) => {
    const x0 = 960 + (r() - .5) * 300, vx = (r() - .5) * 1900, vy = -700 - r() * 1100, rot = r() * 720, col = cols[i % cols.length];
    const dt = t - t0; const x = x0 + vx * dt, y = 520 + vy * dt + 1500 * dt * dt;
    c.style.cssText = `transform:translate(${x}px,${y}px) rotate(${rot * dt}deg);background:${col};opacity:${dt < 0 || y > 1150 ? 0 : 1}`;
  });
}

// the Machine pops up in a corner of the frame, in its own little 3D scene
function mascot(ctx, t, t0, t1, o = {}) {
  let m = ctx.el.mascot;
  if (!m) {
    m = ctx.el.mascot = $('div', 'pip', stage.ui); m.style.cssText = `right:${o.right ?? 40}px;bottom:${o.bottom ?? 64}px;width:520px;height:560px`;
    const sc = $('div', 'scene3d', m), w = $('div', 'world3d', sc); const cam = { x: 0, y: 1.25, z: -3.2, yaw: 0, pitch: 0, fov: 50 };
    sc.style.perspective = MC.focal(cam, 520) + 'px'; w.style.transform = MC.worldMatrix(cam, 520);
    ctx.mascotChar = MC.character(SKINS.machine); w.appendChild(ctx.mascotChar.el);
  }
  const k = Math.min(back(ramp(t, t0, t0 + .3)), 1 - easeIn(ramp(t, t1, t1 + .25)));
  m.style.display = t >= t0 && t < t1 + .25 ? '' : 'none';
  const sp = pulse(t, t0 + .2, t1, .1);
  ctx.mascotChar.pose({ x: 0, y: -2.2 + 2.2 * k, z: 0, yaw: 180 + 8 * Math.sin(t * 2), headPitch: sp * Math.sin(t * 12) * 5, armL: 150 * sp, armLout: 14 + 10 * Math.sin(t * 9), noShadow: true });
}

// a flat rectangle lying in the world at height y (drawn in the shared 3D layer)
function quad3d(ctx, key, cls, r, html = '') {
  let q = ctx.el['q_' + key]; if (!q) { q = ctx.el['q_' + key] = $('div', cls, stage.w3); q.innerHTML = html; }
  const S = MC.S; q.style.width = (r.x1 - r.x0) * S + 'px'; q.style.height = (r.z1 - r.z0) * S + 'px';
  q.style.transform = `translate3d(${r.x0 * S}px,${-r.y * S}px,${r.z0 * S}px) rotateX(90deg)`;
  q.style.opacity = r.alpha ?? 1; return q;
}
// tumble off the world from (x,y,z) at time tf, drifting along (dx,dz)
function fall(p, t, tf, dx = 1.6, dz = 0) {
  if (t < tf) return p; const dt = t - tf;
  return { ...p, x: p.x + dx * dt, z: p.z + dz * dt, y: p.y - 17 * dt * dt, roll: dt * 190, lean: -dt * 120, armL: 170, armR: 170, armLout: 30 + 25 * Math.sin(t * 30), armRout: 30 - 25 * Math.sin(t * 30), legL: 35 * Math.sin(t * 25), legR: -35 * Math.sin(t * 25), noShadow: true, hidden: dt > 1.6 };
}
function scoreboard(ctx, title, rows) { const e = el(ctx, 'sb', 'scoreboard'); e.innerHTML = `<h4>${title}</h4>` + rows.map(r => `<div class="row"><span>${r[0]}</span><span>${r[1]}</span></div>`).join(''); }
function stampAt(ctx, key, text, t, t0, o = {}) {
  const st = el(ctx, 'st_' + key, 'stamp' + (o.green ? ' green' : '')); st.innerHTML = text;
  const k = ramp(t, t0, t0 + .14);
  st.style.cssText = `left:${o.x ?? 300}px;top:${o.y ?? 300}px;font-size:${o.size ?? 200}px;opacity:${k && t < (o.until ?? 1e9) ? 1 : 0};transform:scale(${lerp(3, 1, easeOut(k))}) rotate(${o.rot ?? -9}deg)`;
}
