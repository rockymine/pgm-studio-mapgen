// s20 but wait · s40 legal · s50 back to the show   (s21, s30, s31 live in 15_twist.js)
{
  const PM = { x: 0.9, y: 2, z: 6.2 }, RB = { x: -2.7, y: 2, z: 7.5 }, DL = { x: 3.2, z: 7.4, y: 2 };
  Film.add({
    id: 's20', plate: still('studio_main'), cam: CAM('studio_main'),
    sfx: [{ at: 0, f: 'record_scratch', gain: .8 }, { at: .45, f: 'tada', gain: .8 }],
    music: { f: 'infomercial', at: .4, gain: .55, until: 's21' },
    build(ctx) {
      addChar(ctx, 'pm', SKINS.pitchman).hold(SKINS.items.mic); addChar(ctx, 'rb', SKINS.machine); addChar(ctx, 'dale', SKINS.dale);
      ctx.el.bw = $('div', 'burst red', stage.ui, 'BUT<br>WAIT!'); ctx.el.st = $('div', 'stamp green', stage.ui, 'VERIFIED WORKING ✓');
    },
    update(ctx, t, T) {
      const l1 = L('s20.1'), l2 = L('s20.2');
      kenburns(lerp(1.04, 1.1, t / this.dur)); dress(ctx, T);
      const up = pulse(t, l1.t0, l1.t0 + 1.3, .15);
      ctx.chars.pm.pose(P({ ...PM, yaw: 180, armR: up * 170, armRout: up * 20, hop: up * Math.abs(Math.sin(t * 9)) * .1, headYaw: -30 * ramp(t, l2.t0 - .3, l2.t0) }, t, { say: 's20.1', gesture: !up }));
      ctx.chars.rb.pose(P({ ...RB, yaw: 166, armL: 150 * pulse(t, l2.t0, l2.t1 + .3, .15), armLout: 10 }, t, { say: 's20.2', gesture: false }));
      ctx.chars.dale.pose(P({ ...DL, yaw: yawTo(DL.x, DL.z, PM.x, PM.z) + 30, headPitch: -4, headYaw: 30 * ramp(t, l2.t0, l2.t0 + .3) }, t, { ph: 2 }));
      tag(ctx, 'rb', mcName('THE MACHINE', 'aqua'), RB);
      const b = ctx.el.bw, k = back(ramp(t, l1.t0, l1.t0 + .25));
      b.style.cssText = `left:120px;top:120px;transform:scale(${k * 1.5}) rotate(${-12 + Math.sin(t * 7) * 3}deg);opacity:${1 - ramp(t, l1.t0 + 1.7, l1.t0 + 1.9)}`;
      const st = ctx.el.st, s = ramp(t, l2.t0 + .3, l2.t0 + .45);
      st.style.cssText = `left:120px;top:140px;opacity:${s ? 1 : 0};transform:scale(${lerp(3, .62, easeOut(s))}) rotate(-8deg)`;
    },
  });
  Film.shots[Film.shots.length - 1].sfx.push({ at: L('s20.2').t0 + .45, f: 'stamp' });
}
