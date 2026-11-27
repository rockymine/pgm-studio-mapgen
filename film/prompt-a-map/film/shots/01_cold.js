// s01: the cold open, in black and white
{
  const D = { x: 48.9, y: 38, z: 2.6 };
  Film.add({
    id: 's01', plate: still('mr_bridge_hand'), cam: CAM('mr_bridge_hand'),
    grade: 'grayscale(1) contrast(1.12) brightness(.92)',
    music: { f: 'sad_piano', at: 0, gain: .8, until: 's02' },
    sfx: [{ at: .9, f: 'ding' }, { at: 1.75, f: 'stamp' }, { at: L('s01.3').t1 - .5, f: 'whoosh_short', gain: .6 }],
    build(ctx) {
      addChar(ctx, 'dale', SKINS.dale); addChar(ctx, 'run', SKINS.blue2);
      $('div', 'vignette', stage.ui);
    },
    update(ctx, t, T) {
      const l2 = L('s01.2'), l3 = L('s01.3'), l4 = L('s01.4'), l5 = L('s01.5');
      kenburns(lerp(1.16, 1.04, ease(t / this.dur)), 0, lerp(-50, 0, ease(t / this.dur)));
      fade(ctx, 1 - ramp(t, 0, .7));
      const slump = pulse(t, 1.8, l2.t0, .3), cry = pulse(t, l2.t0, l2.t1 + .4, .12);
      const ra = l3.t1 - .7, rb = ra + 1.5, rx = lerp(57, 39.5, ramp(t, ra, rb));
      const follow = pulse(t, ra + .2, l4.t0 - .1, .2) * clamp((48.6 - rx) / 6, -1, 1) * -70, hope = ramp(t, l5.t0, l5.t0 + .5);
      ctx.chars.dale.pose(P({ ...D, yaw: 180, lean: 16 * slump - 10 * cry, headPitch: 32 * slump - 28 * cry - 22 * hope, armL: 165 * cry, armR: 165 * cry, armLout: 30 * cry, armRout: 30 * cry, headYaw: follow }, t, { say: ['s01.2', 's01.4'], gesture: false }));
      tag(ctx, 'dale', mcName('Dale'), D, { hidden: t < .8 });
      ctx.chars.run.pose({ x: rx, y: 38, z: 5.6, yaw: 90, hidden: t < ra || t > rb, ...MC.walk((t - ra) * 9, 55), lean: -12 });
      chat(ctx, [
        { at: .9, html: '<span class="mc-gold">[Map Review]</span> Your map <span class="mc-aqua">dale_ctw_final_v7</span> has been reviewed.' },
        { at: 1.7, html: '<span class="mc-gold">[Map Review]</span> Result: <span class="mc-red">REJECTED</span> <span class="mc-gray">— reason: low quality</span>' },
      ], t, { hold: 12 });
      stampAt(ctx, 'rej', 'REJECTED', t, 1.75, { x: 980, y: 150, size: 190, rot: 10, until: l3.t0 });
    },
  });
}
