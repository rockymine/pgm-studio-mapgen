import sys, os, json
from PIL import Image, ImageDraw
d, step, name = sys.argv[1], int(sys.argv[2]), sys.argv[3]
info = json.load(open('filminfo.json'))
fs = sorted(f for f in os.listdir(d) if f.endswith('.jpg'))[::step]
per = 16
for s in range(0, len(fs), per):
    sheet = Image.new('RGB', (1920, 1080)); dr = ImageDraw.Draw(sheet)
    for i, f in enumerate(fs[s:s + per]):
        im = Image.open(f'{d}/{f}').resize((480, 270)); x, y = (i % 4) * 480, (i // 4) * 270; sheet.paste(im, (x, y))
        t = int(f[:6]) / 30; sh = [k['id'] for k in info['shots'] if k['t0'] <= t][-1]
        dr.rectangle([x, y, x + 110, y + 16], fill=(0, 0, 0)); dr.text((x + 3, y + 2), f'{t:6.1f}s {sh}', fill=(255, 255, 0))
    sheet.save(f'out/{name}-{s // per:02d}.jpg', quality=80)
print(len(fs), 'frames ->', (len(fs) + per - 1) // per, 'sheets')
