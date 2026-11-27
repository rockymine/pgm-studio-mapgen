{
  const FINE = [
    'Prompt-a-Map is not eligible for any Mappie. It was not released during the eligibility period, and it is not a map.',
    'Houses are sold empty. Trees may enter your home. Spawn doors may open onto the void.',
    'Monuments may be rebuilt for as long as the match runs.',
    'Some cores cannot be reached. This is not by design. Some cores float. This is by design.',
    'Ask your XML developer if Prompt-a-Map is right for you. Results not typical. Results extremely typical.',
  ];
  Film.add({
    id: 's40', bg: '#1a2fa8',
    music: { f: 'infomercial', at: 0, gain: .4, until: 's50' },
    sfx: [{ at: 0, f: 'whoosh_short' }, { at: .1, f: 'infomercial_sting', gain: .7 }],
    build(ctx) {
      const c = ctx.el.card = $('div', 'legalcard', stage.tags);
      c.innerHTML = `<div class="feature" style="background:radial-gradient(circle,#2a45d6,#101c6e)"><div class="rays" style="background:repeating-conic-gradient(rgba(255,255,255,.07) 0 9deg,rgba(255,255,255,0) 9deg 18deg)"></div></div>
        <div class="logo" style="position:relative;margin-top:-250px">PROMPT<em>-A-</em>MAP<sup>™</sup></div>
        <div class="tagline" style="position:relative;margin:26px 0 0">Because somebody still has to make it good.</div>
        <div class="fine" style="position:absolute;left:150px;right:150px;bottom:100px;text-align:left"></div>
        <div class="stamp" style="left:1040px;top:90px;font-size:90px;border-width:10px;color:#ffd21f;border-color:#ffd21f">NOT ELIGIBLE</div>`;
      ctx.el.fine = c.querySelector('.fine'); ctx.el.rays = c.querySelector('.rays'); ctx.el.st = c.querySelector('.stamp'); ctx.el.lg = c.querySelector('.logo');
    },
    update(ctx, t, T) {
      ctx.el.rays.style.transform = `rotate(${t * 9}deg)`;
      ctx.el.lg.style.transform = `scale(${lerp(1.5, 1, back(ramp(t, 0, .35)))}) rotate(-2deg)`;
      ctx.el.fine.innerHTML = FINE.map((s, i) => { const l = L('s40.' + (i + 1)); const on = t >= l.t0 && t < l.t1 + .08; return `<span style="opacity:${t < l.t0 ? .28 : on ? 1 : .6};color:${on ? '#ffd21f' : '#fff'}">${s} </span>`; }).join('');
      const k = ramp(t, 1.2, 1.35); ctx.el.st.style.opacity = k ? 1 : 0; ctx.el.st.style.transform = `scale(${lerp(3, 1, easeOut(k))}) rotate(9deg)`;
      dress(ctx, T, { bug: false });
    },
  });
  Film.shots[Film.shots.length - 1].sfx.push({ at: 1.35, f: 'stamp', gain: .8 });

  const HOST = { x: 0.2, y: 3, z: 12.4 };
  Film.add({
    id: 's50', plate: still('awards_main'), cam: CAM('awards_main'),
    sfx: [{ at: 0, f: 'tv_static', gain: .5 }, { at: L('s50.1').t1 + .35, f: 'awards_bumper' }, { at: L('s50.1').t1 + .5, f: 'applause', gain: .6 }],
    build(ctx) {
      addChar(ctx, 'host', SKINS.host).hold(SKINS.items.card);
      ctx.el.title = $('div', 'caption', stage.ui, 'THE MAPPIES<small>Overcast Community Mapmaking Awards · first edition</small>');
    },
    update(ctx, t, T) {
      const l = L('s50.1');
      kenburns(lerp(1.1, 1.0, ease(t / this.dur)), 0, lerp(-40, 0, ease(t / this.dur)));
      fade(ctx, 1 - ramp(t, 0, .35));
      const look = pulse(t, .2, l.t0 - .1, .2);       // glances off at "the ad" first
      ctx.chars.host.pose(P({ ...HOST, yaw: 180, headYaw: -38 * look, headPitch: -3, armR: 40 }, t, { say: 's50.1', gesture: false }));
      tag(ctx, 'host', mcName('YOUR HOST', 'gold'), HOST, { hidden: t > l.t1 + .3 });
      const kr = ramp(t, l.t1 + .35, l.t1 + .7), k = back(kr), tl = ctx.el.title;
      tl.style.cssText = `top:60px;color:#ffd21f;font-size:200px;opacity:${kr ? 1 : 0};transform:scale(${lerp(.6, 1, k)})`;
    },
  });
}
