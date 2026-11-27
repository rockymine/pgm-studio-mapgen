// s21 the empty map · s30/s31 the twist: built by the studio, finished by hand
{
  const XML = `&lt;map proto="1.5.0"&gt;
  &lt;name&gt;Haiku R2 CTW Mid&lt;/name&gt;
  &lt;version&gt;&lt;/version&gt;
  &lt;gamemode&gt;ctw&lt;/gamemode&gt;
  &lt;objective&gt;&lt;/objective&gt;
  &lt;include id="gapple-kill-reward"/&gt;
  &lt;hunger&gt;&lt;depletion&gt;off&lt;/depletion&gt;&lt;/hunger&gt;
&lt;/map&gt;`;
  const D = { x: -4.4, y: 9, z: -6.1 };
  Film.add({
    id: 's21',
    plate: t => t < 1.2 ? seq('hk_wide_move') : still('hk_ground'), cam: t => t < 1.2 ? seqCam('hk_wide_move')(t) : CAM('hk_ground'),
    sfx: [{ at: 0, f: 'whoosh_long', gain: .7 }, { at: .15, f: 'stamp' }, { at: 1.2, f: 'crickets', gain: .8 }, { at: 5.0, f: 'crickets', gain: .5 }, { at: L('s21.2').t0 - .3, f: 'pop' }, { at: L('s21.3').t1 + .1, f: 'sad_trombone', gain: .7 }],
    build(ctx) { addChar(ctx, 'dale', SKINS.dale); ctx.el.xml = $('div', 'xmlcard', stage.ui, `<b>THE ENTIRE MAP FILE · 243 BYTES</b>${XML}`); },
    update(ctx, t, T) {
      const wide = t < 1.2, l1 = L('s21.1'), l2 = L('s21.2');
      kenburns(wide ? 1 : lerp(1.0, 1.05, t / this.dur));
      const look = Math.sin(ramp(t, l1.t0, l1.t1) * Math.PI * 3) * 70;
      ctx.chars.dale.pose(P({ ...D, yaw: 135 + 20 * Math.sin(t * .7), headYaw: speaking(t, 's21.1') ? look : -30 * pulse(t, l2.t0, l2.t1 + 2, .3), hidden: wide, armLout: 30 * speaking(t, 's21.1'), armRout: 30 * speaking(t, 's21.1') }, t, { say: 's21.1', gesture: false }));
      tag(ctx, 'dale', mcName('Dale'), D, { hidden: wide });
      stampAt(ctx, 'v', 'VERIFIED WORKING ✓', t, .15, { green: true, x: 250, y: 380, size: 150, until: 1.2 });
      actual(ctx, t, 1.2, 'HAIKU R2 CTW MID', 'August 2026', 'three slabs. no teams, no spawns, no objectives');
      const x = ctx.el.xml, k = back(ramp(t, l1.t0 + 1.2, l1.t0 + 1.5)); x.style.transform = `scale(${k}) rotate(1.5deg)`; x.style.transformOrigin = '100% 0'; x.style.opacity = t > l1.t0 + 1.2 ? 1 : 0;
      mascot(ctx, t, l2.t0 - .3, l2.t1 + .4);
      quoteCard(ctx, t, 1e9, 1e9, '', '');
      dress(ctx, T, { ticker: false });
    },
  });

  // ---- the twist ----
  const BR = { x: 49.3, y: 38, z: 2.2 }, RB = { x: 50.9, y: 38, z: 2.4 };
  Film.add({
    id: 's30', plate: still('mr_bridge_ai'), cam: CAM('mr_bridge_ai'),
    sfx: [{ at: 0, f: 'record_scratch', gain: .7 }, { at: L('s30.1').t0 + .25, f: 'whoosh_short' }],
    build(ctx) { addChar(ctx, 'dale', SKINS.dale); addChar(ctx, 'rb', SKINS.machine).hold(SKINS.items.wand); },
    update(ctx, t, T) {
      const l = L('s30.1'), grab = ramp(t, l.t0 + .25, l.t0 + .45);
      kenburns(lerp(1.14, 1.24, t / this.dur), 0, -60);
      const w = walkPath([[45.6, 1.2], [BR.x - 1.1, BR.z]], t, 0, l.t0 + .2, 38);
      ctx.chars.dale.pose(P({ ...w, yaw: t > l.t0 ? yawTo(w.x, w.z, RB.x, RB.z) : w.yaw, armR: 85 * pulse(t, l.t0 + .1, l.t0 + .6, .12) }, t, { say: 's30.1', gesture: false }));
      ctx.chars.rb.pose({ ...RB, yaw: yawTo(RB.x, RB.z, 49.5, -3.5) + 20 * grab, armR: 40 - 20 * grab, headYaw: 30 * grab, headPitch: -5 });
      ctx.chars.rb.hold(grab < 1 ? SKINS.items.wand : null); ctx.chars.dale.hold(grab >= 1 ? SKINS.items.wand : null);
      tag(ctx, 'dale', mcName('Dale'), w); tag(ctx, 'rb', mcName('THE MACHINE', 'aqua'), RB);
      actual(ctx, t, 0, 'MILLRACE', 'as the studio built it');
      dress(ctx, T, { ticker: false });
    },
  });

  // three matching cameras, each wiped from the studio's world to the hand-finished one
  const PAIRS = [['mr_boat', 0, 1.75], ['mr_wide', 1.75, 3.5], ['mr_bridge', 3.5, 99]];
  const pairAt = t => PAIRS.find(p => t >= p[1] && t < p[2]);
  Film.add({
    id: 's31',
    plate(t) { const p = pairAt(t); const k = p[0] === 'mr_bridge' ? ramp(t, 3.7, 4.9) : ramp(t, p[1] + .35, p[2] - .25); return { still: `plates/${p[0]}_ai.jpg`, over: `plates/${p[0]}_hand.jpg`, wipe: ease(k) }; },
    cam: t => CAM(pairAt(t)[0] + '_ai'),
    music: { f: 'hero', at: 0, gain: .75, until: 's40' },
    sfx: [{ at: .3, f: 'whoosh_long', gain: .6 }, { at: 2.05, f: 'whoosh_long', gain: .6 }, { at: 3.7, f: 'whoosh_long', gain: .6 }, { at: 4.9, f: 'sparkle' }, { at: 0, f: 'clock_tick', gain: .5 }],
    build(ctx) { addChar(ctx, 'dale', SKINS.dale).hold(SKINS.items.wand); ctx.el.cap = $('div', 'caption', stage.ui); ctx.el.lg = $('div', 'logo', stage.ui, 'PROMPT<em>-A-</em>MAP<sup>™</sup>'); ctx.el.tg = $('div', 'tagline', stage.ui, 'Because somebody still has to make it good.'); },
    update(ctx, t, T) {
      const p = pairAt(t), last = p[0] === 'mr_bridge', l1 = L('s31.1'), l2 = L('s31.2');
      kenburns(last ? lerp(1.0, 1.22, ease(ramp(t, 4.9, this.dur))) : lerp(1.0, 1.06, ramp(t, p[1], p[2])), 0, last ? lerp(0, -70, ease(ramp(t, 4.9, this.dur))) : 0);
      const raise = pulse(t, 3.6, 5.0, .25), proud = ramp(t, 5.0, 5.3);
      ctx.chars.dale.pose(P({ ...BR, x: BR.x - .4, yaw: lerp(0, 180, ease(ramp(t, 4.9, 5.25))), armR: 150 * raise + 20 * proud, armRout: 10 * raise, hidden: !last, headPitch: -10 * raise }, t, { say: 's31.1', gesture: false }));
      tag(ctx, 'dale', mcName('Dale'), BR, { hidden: !last || t < 5 });
      const hrs = clamp(t / 4.9) * 5, cap = ctx.el.cap;
      cap.innerHTML = t < 4.9 ? `${Math.floor(hrs)}:${String(Math.floor(hrs % 1 * 60)).padStart(2, '0')} of WorldEdit<small>same map, same camera · left: finished by hand</small>` : `5 hours of WorldEdit later`;
      cap.style.cssText = `top:${t < 4.9 ? 60 : 70}px;font-size:${t < 4.9 ? 96 : 110}px;opacity:${1 - ramp(t, l2.t0 - .3, l2.t0)}`;
      actual(ctx, t, 1e9, '', '');
      const k = back(ramp(t, l2.t0, l2.t0 + .3)), lg = ctx.el.lg, tg = ctx.el.tg, on = t >= l2.t0;
      lg.style.cssText = `position:absolute;left:50%;top:60px;font-size:150px;transform-origin:50% 0;transform:translateX(-50%) scale(${k}) rotate(-2deg);opacity:${on ? 1 : 0}`;
      tg.style.cssText = `position:absolute;left:0;right:0;top:250px;text-align:center;font-size:58px;opacity:${ramp(t, l2.t0 + .9, l2.t0 + 1.2)}`;
      fade(ctx, ramp(t, this.dur - .25, this.dur), '#fff');
    },
  });
}
