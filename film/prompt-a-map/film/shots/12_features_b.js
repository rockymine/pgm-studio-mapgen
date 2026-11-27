// s13 express exit · s14 the core with a view · s15 extended play · s16 bridging
{
  const N = { P1: 'WoolGoblin', P2: 'BridgeBoi', P3: 'TNT_Tina', P4: 'ObbyOtto', KID: 'lil_stevie' };
  const died = (n, cls = 'mc-yellow') => `<span class="${cls}">${n}</span> <span class="mc-gray">fell out of the world</span>`;

  // ---------------- s13: the spawn whose doors open over the drop (Quatrefoil, yellow) ----------------
  {
    const Z = 40.5, Y = 9, IN = 41.6, EDGE = 48.15;
    const out = (t, ta, tb, tf, o = {}) => fall({ ...walkPath([[IN, Z + (o.dz || 0)], [EDGE, Z + (o.dz || 0)]], t, ta, tb, Y, { linear: true }), hidden: t < ta }, t, tf, 2.4, 0);
    Film.add({
      id: 's13', plate: still('qf_door'), cam: CAM('qf_door'), depth: 'qf_door',
      sfx: [{ at: 0, f: 'whoosh_short' }, { at: 0.02, f: 'pop' }, { at: 3.3, f: 'fall_whistle', gain: .5 }, { at: 4.75, f: 'fall_whistle', gain: .5 }, { at: 8.1, f: 'fall_whistle', gain: .55 }, { at: 4.3, f: 'splat_void', gain: .7 }, { at: 5.75, f: 'splat_void', gain: .7 }, { at: 9.1, f: 'splat_void', gain: .7 }],
      build(ctx) { addChar(ctx, 'a', SKINS.yel1); addChar(ctx, 'b', SKINS.yel3); addChar(ctx, 'c', SKINS.yel4); addChar(ctx, 'k', SKINS.kid); addChar(ctx, 'd', SKINS.yel2); },
      update(ctx, t, T) {
        featureCard(ctx, t, 3, 'The Express Exit');
        kenburns(lerp(1.0, 1.05, t / this.dur));
        actual(ctx, t, 1.5, 'QUATREFOIL', 'September 2026', 'yellow spawn: two doors, both over the drop');
        const a = out(t, 1.9, 3.25, 3.25), b = out(t, 3.35, 4.7, 4.7, { dz: .5 });
        ctx.chars.a.pose(a); ctx.chars.b.pose(b);
        // c stops on the kerb, looks down, gets shoved by the kid
        const cw = walkPath([[IN, Z], [47.45, Z]], t, 4.9, 6.2, Y, { linear: true }), wob = pulse(t, 6.2, 8.1, .2);
        ctx.chars.c.pose(fall({ ...cw, hidden: t < 4.9, headPitch: 45 * wob, armLout: 55 * wob + 12 * Math.sin(t * 9) * wob, armRout: 55 * wob - 12 * Math.sin(t * 9) * wob, lean: -6 * wob + 5 * Math.sin(t * 5) * wob }, t, 8.1, 2.6, .4));
        const kw = walkPath([[IN - 1, Z], [EDGE - .2, Z]], t, 7.35, 8.05, Y, { linear: true, stride: 1.6 });
        ctx.chars.k.pose(fall({ ...kw, hidden: t < 7.35, armL: 170, armR: 170, hop: .5 * Math.sin(ramp(t, 7.7, 8.3) * Math.PI) }, t, 8.15, 3.2, 0));
        // d comes to the door, peeks, stays
        const dw = walkPath([[IN, Z + .4], [45.9, Z + .4]], t, 8.5, 9.6, Y), peek = pulse(t, 9.6, 12, .3);
        ctx.chars.d.pose(P({ ...dw, hidden: t < 8.5, headPitch: 28 * peek, lean: -8 * peek, margin: 1.3 }, t, { say: 's13.3', gesture: false }));
        tag(ctx, 'd', mcName(N.P2, 'gold'), dw, { hidden: t < 9.2 });
        tag(ctx, 'c', mcName(N.P4, 'gold'), cw, { hidden: t < 5.6 || t > 8.1 });
        chat(ctx, [
          { at: 1.5, html: '<span class="mc-green">The match has started!</span>' },
          { at: 4.25, html: died(N.P1) }, { at: 5.7, html: died(N.P3) },
          { at: 9.0, html: died(N.KID) }, { at: 9.25, html: `<span class="mc-yellow">${N.P4}</span> <span class="mc-gray">was knocked out of the world by</span> <span class="mc-yellow">${N.KID}</span>` },
        ], t);
        quoteCard(ctx, t, 4.9, 8.0, '…a spawn facing outward opens its only exit over the drop.', 'actual review note, August 2026');
        dress(ctx, T, { ticker: false });
      },
    });
  }

  // ---------------- s14: the core that walked off the land (Goldhollow) ----------------
  {
    const A = { x: 79.6, y: 7, z: 58.8 }, B = { x: 80.2, y: 7, z: 55.4 }, CORE = [90.5, 9.5, 54.5];
    const wideAt = () => [L('s14.3').t1 + .1, L('s14.4').t0 - .2];
    Film.add({
      id: 's14',
      plate(t) { const [a, b] = wideAt(); return t >= a && t < b ? seq('gh_wide_move', a) : still('gh_pov'); },
      cam(t) { const [a, b] = wideAt(); return t >= a && t < b ? seqCam('gh_wide_move', a)(t) : CAM('gh_pov'); },
      sfx: [{ at: 0, f: 'whoosh_short' }, { at: 0.02, f: 'pop' }, { at: L('s14.3').t1 + .1, f: 'whoosh_long', gain: .7 }, { at: L('s14.5').t1 + .2, f: 'crickets', gain: .6 }, { at: L('s14.6').t0 - .3, f: 'pop' }],
      build(ctx) { addChar(ctx, 'a', SKINS.red1); addChar(ctx, 'b', SKINS.red2); },
      update(ctx, t, T) {
        featureCard(ctx, t, 4, 'Objectives<br>with a view');
        const [wa, wb] = wideAt(), wide = t >= wa && t < wb, l2 = L('s14.2'), l3 = L('s14.3'), l4 = L('s14.4');
        kenburns(wide ? 1 : lerp(1.0, 1.04, t / this.dur));
        const east = -90, toCam = yawTo(A.x, A.z, 73.5, 60.5);
        const look = ramp(t, l2.t0 + .9, l2.t0 + 1.2) - ramp(t, l3.t0, l3.t0 + .3);        // turns round looking for it
        const ask = pulse(t, l4.t0 - .2, l4.t1 + .6, .2);
        ctx.chars.a.pose(P({ ...A, yaw: lerp(east, toCam, Math.max(look, 0)) + 40 * ask, headYaw: look > 0 ? 55 * Math.sin(t * 4.2) : 0, hidden: wide }, t, { say: ['s14.2', 's14.4'], ph: 1 }));
        const point = pulse(t, l3.t0 - .1, l3.t1 + 2.2, .15);
        ctx.chars.b.pose(P({ ...B, yaw: east + 12, armR: 88 * point, armRout: 4, headYaw: -50 * pulse(t, L('s14.5').t0 - .2, L('s14.5').t1 + .3, .2), hidden: wide }, t, { say: ['s14.3', 's14.5'], gesture: false }));
        tag(ctx, 'a', mcName(N.P1, 'red'), A, { hidden: wide }); tag(ctx, 'b', mcName(N.P4, 'red'), B, { hidden: wide });
        if (wide) {
          anchor(ctx, 'm1', 'marker', 'THE CORE ↓', [90.5, 15, 54.5], { fixed: true });
          anchor(ctx, 'm2', 'marker', '↑ THE MAP', [52, 6, 44], { fixed: true, below: true });
          anchor(ctx, 'm3', 'marker', '← 7 blocks of air', [86, 3, 62], { fixed: true, below: true, scale: .7 });
        } else ['m1', 'm2', 'm3'].forEach(k => { if (ctx.el['a_' + k]) ctx.el['a_' + k].style.display = 'none'; });
        scoreboard(ctx, 'Goldhollow', [['<span class="mc-red">Red Core</span>', '<span class="mc-green">✔ 100%</span>'], ['<span class="mc-blue">Blue Core</span>', '<span class="mc-green">✔ 100%</span>'], ['<span class="mc-gray">Reachable</span>', '<span class="mc-red">0</span>']]);
        actual(ctx, t, 1.5, 'GOLDHOLLOW', 'August 2026', 'a capture-the-wool layout wearing a destroy-the-core hat');
        const l6 = L('s14.6'); mascot(ctx, t, l6.t0 - .3, l6.t1 + .3);
        quoteCard(ctx, t, wa + .2, wb, '…fifteen capture boards wearing three different hats.', 'actual review, August 2026');
        dress(ctx, T, { ticker: false });
      },
    });
  }

  // ---------------- s15: the monument that could be rebuilt (Scarrow Delph) ----------------
  {
    const AT = { x: 23.4, y: 32, z: -57.3 }, DF0 = [19.2, -55.6], DF1 = [21.6, -56.4], BLOCK = [22.5, 36.5, -57.5];
    const l = n => L('s15.' + n);
    const tBreak = l(2).t0 - .12, tPick = l(3).t0 - .25, tPlace = l(3).t1 + .35, m0 = l(4).t1 + .35, m1 = l(5).t0 - .5;
    // montage: break/place cycles that get faster
    const cyc = (t) => { const k = ramp(t, m0, m1), n = 22 * k * k + 3 * k; return { n: Math.floor(n), f: n % 1, k }; };
    const mined = t => (t >= tBreak && t < tPlace) || (t >= m0 && t < m1 && cyc(t).f < .5) || false;
    const sfx = [{ at: 0, f: 'whoosh_short' }, { at: 0.02, f: 'pop' }, { at: tBreak, f: 'block_break_1' }, { at: tPick, f: 'pop', gain: .6 }, { at: tPlace, f: 'block_place' }, { at: m0, f: 'fast_forward', gain: .6 }, { at: m0 + 2, f: 'fast_forward', gain: .6 }, { at: m1 - .1, f: 'power_down', gain: .6 }];
    for (let i = 0; i < 5; i++) sfx.push({ at: tBreak - 2.3 + i * .45, f: 'block_break_' + (2 + i % 2), gain: .5 });
    { let last = -1; for (let t = m0; t < m1; t += 1 / 30) { const c = cyc(t), h = c.n * 2 + (c.f < .5 ? 0 : 1); if (h !== last) { sfx.push({ at: t, f: c.f < .5 ? 'block_break_1' : 'block_place', gain: .45 }); last = h; } } }
    Film.add({
      id: 's15', plate: t => still(mined(t) ? 'sc_mined' : 'sc_mon'), cam: CAM('sc_mon'),
      sfx,
      grade: t => { const k = ramp(t, m0, m1); return t >= m0 && t < m1 ? `brightness(${.72 + .28 * Math.cos(k * Math.PI * 6)}) hue-rotate(${-18 * (1 - Math.cos(k * Math.PI * 6)) / 2}deg)` : ''; },
      build(ctx) { addChar(ctx, 'a', SKINS.blue1).hold(SKINS.items.pick); addChar(ctx, 'd', SKINS.red2); },
      update(ctx, t, T) {
        featureCard(ctx, t, 5, 'Extended Play');
        kenburns(lerp(1.0, 1.06, t / this.dur));
        const fast = t >= m0 && t < m1, c = cyc(t), tired = ramp(t, m1 - .3, m1 + .3);
        const swing = (fast ? 1 : pulse(t, tBreak - 2.4, tBreak + .05, .1)) * (1 - tired);
        const rate = fast ? 20 + 30 * c.k : 14;
        ctx.chars.a.pose(P({ ...AT, yaw: yawTo(AT.x, AT.z, 22.5, -57.9) , headPitch: -55 * (1 - tired) + 30 * tired, armR: (120 + 35 * Math.sin(t * rate)) * swing + 8 * tired, lean: 14 * tired, armL: 6 * tired }, t, { say: ['s15.2', 's15.4', 's15.5'], gesture: false }));
        // defender: wanders over, picks the block up, puts it back
        const w = walkPath([DF0, DF1], t, tBreak + .5, tPick, 32), place = fast ? (c.f >= .5 ? 1 : 0) * 1 : pulse(t, tPlace - .25, tPlace + .25, .1);
        ctx.chars.d.pose(P({ ...w, yaw: t >= tPick ? yawTo(DF1[0], DF1[1], 22.5, -57.5) : w.yaw, headPitch: t >= tPick ? -50 : 0, armR: 150 * place + (fast ? 20 * Math.sin(t * rate) : 0) }, t, { say: 's15.3', gesture: false, ph: 3 }));
        ctx.chars.d.hold(t >= tPick && t < tPlace ? SKINS.items.obsidian : null);
        tag(ctx, 'a', mcName(N.P3, 'blue'), AT); tag(ctx, 'd', mcName(N.P2, 'red'), w);
        // the dropped block, falling to the ground between them
        const dk = ramp(t, tBreak, tBreak + .55), py = lerp(BLOCK[1], 32.35, dk * dk) + (dk >= 1 ? .08 * Math.sin(t * 5) : 0);
        const it = anchor(ctx, 'item', 'itemdrop', '', [lerp(BLOCK[0], 22.4, dk), py, lerp(BLOCK[2], -56.6, dk)], { hidden: !(t >= tBreak && t < tPick), scale: .9 });
        it.style.transform += ` rotate(${t * 140}deg)`;
        // clock + score
        const mins = fast ? 7.2 + 220 * c.k : (t >= m1 ? 227.2 : 5 + t * .15), hh = Math.floor(mins / 60), mm = Math.floor(mins % 60), ss = Math.floor((mins * 60) % 60);
        const clk = el(ctx, 'clock', 'clock'); clk.innerHTML = `<span class="mc-gray">Match time</span> ${hh}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}`;
        clk.style.transform = `scale(${1 + .3 * pulse(t, m0, m1 + .8, .3)})`; clk.style.opacity = t > 1.35 ? 1 : 0;
        scoreboard(ctx, 'Scarrow Delph', [['<span class="mc-red">The Gallery</span>', mined(t) ? '<span class="mc-yellow">33%</span>' : '<span class="mc-green">0%</span>'], ['<span class="mc-gray">Repairs</span>', String(t < tPlace ? 0 : 1 + (fast ? c.n : t >= m1 ? 25 : 0))]]);
        const reps = []; if (t >= tBreak) reps.push({ at: tBreak, html: `<span class="mc-blue">${N.P3}</span> damaged <span class="mc-red">The Gallery</span>` });
        if (t >= tPlace) reps.push({ at: tPlace, html: `<span class="mc-red">${N.P2}</span> repaired <span class="mc-red">The Gallery</span>` });
        if (fast) for (let i = Math.max(0, c.n - 3); i <= c.n; i++) reps.push({ at: m0, html: `<span class="mc-blue">${N.P3}</span> damaged <span class="mc-red">The Gallery</span>` }, { at: m0, html: `<span class="mc-red">${N.P2}</span> repaired <span class="mc-red">The Gallery</span>` });
        chat(ctx, reps.slice(fast ? -(4 + c.n % 2) : -8), t, { max: 5, hold: fast ? 99 : 6 });
        const cap = el(ctx, 'cap', 'caption'); cap.innerHTML = 'Three hours later'; cap.style.top = '430px'; cap.style.opacity = pulse(t, m0 + 1.2, m1 + .2, .25);
        actual(ctx, t, 1.5, 'SCARROW DELPH', 'September 2026', 'the obsidian dropped, so the defenders put it back');
        quoteCard(ctx, t, tPlace + .4, m0 + 1.1, '…for as long as the match ran.', 'the fix’s own commit message');
        dress(ctx, T, { ticker: false });
      },
    });
  }

  // ---------------- s16: the build zone in sight and out of reach (Gypsum Reach) ----------------
  {
    const A = { x: -25.3, y: 16, z: 37.2 }, B = { x: -27.3, y: 16, z: 39.1 };
    const tries = [4.3, 5.0, 5.7], zoneAt = 6.3;
    Film.add({
      id: 's16', plate: still('gyp_eye'), cam: CAM('gyp_eye'),
      sfx: [{ at: 0, f: 'whoosh_short' }, { at: 0.02, f: 'pop' }, ...tries.map(a => ({ at: a, f: 'error_beep', gain: .7 })), { at: zoneAt, f: 'sparkle' }],
      build(ctx) { addChar(ctx, 'a', SKINS.red1); addChar(ctx, 'b', SKINS.kid); },
      update(ctx, t, T) {
        featureCard(ctx, t, 6, 'Bridging');
        kenburns(lerp(1.0, 1.06, t / this.dur));
        const l2 = L('s16.2'), place = Math.max(...tries.map(a => pulse(t, a - .15, a + .25, .1))), point = pulse(t, l2.t0 - .2, l2.t1 + 1.2, .2);
        ctx.chars.a.pose(P({ ...A, yaw: -90 + 30 * ramp(t, l2.t0 - .4, l2.t0), headPitch: 35 * (1 - point) * ramp(t, 3.6, 4.2), lean: -10 * place, armR: 70 * place + 85 * point, headYaw: 0 }, t, { say: 's16.2', gesture: false }));
        ctx.chars.b.pose(P({ ...B, yaw: -100, headYaw: 20 * Math.sin(t * 1.3), hop: .25 * Math.abs(Math.sin(t * 5)) * pulse(t, zoneAt, zoneAt + 1, .2) }, t, { ph: 2 }));
        tag(ctx, 'a', mcName(N.P1, 'red'), A); tag(ctx, 'b', mcName(N.KID, 'red'), B, { h: 1.6 });
        const z = ease(ramp(t, zoneAt, zoneAt + .5));
        quad3d(ctx, 'zone', 'zone3d', { x0: -16, x1: -9, z0: 24, z1: 48, y: 16.02, alpha: z * (0.75 + .25 * Math.sin(t * 6)) });
        quad3d(ctx, 'gap', 'gap3d', { x0: -24, x1: -16, z0: 30, z1: 46, y: 16.02, alpha: z * .9 });
        anchor(ctx, 'mz', 'marker', '↑ BUILD ZONE', [-12.5, 16.2, 40], { fixed: true, below: true, hidden: z < .5, scale: .8 });
        anchor(ctx, 'mg', 'marker', '8 blocks of nothing', [-20, 16.5, 43], { fixed: true, below: true, hidden: z < .5, scale: .62 });
        const ab = el(ctx, 'ab', 'actionbar'); const on = Math.max(...tries.map(a => pulse(t, a, a + .65, .08)));
        ab.innerHTML = '<span class="mc-red" style="background:rgba(0,0,0,.55);padding:4px 26px">⚠ You may not build here</span>'; ab.style.opacity = on; ab.style.bottom = '330px'; ab.style.fontSize = '70px';
        actual(ctx, t, 1.5, 'GYPSUM REACH', 'September 2026', 'the coast moved back; the build zone did not');
        quoteCard(ctx, t, zoneAt + .9, this.dur, '…leaves the zone in sight and out of reach.', 'the studio’s own documentation');
        dress(ctx, T, { ticker: false });
      },
    });
  }
}
