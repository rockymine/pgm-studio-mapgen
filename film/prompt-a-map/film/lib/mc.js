// Blocky characters in a CSS 3D scene whose camera matches the eye renderer's.
// World coords are Minecraft's (x east, y up, z south); yaw 0 looks south (+z), pitch + looks down.
const MC = (() => {
  const S = 128;            // css px per block inside the 3D world
  const U = S * 1.8 / 32;   // one skin pixel

  const rad = d => d * Math.PI / 180;

  // camera basis exactly as the renderer's Lens.Of
  function basis(cam) {
    const yaw = rad(cam.yaw), pitch = rad(cam.pitch);
    const f = [-Math.sin(yaw) * Math.cos(pitch), -Math.sin(pitch), Math.cos(yaw) * Math.cos(pitch)];
    const r = [-Math.cos(yaw), 0, -Math.sin(yaw)];
    let u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]];
    if (u[1] < 0) u = u.map(v => -v);
    return { f, r, u };
  }
  const focal = (cam, W) => (W / 2) / Math.tan(rad(cam.fov ?? 70) / 2);

  // matrix3d for the world div: local = (x*S, -y*S, z*S)
  function worldMatrix(cam, W) {
    const { f, r, u } = basis(cam), F = focal(cam, W);
    const A = [r, u.map(v => -v), f.map(v => -v)];           // rows: css x, y, z
    const D = [1, -1, 1];
    const C = [cam.x, cam.y, cam.z];
    const m = [];
    for (let col = 0; col < 3; col++) { for (let row = 0; row < 3; row++) m.push(A[row][col] * D[col]); m.push(0); }
    const t = A.map(row => -(row[0] * C[0] + row[1] * C[1] + row[2] * C[2]) * S);
    m.push(t[0], t[1], t[2] + F, 1);
    return `matrix3d(${m.map(v => +v.toFixed(5)).join(',')})`;
  }

  // world point -> stage pixel (and depth), for 2D labels
  function project(cam, W, H, p) {
    const { f, r, u } = basis(cam), F = focal(cam, W);
    const d = [p[0] - cam.x, p[1] - cam.y, p[2] - cam.z];
    const cz = d[0] * f[0] + d[1] * f[1] + d[2] * f[2];
    const cx = d[0] * r[0] + d[1] * r[1] + d[2] * r[2];
    const cy = d[0] * u[0] + d[1] * u[1] + d[2] * u[2];
    return { x: W / 2 + cx / cz * F, y: H / 2 - cy / cz * F, depth: cz, scale: F / cz };
  }

  // ---- textures -------------------------------------------------------------------------------
  const cache = new Map();
  function shadeHex(hex, k) {
    const n = parseInt(hex.slice(1), 16);
    const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map(v => Math.max(0, Math.min(255, Math.round(v * k))));
    return `rgb(${c[0]},${c[1]},${c[2]})`;
  }
  // rows: array of strings, one char a pixel, looked up in pal; '.' or missing = base
  function tex(w, h, base, rows, pal, k) {
    const key = [w, h, base, rows && rows.join('/'), k].join('|');
    if (cache.has(key)) return cache.get(key);
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d');
    g.fillStyle = shadeHex(base, k); g.fillRect(0, 0, w, h);
    if (rows) rows.forEach((row, y) => [...row].forEach((ch, x) => {
      if (ch === '.' || ch === ' ' || !pal[ch]) return;
      g.fillStyle = shadeHex(pal[ch], k); g.fillRect(x, y, 1, 1);
    }));
    // faint pixel noise so flat colours read as a skin, deterministic
    let s = (w * 131 + h * 17 + base.charCodeAt(1) * 7 + base.charCodeAt(3)) | 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      s = (s * 16807 + 11) % 2147483647;
      if (s % 5 === 0) { g.fillStyle = s % 2 ? 'rgba(0,0,0,.07)' : 'rgba(255,255,255,.06)'; g.fillRect(x, y, 1, 1); }
    }
    const url = c.toDataURL(); cache.set(key, url); return url;
  }

  const LIGHT = { front: 0.94, back: 0.62, left: 0.78, right: 0.72, top: 1.0, bottom: 0.5 };

  // a cuboid w x h x d (skin px), its pivot at (px,py,pz) measured from the box's min corner (y from top)
  function box(w, h, d, spec, pal, pivot) {
    const el = document.createElement('div'); el.className = 'mcbox';
    const faces = {
      front: [w, h, `translate3d(${-w / 2 * U}px,${-h / 2 * U}px,${d / 2 * U}px)`],
      back: [w, h, `rotateY(180deg) translate3d(${-w / 2 * U}px,${-h / 2 * U}px,${d / 2 * U}px)`],
      right: [d, h, `rotateY(90deg) translate3d(${-d / 2 * U}px,${-h / 2 * U}px,${w / 2 * U}px)`],
      left: [d, h, `rotateY(-90deg) translate3d(${-d / 2 * U}px,${-h / 2 * U}px,${w / 2 * U}px)`],
      top: [w, d, `rotateX(90deg) translate3d(${-w / 2 * U}px,${-d / 2 * U}px,${h / 2 * U}px)`],
      bottom: [w, d, `rotateX(-90deg) translate3d(${-w / 2 * U}px,${-d / 2 * U}px,${h / 2 * U}px)`],
    };
    const inner = document.createElement('div'); inner.className = 'mcbox';
    // move box centre so that pivot sits at the element origin
    inner.style.transform = `translate3d(${(w / 2 - pivot[0]) * U}px,${(h / 2 - pivot[1]) * U}px,${(d / 2 - pivot[2]) * U}px)`;
    for (const [name, [fw, fh, tf]] of Object.entries(faces)) {
      const f = document.createElement('div'); f.className = 'mcface';
      f.style.width = fw * U + 'px'; f.style.height = fh * U + 'px'; f.style.transform = tf;
      const rows = spec[name] || (name !== 'front' && name !== 'top' && name !== 'bottom' ? spec.side : null);
      const base = (name === 'top' && spec.topBase) || (name === 'bottom' && spec.bottomBase) || spec.base;
      f.style.backgroundImage = `url(${tex(fw, fh, base, rows, pal, LIGHT[name])})`;
      inner.appendChild(f);
    }
    el.appendChild(inner); return el;
  }

  // ---- character ------------------------------------------------------------------------------
  function character(skin) {
    const pal = skin.pal || {};
    const root = document.createElement('div'); root.className = 'mcbox mcchar';
    const shadow = document.createElement('div'); shadow.className = 'mcshadow';
    shadow.style.width = shadow.style.height = 14 * U + 'px';
    shadow.style.transform = `rotateX(90deg) translate3d(${-7 * U}px,${-7 * U}px,0)`;
    const rig = document.createElement('div'); rig.className = 'mcbox';   // everything that leans/jumps
    const part = (w, h, d, spec, pivot, at) => {
      const b = box(w, h, d, spec, pal, pivot);
      b.dataset.at = at.join(','); b.style.transform = `translate3d(${at[0] * U}px,${-at[1] * U}px,${at[2] * U}px)`;
      rig.appendChild(b); return b;
    };
    const P = {
      legL: part(4, 12, 4, skin.leg, [2, 0, 2], [2, 12, 0]),
      legR: part(4, 12, 4, skin.leg, [2, 0, 2], [-2, 12, 0]),
      body: part(8, 12, 4, skin.body, [4, 12, 2], [0, 12, 0]),
      armL: part(4, 12, 4, skin.arm, [2, 2, 2], [6, 22, 0]),
      armR: part(4, 12, 4, skin.arm, [2, 2, 2], [-6, 22, 0]),
      head: part(8, 8, 8, skin.head, [4, 8, 4], [0, 24, 0]),
    };
    if (skin.hat) { // an overlay box on the head (headset, hard hat, crown...)
      const h = box(skin.hat.w, skin.hat.h, skin.hat.d, skin.hat, pal, [skin.hat.w / 2, skin.hat.h, skin.hat.d / 2]);
      h.style.transform = `translate3d(${(skin.hat.x || 0) * U}px,${-(skin.hat.y ?? 8) * U}px,${(skin.hat.z || 0) * U}px)`;
      P.head.appendChild(h);
    }
    let held = null;
    function hold(spec) { // a box in the right hand
      if (held) held.remove();
      if (!spec) { held = null; return; }
      held = box(spec.w, spec.h, spec.d, spec, spec.pal || pal, [spec.w / 2, spec.h / 2, spec.d / 2]);
      held.style.transform = `translate3d(0,${10.5 * U}px,${(spec.d / 2 + 1) * U}px) rotateX(${spec.tilt ?? -20}deg)`;
      P.armR.appendChild(held);
    }
    root.appendChild(shadow); root.appendChild(rig);
    const setPart = (b, tf) => { const at = b.dataset.at.split(',').map(Number); b.style.transform = `translate3d(${at[0] * U}px,${-at[1] * U}px,${at[2] * U}px) ${tf}`; };
    function pose(p) {
      const size = p.size ?? skin.size ?? 1;
      root.style.display = p.hidden ? 'none' : '';
      root.style.transform = `translate3d(${p.x * S}px,${-p.y * S}px,${p.z * S}px) rotateY(${-(p.yaw || 0)}deg) scale3d(${size},${size},${size})`;
      rig.style.transform = `translateY(${-(p.hop || 0) * S}px) rotateX(${p.lean || 0}deg) rotateZ(${p.roll || 0}deg)`;
      shadow.style.opacity = p.noShadow ? 0 : Math.max(0, 0.38 - (p.hop || 0) * 0.15);
      setPart(P.legL, `rotateX(${p.legL || 0}deg)`);
      setPart(P.legR, `rotateX(${p.legR || 0}deg)`);
      setPart(P.armL, `rotateX(${p.armL || 0}deg) rotateZ(${-(p.armLout || 0)}deg)`);
      setPart(P.armR, `rotateX(${p.armR || 0}deg) rotateZ(${p.armRout || 0}deg)`);
      setPart(P.head, `rotateY(${-(p.headYaw || 0)}deg) rotateX(${-(p.headPitch || 0)}deg)`);
      setPart(P.body, '');
      root.style.opacity = p.alpha ?? 1;
    }
    return { el: root, pose, hold, skin };
  }

  // walk cycle helper: returns limb angles for a distance travelled (blocks)
  const walk = (dist, amp = 38) => { const a = Math.sin(dist * 2.6) * amp; return { legL: a, legR: -a, armL: -a, armR: a }; };

  return { S, U, basis, focal, worldMatrix, project, character, box, walk, tex };
})();
