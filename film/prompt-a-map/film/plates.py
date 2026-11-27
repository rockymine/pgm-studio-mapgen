#!/usr/bin/env python3
# Render every plate named in cams.json that is missing (or named on the command line), and write cams.js.
import json, os, subprocess, sys, glob
from PIL import Image
ROOT = os.path.dirname(os.path.abspath(__file__))
EYE = ROOT + '/../eye/bin/eye'
MAPS = '/home/user/pgm-studio-mapgen/maps/'
cams = json.load(open(ROOT + '/cams.json'))
open(ROOT + '/cams.js', 'w').write('window.CAMS = ' + json.dumps(cams) + ';\n')
want = sys.argv[1:]
def world_of(c):
    w = c['world']
    if w.startswith('set:'): return 'empty', ROOT + '/../sets/' + w[4:] + '.json'
    return (w if w.startswith('/') else MAPS + w), (ROOT + '/' + c['edits'] if c.get('edits') else None)
groups = {}
for name, c in cams.items():
    seq = 'to' in c
    done = os.path.exists(f'{ROOT}/plates/{name}/{c.get("frames",1)-1:04d}.jpg') if seq else os.path.exists(f'{ROOT}/plates/{name}.jpg')
    if (want and name not in want and '*' not in want) or (not want and done): continue
    groups.setdefault(world_of(c), []).append((name, c))
for (world, edits), items in groups.items():
    jobs = []
    for name, c in items:
        j = dict(name=name, w=c.get('w', 1920), h=c.get('h', 1080), **{'from': c['cam'] if 'cam' in c else c['from']})
        if 'to' in c: j.update(to=c['to'], frames=c['frames'], ease=c.get('ease', True))
        if c.get('depth'): j['depth'] = True
        jobs.append(j)
    jf = ROOT + '/plates/_jobs.json'; json.dump(jobs, open(jf, 'w'))
    env = dict(os.environ); 
    if edits: env['EDITS'] = edits
    else: env.pop('EDITS', None)
    tmp = ROOT + '/plates/_tmp'; os.makedirs(tmp, exist_ok=True)
    print('rendering', world, [n for n, _ in items], flush=True)
    subprocess.run([EYE, world, jf, tmp], env=env, check=True, stdout=subprocess.DEVNULL)
    for name, c in items:
        if 'to' in c:
            os.makedirs(f'{ROOT}/plates/{name}', exist_ok=True)
            for f in sorted(glob.glob(f'{tmp}/{name}-*.png')):
                Image.open(f).convert('RGB').save(f'{ROOT}/plates/{name}/{f[-8:-4]}.jpg', quality=92); os.remove(f)
        else:
            Image.open(f'{tmp}/{name}.png').convert('RGB').save(f'{ROOT}/plates/{name}.jpg', quality=94)
            if c.get('depth'):
                import numpy as np, base64
                d = np.asarray(Image.open(f'{tmp}/{name}.depth.png').convert('RGB')).astype(np.uint16)
                v = (d[:, :, 0] << 8) | d[:, :, 1]; v[d[:, :, 2] > 127] = 65535
                open(f'{ROOT}/plates/{name}.depth.js', 'w').write(f"(window.DEPTH = window.DEPTH || {{}})['{name}'] = {{w:{v.shape[1]},h:{v.shape[0]},b64:'" + base64.b64encode(v.astype('<u2').tobytes()).decode() + "'};\n")
            os.remove(f'{tmp}/{name}.png')
print('ok')
