// s02–s05: the product, the prompt, the machine room, the fifteen maps.
{
  const PM = { x: 0.9, y: 2, z: 6.2 }, RB = { x: -2.7, y: 2, z: 7.5 }, DL = { x: 2.3, z: 5.3, y: 2 };

  Film.add({
    id: 's02', plate: still('studio_main'), cam: CAM('studio_main'),
    sfx: [{ at: 0, f: 'whoosh_short' }, { at: 0.05, f: 'tada', gain: .8 }, { at: 2.2, f: 'confetti' }, { at: 2.25, f: 'infomercial_sting', gain: .9 }],
    music: { f: 'infomercial', at: 0, gain: .55, until: 's04' },
    build(ctx) {
      addChar(ctx, 'pm', SKINS.pitchman).hold(SKINS.items.mic);
      addChar(ctx, 'rb', SKINS.machine); addChar(ctx, 'dale', SKINS.dale);
      ctx.el.logo = $('div', 'logo', stage.ui, 'PROMPT<em>-A-</em>MAP<sup>™</sup>');
      ctx.el.logo.style.cssText = 'position:absolute;left:50%;top:60px;transform-origin:50% 0';
      ['NO<br>WORLDEDIT!', 'NO<br>XML!', 'NO TASTE<br>REQUIRED!'].forEach((s, i) => { const b = $('div', 'burst' + (i === 2 ? ' red' : ''), stage.ui, s); ctx.el['b' + i] = b; });
    },
    update(ctx, t, T) {
      const l1 = L('s02.1'), l2 = L('s02.2'), l3 = L('s02.3'), l4 = L('s02.4'), l5 = L('s02.5');
      kenburns(lerp(1, 1.06, t / this.dur));
      dress(ctx, T);
      fade(ctx, 1 - ramp(t, 0, .3), '#fff');
      // pitchman
      const slam = l1.t1 - 0.95, up = pulse(t, slam, slam + 1.6, .18);
      const nos = [0, 1, 2].map(i => pulse(t, l3.t0 + i * (l3.t1 - l3.t0) / 3, l3.t0 + (i + 1) * (l3.t1 - l3.t0) / 3, .08));
      const toDale = ease(ramp(t, l4.t0 - .2, l4.t0 + .2));
      ctx.chars.pm.pose(P({
        ...PM, yaw: 180 + toDale * 28, headYaw: toDale * 24,
        armL: up * 165 + nos[1] * 150, armLout: up * 28 + nos[1] * 20, armR: up * 165 + nos[0] * 150 + nos[2] * 160, armRout: up * 28 + nos[0] * 20 + nos[2] * 30,
        hop: up * Math.abs(Math.sin(t * 9)) * .12,
      }, t, { say: ['s02.1', 's02.2', 's02.3', 's02.5'], gesture: !(up || nos.some(Boolean)) }));
      tag(ctx, 'pm', mcName('THE PITCHMAN', 'gold'), PM, { hidden: t > slam - .1 && t < l2.t0 + .4 });
      // the machine pops up on "artificial intelligence"
      const pop = l2.t0 + 1.0, k = back(ramp(t, pop, pop + .35));
      ctx.chars.rb.pose({ ...RB, y: RB.y - 3 + 3 * k, yaw: 166, hidden: t < pop, armL: 160 * pulse(t, pop + .3, pop + 2.2, .2), armLout: 20 + 14 * Math.sin(t * 11), headYaw: 6 * Math.sin(t * 2) });
      tag(ctx, 'rb', mcName('THE MACHINE', 'aqua'), RB, { hidden: t < pop + .3 });
      // dale walks in
      const wa = l4.t0 - 1.9, wb = l4.t0 - .15;
      const w = walkPath([[9, DL.z - 1], [DL.x, DL.z]], t, wa, wb, DL.y);
      const face = yawTo(DL.x, DL.z, PM.x, PM.z) + 35, shrug = pulse(t, l5.t1 - .2, this.dur, .2);
      ctx.chars.dale.pose(P({ ...w, yaw: t >= wb ? face : w.yaw, hidden: t < wa, headPitch: -6, armLout: shrug * 34, armRout: shrug * 34, armL: shrug * 20, armR: shrug * 20 }, t, { say: 's02.4', ph: 2 }));
      tag(ctx, 'dale', mcName('Dale'), w, { hidden: t < wa + .4 });
      // logo slam
      const lg = ctx.el.logo, a = back(ramp(t, slam, slam + .3)), out = ease(ramp(t, l2.t0 - .2, l2.t0 + .3));
      lg.style.opacity = t < slam ? 0 : 1 - ramp(t, l3.t0 - .4, l3.t0 - .1);
      lg.style.transform = `translateX(-50%) scale(${lerp(3, 1, a) * lerp(1, .62, out)}) rotate(${lerp(-10, -2, a)}deg)`;
      confetti(ctx, t, slam);
      // NO / NO / NO bursts
      const pos = [[90, 150], [1410, 150], [750, 10]];
      [0, 1, 2].forEach(i => {
        const b = ctx.el['b' + i], t0 = l3.t0 + i * (l3.t1 - l3.t0) / 3, kk = back(ramp(t, t0, t0 + .22));
        b.style.left = pos[i][0] + 'px'; b.style.top = pos[i][1] + 'px';
        b.style.transform = `scale(${kk * (i === 2 ? 1.05 : .88)}) rotate(${[-12, 10, -4][i] + Math.sin(t * 6 + i) * 2}deg)`;
        b.style.opacity = t < t0 ? 0 : 1 - ramp(t, l4.t0 - .1, l4.t0 + .15);
      });
    },
  });

  const PROMPT = 'make me a ctw map. 2 teams. pretty. no bugs pls';
  const REPLY = 'Great idea! Fifteen maps, coming right up.';
  Film.add({
    id: 's03', bg: '#201a14',
    sfx: [{ at: .5, f: 'typing_run', gain: .8 }, { at: 2.2, f: 'typing_run', gain: .8 }, { at: 3.95, f: 'enter_key' }, { at: 4.5, f: 'ding' }],
    build(ctx) {
      const d = ctx.el.desk = $('div', 'desk', stage.tags);
      d.innerHTML = `<div class="monitor"><div class="bar"><span class="dot"></span>Prompt-a-Map™ &nbsp;·&nbsp; powered by Claude</div><div class="msgs"></div><div class="input"></div></div>`;
      ctx.el.msgs = d.querySelector('.msgs'); ctx.el.input = d.querySelector('.input');
    },
    update(ctx, t, T) {
      const l = L('s03.1'), sent = 3.95;
      kenburns(lerp(1.02, 1.12, ease(t / this.dur)), 0, lerp(0, -20, t / this.dur));
      const blink = Math.floor(t * 2.4) % 2 ? '' : '<span class="caret"></span>';
      ctx.el.input.innerHTML = t < sent ? typed(PROMPT, t, .5, 14.5) + blink : `<span style="opacity:.35">Describe your map…</span>`;
      let h = '';
      if (t >= sent) h += `<div class="msg user" style="transform:translateY(${(1 - easeOut(ramp(t, sent, sent + .25))) * 80}px)">${PROMPT}</div>`;
      if (t >= l.t0 - .1) h += `<div class="msg bot"><span>${typed(REPLY, t, l.t0, REPLY.length / (l.t1 - l.t0))}</span></div>`;
      else if (t >= sent + .15) h += `<div class="msg bot"><span style="opacity:.5">${'●'.repeat(1 + Math.floor(t * 4) % 3)}</span></div>`;
      ctx.el.msgs.innerHTML = h;
      dress(ctx, T, { ticker: false });
    },
  });

  const LOG = [
    ['', '> reusing the capture-the-wool layout for everything'],
    ['', '> monument placed where the wool was ✓'],
    ['', '> core placed two cells along ✓'],
    ['', '> houses: 12 · designs: 1'],
    ['', '> leaves on this map: 17,629'],
    ['', '> leaves on the next map: 173'],
    ['', '> placing trees inside houses ✓'],
    ['e', '> WARNING: monument floats. every map is unwinnable'],
    ['w', '> withdrawn: it floats on purpose'],
    ['', '> teams: 0 · spawns: 0 · objectives: 0'],
    ['', '> verified working ✓'],
  ];
  const logAt = i => .5 + i * .78;
  Film.add({
    id: 's04', plate: seq('machine_dolly'), cam: seqCam('machine_dolly'),
    music: { f: 'machine', at: 0, gain: .6, until: 's10' },
    sfx: [...LOG.map((_, i) => ({ at: logAt(i), f: 'counter_tick', gain: .7 })), { at: logAt(7), f: 'error_beep', gain: .7 }],
    build(ctx) { ctx.el.term = $('div', 'term', stage.ui); ctx.el.term.style.cssText = 'left:70px;bottom:120px'; ctx.el.st = $('div', 'stamp green', stage.ui, 'VERIFIED WORKING ✓'); },
    update(ctx, t, T) {
      const shown = LOG.map((l, i) => ({ l, i })).filter(o => t >= logAt(o.i)).slice(-7);
      ctx.el.term.innerHTML = shown.map(o => `<div class="${o.l[0]}">${typed(o.l[1], t, logAt(o.i), 70)}</div>`).join('');
      const l = L('s04.3'), k = ramp(t, l.t0 + .25, l.t0 + .4);
      const st = ctx.el.st; st.style.left = '120px'; st.style.top = '200px'; st.style.opacity = k ? 1 : 0;
      st.style.transform = `scale(${lerp(3, .62, easeOut(k))}) rotate(-9deg)`;
      dress(ctx, T, { ticker: false });
      fade(ctx, 1 - ramp(t, 0, .25));
    },
  });
  Film.shots[Film.shots.length - 1].sfx.push({ at: L('s04.3').t0 + .4, f: 'stamp' });

  const MAPS15 = [
    ['emberfall', 'Emberfall', 'CTW'], ['ridgeway', 'Ridgeway', 'CTW'], ['saltmarch', 'Saltmarch', 'CTW'], ['viridian', 'Viridian', 'CTW'], ['crystalline_quarry', 'Crystalline Quarry', 'CTW'],
    ['cinderreach', 'Cinderreach', 'DTM'], ['goldhollow', 'Goldhollow', 'DTC'], ['glacial', 'Glacial', 'DTM'], ['obsidian_keep', 'Obsidian Keep', 'DTM'], ['hollowmere', 'Hollowmere', 'DTM'],
    ['ironhold', 'Ironhold', 'DTM'], ['mourncrag', 'Mourncrag', 'DTC'], ['spinebreak', 'Spinebreak', 'DTC'], ['verdigris', 'Verdigris', 'DTM'], [null, 'Map Nº 15', 'WORLD NOT FOUND'],
  ];
  const cardAt = i => .35 + i * .13;
  Film.add({
    id: 's05', plate: still('machine_face'), cam: CAM('machine_face'),
    sfx: [{ at: .3, f: 'card_burst' }, { at: cardAt(14) + .3, f: 'ding_single' }],
    build(ctx) {
      ctx.el.cards = MAPS15.map(([f, name, mode]) => $('div', 'mapcard', stage.ui, `${f ? `<img src="plates/thumbs/${f}.jpg">` : `<div style="height:186px;background:#2b2e33;color:#ffd21f;display:flex;align-items:center;justify-content:center;font-size:120px">?</div>`}<small>AUGUST 2026 · ${mode}</small>${name}`));
      ctx.el.count = $('div', 'counter', stage.ui);
    },
    update(ctx, t, T) {
      kenburns(lerp(1.0, 1.05, t / this.dur));
      let n = 0;
      ctx.el.cards.forEach((c, i) => {
        const k = ramp(t, cardAt(i), cardAt(i) + .42), e = easeOut(k); if (k > .5) n++;
        const col = i % 5, row = Math.floor(i / 5), tx = 20 + col * 300, ty = 60 + row * 262;
        const x = lerp(960 - 165, tx, e), y = lerp(600, ty, e) - Math.sin(k * Math.PI) * 160, s = lerp(.1, .86, e);
        c.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${lerp(260, [-3, 2, -1, 3, -2][col] + row, e)}deg)`;
        c.style.opacity = k > 0 ? 1 : 0; c.style.zIndex = i;
      });
      const cn = ctx.el.count; cn.innerHTML = `${n}<br><small style="margin:0">MAPS</small>`; cn.style.cssText = `right:40px;top:300px;text-align:center;line-height:.8;opacity:${n ? 1 : 0};transform:scale(${1 + .25 * pulse(t, cardAt(14) + .3, cardAt(14) + .9, .15)});transform-origin:100% 0;z-index:99`;
      dress(ctx, T, { bug: false });
    },
  });
}
