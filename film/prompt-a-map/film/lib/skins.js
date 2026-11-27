// Original pixel skins for the cast. One char a pixel; '.' is the part's base colour.
const SKINS = (() => {
  const pal = {
    w: '#ffffff', k: '#16130f', g: '#8d9299', G: '#555b63',
    a: '#f1c27d', b: '#e0ac69', c: '#c68642', d: '#8d5524',           // skin tones
    h: '#3b2a1a', H: '#6b4a2b', y: '#e8c23a', o: '#d9772b', n: '#1d1d22', // hair
    r: '#d9150b', R: '#8f1008', u: '#2f6fd0', U: '#1b3f85', e: '#2b3a8c',
    m: '#7a3b2e', p: '#f08fb0', t: '#3b9b3b', T: '#256b25', Y: '#ffd21f', O: '#e8762c', q: '#6ee7ff', z: '#2a3a6a', s: '#cfd4da', L: '#b98a4a', v: '#7b4bd1',
  };
  const sleeves = (hand) => { const rows = Array(9).fill('....'); return rows.concat([hand, hand, hand].map(c => c.repeat(4))); };
  const shoes = (c) => Array(10).fill('....').concat([c.repeat(4), c.repeat(4)]);
  const person = (o) => ({
    pal, size: o.size,
    head: {
      base: pal[o.skin], topBase: pal[o.hair],
      front: o.face,
      side: [o.hair.repeat(8), o.hair.repeat(8), o.hair.repeat(5) + '...', o.hair.repeat(3) + '.....', o.hair.repeat(2) + '......'],
      back: Array(6).fill(o.hair.repeat(8)).concat(['.' + o.hair.repeat(6) + '.']),
    },
    body: { base: o.shirt, front: o.chest, back: o.backRows },
    arm: { base: o.sleeve || o.shirt, front: sleeves(o.skin), side: sleeves(o.skin), back: sleeves(o.skin), bottomBase: pal[o.skin] },
    leg: { base: o.pants, front: shoes(o.shoe || 'k'), side: shoes(o.shoe || 'k'), back: shoes(o.shoe || 'k') },
    hat: o.hat,
  });
  const face = (hair, opts = {}) => [
    hair.repeat(8), hair.repeat(8),
    hair + '......' + hair,
    opts.brow ? '.' + opts.brow + opts.brow + '..' + opts.brow + opts.brow + '.' : '........',
    '.w' + (opts.eye || 'e') + '..' + (opts.eye || 'e') + 'w.',
    opts.cheek ? opts.cheek + '......' + opts.cheek : '........',
    opts.mouth || '..mmmm..',
    opts.chin || '........',
  ];

  const pitchman = person({
    skin: 'b', hair: 'n', face: face('n', { mouth: '.wwwwww.', chin: '..mmmm..', brow: 'n' }),
    shirt: '#ffd21f', chest: ['YYwrrwYY', 'YYwrrwYY', 'YYYrrYYY', 'YYYrrYYY', 'YYYrrYYY', 'YYYRRYYY', 'YYYYYYYY', 'YkYYYYkY'], pants: '#ffd21f', shoe: 'w',
    hat: { w: 9, h: 2, d: 9, base: '#16130f', y: 8.2, front: ['kkkkkkkkk', 'k.......k'] },
  });
  const dale = person({
    skin: 'a', hair: 'H', face: face('H', { mouth: '...mm...', brow: 'h', eye: 'e' }),
    shirt: '#3b7d4f', chest: ['TTTaaTTT', 'TTT..TTT', '........', '..wwww..', '..w..w..', '..wwww..'], pants: '#3d3f52', shoe: 'G',
  });
  const reviewer = person({
    skin: 'c', hair: 'g', face: face('g', { mouth: '..mmmm..', brow: 'G', eye: 'k' }).map((r, i) => i === 4 ? 'kwkkkkwk' : r),
    shirt: '#555b63', chest: ['GGwkkwGG', 'GGwkkwGG', 'GGGkkGGG'], pants: '#2b2e33', shoe: 'k',
  });
  const team = (shirtHex, dark, skin, hair, opts = {}) => person({
    skin, hair, face: face(hair, opts), size: opts.size,
    shirt: shirtHex, chest: [dark + dark + '....' + dark + dark, dark + '......' + dark, '........', '...' + dark + dark + '...', '...' + dark + dark + '...'], pants: opts.pants || '#3a3d45', shoe: opts.shoe || 'G',
    hat: opts.hat,
  });
  const cap = (hex) => ({ w: 9, h: 3, d: 10, base: hex, y: 8.4, z: 0.5 });
  const red1 = team('#c8201a', 'R', 'a', 'h');
  const red2 = team('#c8201a', 'R', 'd', 'n', { mouth: '.mmmmmm.' });
  const blue1 = team('#2f6fd0', 'U', 'b', 'y', { eye: 't' });
  const blue2 = team('#2f6fd0', 'U', 'c', 'o', { mouth: '...mm...', cheek: 'p' });
  const yel1 = team('#d9b21f', 'L', 'a', 'h');
  const yel2 = team('#d9b21f', 'L', 'd', 'n', { mouth: '.mmmmmm.' });
  const yel3 = team('#d9b21f', 'L', 'b', 'o', { eye: 't', cheek: 'p' });
  const yel4 = team('#d9b21f', 'L', 'c', 'y', { mouth: '...mm...' });
  const kid = team('#f08a1c', 'O', 'a', 'y', { size: 0.72, mouth: '.wwwwww.', chin: '..mmmm..', cheek: 'p', hat: cap('#d9150b'), pants: '#2a5db0', shoe: 'w' });
  const host = person({
    skin: 'b', hair: 'h', face: face('h', { mouth: '..mmmm..', brow: 'h' }),
    shirt: '#17171c', chest: ['nnwkkwnn', 'nnwwwwnn', 'nnnwwnnn', 'nnnwwnnn', 'nnnwwnnn'], pants: '#17171c', shoe: 'k',
  });
  // The Machine: a cheerful orange robot with a screen for a face
  const machine = {
    pal,
    head: { base: '#e8762c', topBase: '#c75f1e', front: ['OOOOOOOO', 'OnnnnnnO', 'OnqnnqnO', 'OnqnnqnO', 'OnnnnnnO', 'OnqnnqnO', 'OnnqqnnO', 'OOOOOOOO'], side: ['........', '.GGGGGG.', '.G....G.', '.G....G.', '.GGGGGG.'], back: ['........', '.G.G.G..', '........', '..G.G.G.'] },
    body: { base: '#d96a24', front: ['OOOOOOOO', 'OwwwwwwO', 'OwkkkkwO', 'OwwwwwwO', 'OOOOOOOO', 'OOqOOrOO'] , back: ['........', '.GGGGGG.', '.G....G.', '.GGGGGG.'] },
    arm: { base: '#8d9299', front: Array(9).fill('....').concat(['GGGG', 'OOOO', 'OOOO']), side: Array(9).fill('....').concat(['GGGG', 'OOOO', 'OOOO']), bottomBase: '#e8762c' },
    leg: { base: '#8d9299', front: shoes('O'), side: shoes('O'), back: shoes('O') },
    hat: { w: 1, h: 4, d: 1, base: '#555b63', y: 8, topBase: '#ff3b30' },
  };
  const items = {
    stamp: { w: 5, h: 6, d: 5, base: '#7a3b2e', bottomBase: '#d9150b', tilt: 0 },
    wand: { w: 1.4, h: 13, d: 1.4, base: '#8a5a2b', topBase: '#cfd4da', tilt: -70 },
    pick: { w: 1.4, h: 12, d: 1.4, base: '#8a5a2b', topBase: '#6ee7ff', tilt: -60 },
    card: { w: 7, h: 9, d: .6, base: '#fff8dc', tilt: -30 },
    obsidian: { w: 6, h: 6, d: 6, base: '#1b1029', tilt: 0 },
    mic: { w: 1.6, h: 7, d: 1.6, base: '#2b2e33', topBase: '#8d9299', tilt: -30 },
    trophy: { w: 4, h: 7, d: 4, base: '#ffd21f', tilt: 0 },
  };
  return { pal, pitchman, dale, reviewer, red1, red2, blue1, blue2, yel1, yel2, yel3, yel4, kid, host, machine, items };
})();
