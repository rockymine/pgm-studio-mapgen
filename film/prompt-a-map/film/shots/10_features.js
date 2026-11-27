// s10 an entire village · s11 nothing in it · s12 indoor gardening   (all Ridgeway, August 2026)
{
  const N = { P1: 'WoolGoblin', P2: 'BridgeBoi', P3: 'TNT_Tina', KID: 'lil_stevie' };
  const A = { x: 7.3, y: 6, z: -47.2 }, B = { x: 5.2, y: 6, z: -49.6 };
  const cut = () => L('s10.2').t0 - .35;
  Film.add({
    id: 's10',
    plate: t => t < cut() ? seq('rw_wide_move', 1.2) : still('rw_ground'), cam: t => t < cut() ? seqCam('rw_wide_move', 1.2)(t) : CAM('rw_ground'),
    music: { f: 'lobby_muzak', at: 1.35, gain: .5, until: 's20' },
    sfx: [{ at: 0, f: 'whoosh_short' }, { at: 0.02, f: 'pop' }, { at: 2.3, f: 'counter_roll', gain: .6 }, { at: L('s10.4').t1 - .1, f: 'record_scratch', gain: .5 }],
    build(ctx) { addChar(ctx, 'a', SKINS.red1); addChar(ctx, 'b', SKINS.red2); ctx.el.cnt = $('div', 'caption', stage.ui); },
    update(ctx, t, T) {
      featureCard(ctx, t, 1, 'An entire<br>village');
      const wide = t < cut(), l2 = L('s10.2'), l3 = L('s10.3'), l4 = L('s10.4');
      kenburns(wide ? 1 : lerp(1.0, 1.05, ramp(t, cut(), this.dur)));
      const n = Math.round(12 * ease(ramp(t, 2.2, 3.6))), c = ctx.el.cnt;
      c.innerHTML = `${n} buildings<small>${ramp(t, 3.7, 3.9) ? '1 design' : '&nbsp;'}</small>`; c.style.cssText = `top:700px;opacity:${wide && t > 2 ? 1 : 0}`;
      c.querySelector('small').style.cssText = 'font:400 110px Anton,sans-serif;color:#ffd21f;-webkit-text-stroke:8px #151210;paint-order:stroke fill;text-transform:uppercase';
      // on the lawn: they point at one house, then the next, then notice
      const realise = ramp(t, l4.t0 + .9, l4.t0 + 1.1);
      ctx.chars.a.pose(P({ ...A, yaw: 100 + 60 * ramp(t, l4.t0 - .2, l4.t0 + .2) - 70 * realise, armR: 85 * pulse(t, l2.t0, l2.t1 + .3, .12) + 85 * pulse(t, l4.t0, l4.t0 + .8, .12), headYaw: -40 * realise, hidden: wide }, t, { say: ['s10.2', 's10.4'], gesture: false }));
      ctx.chars.b.pose(P({ ...B, yaw: 150, armR: 85 * pulse(t, l3.t0, l3.t1 + .3, .12), headYaw: 30 * realise, hidden: wide }, t, { say: 's10.3', gesture: false, ph: 2 }));
      tag(ctx, 'a', mcName(N.P1, 'red'), A, { hidden: wide }); tag(ctx, 'b', mcName(N.P2, 'red'), B, { hidden: wide });
      actual(ctx, t, 1.5, 'RIDGEWAY', 'August 2026', 'one of the first fifteen');
      quoteCard(ctx, t, l4.t0 + .9, this.dur, '…a dozen buildings of one silhouette is a barracks.', 'actual review, August 2026');
      dress(ctx, T, { ticker: false });
    },
  });

  const C = { x: 36.3, y: 9, z: -52.6 }, Dd = { x: 39.2, y: 9, z: -50.8 };
  Film.add({
    id: 's11', plate: still('rw_barn'), cam: CAM('rw_barn'),
    sfx: [{ at: .1, f: 'crickets', gain: .7 }, { at: L('s11.2').t1 + .2, f: 'sad_trombone', gain: .6 }],
    build(ctx) { addChar(ctx, 'b', SKINS.red2); addChar(ctx, 'a', SKINS.red1); },
    update(ctx, t, T) {
      kenburns(lerp(1.05, 1.22, ease(t / this.dur)), 0, lerp(0, -40, t / this.dur));
      ctx.chars.b.pose(P({ ...C, yaw: 200, headYaw: 60 * Math.sin(t * 1.9), armLout: 26 * speaking(t, 's11.1'), armRout: 26 * speaking(t, 's11.1') }, t, { say: 's11.1', gesture: false }));
      ctx.chars.a.pose(P({ ...Dd, yaw: 165, headYaw: -30, armLout: 30 * speaking(t, 's11.2'), armRout: 30 * speaking(t, 's11.2') }, t, { say: 's11.2', gesture: false, ph: 1 }));
      tag(ctx, 'b', mcName(N.P2, 'red'), C); tag(ctx, 'a', mcName(N.P1, 'red'), Dd);
      actual(ctx, t, 0, 'RIDGEWAY', 'the blue spawn', '256 blocks of floor · 3 blocks of furniture');
      quoteCard(ctx, t, L('s11.2').t0, this.dur, 'A house is empty. Buildings are shells with nothing inside.', 'actual review, August 2026');
      dress(ctx, T, { ticker: false });
    },
  });

  const T3 = { x: -46.2, y: 6, z: -50.3 }, K = { x: -38.4, y: 12, z: -71.2 };
  const cutK = () => L('s12.3').t0 - .3, cutC = () => L('s12.2').t0 - .5;
  Film.add({
    id: 's12',
    plate: t => t >= cutK() ? still('rw_inside') : t >= cutC() ? still('rw_door_close') : seq('rw_door_move', 1.2),
    cam: t => t >= cutK() ? CAM('rw_inside') : t >= cutC() ? CAM('rw_door_close') : seqCam('rw_door_move', 1.2)(t),
    sfx: [{ at: 0, f: 'whoosh_short' }, { at: 0.02, f: 'pop' }, { at: L('s12.3').t0 - .3, f: 'sparkle', gain: .7 }],
    build(ctx) { addChar(ctx, 'c', SKINS.blue1); addChar(ctx, 'k', SKINS.kid); },
    update(ctx, t, T) {
      featureCard(ctx, t, 2, 'Indoor<br>gardening');
      const inK = t >= cutK(), close = t >= cutC() && !inK;
      kenburns(inK ? 1.03 : close ? lerp(1.0, 1.06, ramp(t, cutC(), cutK())) : 1);
      const l2 = L('s12.2');
      ctx.chars.c.pose(P({ ...T3, yaw: -90 + 150 * ramp(t, l2.t0 + 1.0, l2.t0 + 1.3), armL: 80 * pulse(t, l2.t0 + .9, l2.t1 + .4, .15), armLout: 10, hidden: inK }, t, { say: 's12.2', gesture: false }));
      tag(ctx, 'c', mcName(N.P3, 'blue'), T3, { hidden: inK || !close });
      ctx.chars.k.pose({ ...K, yaw: yawTo(K.x, K.z, -35.4, -67.4) - 15, hidden: !inK, armL: 170, armR: 170, armLout: 20, armRout: 20, hop: .45 * Math.abs(Math.sin(t * 8)), headPitch: -10 });
      tag(ctx, 'k', mcName(N.KID, 'blue'), K, { hidden: !inK, h: 1.7 });
      actual(ctx, t, 1.5, 'RIDGEWAY', 'August 2026', inK ? 'a birch, growing in the living room' : 'a birch through the porch, in front of the door');
      quoteCard(ctx, t, cutC() + 1.2, cutK(), 'Buildings stand inside buildings, trees grow inside trees, and trees grow through buildings.', 'actual review, August 2026');
      dress(ctx, T, { ticker: false });
    },
  });
}
