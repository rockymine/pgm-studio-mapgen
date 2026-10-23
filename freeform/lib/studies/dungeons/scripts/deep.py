"""Dungeons with depth, finished through the grammar. Three layouts from dungeons.py given floors at many heights
(rooms raised and sunk, pits and daises, corridors ramping between them in stairs, balconies round tall halls, a
two-storey command hall), then finished: floors by a grammar Style's own fills, unchanged; walls, ceilings, door
frames and stairs by the adapter below, which is what the grammar would need to grow to speak interiors.

    dungeon   stone brick, a style written here in a dozen lines of the grammar's own parts
    crypt     marble.style() — the temple style, its fills on the floors, its quartz and prismarine on the walls
    bunker    foundry.style() — the industrial style, hazard bands, plates, iron and nether brick

    python3 deep.py [name ...]      # renders into ../renders/deep
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

import dungeons as D
from dungeons import N, ROCK, ROOM, CORR, DOOR, STAIR, PILLAR, rect, disc, I, K
from pgmvox import B, World                                                   # noqa: E402
from pgmvox.built import facade                                               # noqa: E402
from pgmvox.core.orient import stair                                          # noqa: E402
from pgmvox.grammar import rules as G, marks, marble, foundry                 # noqa: E402
from pgmvox.read import render                                                # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "deep")
SY = 72
DIR = {"e": (1, 0), "w": (-1, 0), "s": (0, 1), "n": (0, -1)}


# --- depth ---------------------------------------------------------------------------------------------------------

class Deep:
    """A level with depth: every open cell its own floor y and ceiling height; rooms as sections a style can fill."""

    def __init__(self, kind, height, base):
        self.kind = kind.copy()
        self.open = (kind != ROCK) & (kind != PILLAR)
        self.F = np.full((N, N), base, int)
        self.H = height.astype(int).copy()
        self.rooms = []                       # dicts: mask, floor, name, tags
        self.solid = []                       # (mask3d, block) laid after carving: balconies, steps, piers
        self.stairs = []                      # (x, y, z, rises) stair blocks

    def room_floors(self, rng, spread=4, keep=None):
        lab, n = ndimage.label(self.kind == ROOM)
        for k in range(1, n + 1):
            m = lab == k
            f = int(self.F[m][0] + (keep(k, m) if keep else rng.integers(-spread, spread + 1)))
            self.F[m] = f
            self.rooms.append(dict(mask=m, floor=f, name=f"room{k}", tags=set()))

    def ramps(self, iters=600):
        """Corridors and doors take floors between the rooms they join: relaxed toward their neighbours, rooms held,
        then rounded, so a corridor climbs or falls a block at a time along its length."""
        fixed = (self.kind == ROOM) | (self.kind == STAIR)
        free = self.open & ~fixed
        F = self.F.astype(float)
        nb = np.zeros((N, N))
        for dx, dz in DIR.values():
            nb += np.roll(self.open, (dx, dz), (0, 1))
        for _ in range(iters):
            s = np.zeros((N, N))
            for dx, dz in DIR.values():
                s += np.roll(np.where(self.open, F, 0), (dx, dz), (0, 1))
            F = np.where(free & (nb > 0), s / np.maximum(nb, 1), F)
        self.F = np.where(free, np.round(F), self.F).astype(int)
        for _ in range(4):                                                 # no step steeper than a block
            hi = ndimage.minimum_filter(np.where(self.open, self.F, 999), footprint=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
            self.F = np.where(free & (self.F > hi + 1), hi + 1, self.F)
            lo = ndimage.maximum_filter(np.where(self.open, self.F, -999), footprint=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
            self.F = np.where(free & (self.F < lo - 1), lo - 1, self.F)
        # a stair wherever the next cell along is a block higher
        for (dx, dz), side in ((v, k) for k, v in DIR.items()):
            up = self.open & np.roll(self.open, (-dx, -dz), (0, 1)) & (np.roll(self.F, (-dx, -dz), (0, 1)) == self.F + 1)
            for i, k in np.argwhere(up):
                self.stairs.append((i, self.F[i, k] + 1, k, side))

    def dais(self, m, up=1):
        self.F[m] += up

    def pit(self, centre, r, depth, ring=1):
        """A pit: rings stepping down `depth` blocks into a round floor, each a block lower and `ring` wide."""
        d = np.hypot(I - centre[0], K - centre[1])
        for k in range(depth):
            self.F[self.open & (d <= r - k * ring)] -= 1

    def balcony(self, m, at, width=2, stair_side="s"):
        """A gallery round the inside of room `m`, `at` over its floor, `width` deep, on piers every four along its
        inner edge, reached by a straight flight up along one wall."""
        f = int(self.F[m].max())
        inner = ndimage.binary_erosion(m, iterations=width)
        ring = m & ~inner
        self.H[m] = np.maximum(self.H[m], at + 4)
        vol = np.zeros((N, SY, N), bool)
        vol[:, f + at, :] = ring
        edge = ring & ndimage.binary_dilation(inner, np.ones((3, 3)))
        piers = edge & (((I + K) % 4) == 0)
        for i, k in np.argwhere(piers):
            vol[i, f + 1:f + at, k] = True
        xs, zs = np.nonzero(m)
        x0, z0, x1, z1 = xs.min(), zs.min(), xs.max(), zs.max()
        zrow = z1 - width if stair_side == "s" else z0 + width
        for s in range(at):                                                # the flight, rising east along the wall
            x = x0 + width + 1 + s
            if x > x1 - width:
                break
            self.stairs.append((x, f + 1 + s, zrow, "e"))
            vol[x, f + 1:f + 1 + s, zrow] = True
            vol[x, f + at, zrow] = False
        self.solid.append((vol, "deck"))
        return ring


# --- the layouts with depth ----------------------------------------------------------------------------------------

def dungeon():
    rng = np.random.default_rng(3)
    levels, _ = D.dungeon()
    lv = levels[0]
    dp = Deep(lv.kind, lv.height, 24)
    dp.room_floors(rng, spread=4)
    for r in dp.rooms:
        m = r["mask"]
        xs, zs = np.nonzero(m)
        area = m.sum()
        box = rect(xs.min(), zs.min(), xs.max(), zs.max())
        if (box & ~m & (dp.kind == PILLAR)).any() or (lv.kind[box] == PILLAR).any():
            dp.H[m] = 10
            dp.balcony(m, 5)
            r["tags"].add("hall")
        elif area > 500 and (box == m).all():
            dp.dais(rect(xs.min() + 5, zs.min() + 5, xs.max() - 5, zs.max() - 5) & m)
            r["tags"].add("dais")
        elif abs(area - np.pi * (np.ptp(xs) / 2) ** 2) < area * 0.2 and area > 120:
            dp.pit(((xs.min() + xs.max()) / 2, (zs.min() + zs.max()) / 2), np.ptp(xs) / 2 - 2, 3)
            dp.H[m] += 3
            r["tags"].add("pit")
    dp.ramps()
    return dp, "dungeon"


def crypt():
    levels, _ = D.crypt()
    lv = levels[0]
    dp = Deep(lv.kind, lv.height, 26)
    c = (N - 1) / 2
    r = np.hypot(I - c, K - c)
    def keep(k, m):
        rr = r[m].mean()
        return -4 if rr < 16 else (3 if rr > 55 else (-1 if 22 < rr < 32 else 0))
    dp.room_floors(None, keep=keep)
    dp.pit((c, c), 12, 3, ring=2)                                          # the rotunda steps down to its floor
    dp.H[r <= 16] = 14
    for rm in dp.rooms:
        if r[rm["mask"]].mean() > 55:
            rm["tags"].add("chapel")
            dp.H[rm["mask"]] = 9
        if r[rm["mask"]].mean() < 16:
            rm["tags"].add("rotunda")
    dp.ramps()
    return dp, "crypt"


def bunker():
    levels, shafts = D.bunker()
    lv = levels[0]
    dp = Deep(lv.kind, lv.height, 22)
    # the entrance ramps down from near the surface; the command hall is two storeys; the generator hall sunk
    def keep(k, m):
        xs, zs = np.nonzero(m)
        cx, cz = xs.mean(), zs.mean()
        if cx < 30 and cz < 60:
            return 10                                                      # the guard room, high by the entrance
        if 50 < cx < 95 and cz < 56:
            return -2                                                      # command
        if cx > 105 and cz > 95:
            return -6                                                      # generator hall
        return 0
    dp.room_floors(None, keep=keep)
    entry = (I < 18) & (K < 48)
    dp.F[entry & dp.open] = 34                                            # the chicane's top, under the surface
    dp.kind[entry & dp.open] = STAIR                                       # held there; the rest ramps down to 22
    for rm in dp.rooms:
        xs, zs = np.nonzero(rm["mask"])
        if 50 < xs.mean() < 95 and zs.mean() < 56:
            rm["tags"].add("command")
            dp.H[rm["mask"]] = 11
            dp.balcony(rm["mask"], 5, stair_side="n")
        if xs.mean() > 105 and zs.mean() > 95:
            rm["tags"].add("generator")
            dp.H[rm["mask"]] = 12
            m = rm["mask"]
            walk = m & (np.abs(K - (zs.min() + zs.max()) / 2) < 1.5)            # a catwalk across, at the door's level
            vol = np.zeros((N, SY, N), bool)
            vol[:, rm["floor"] + 6, :] = walk
            dp.solid.append((vol, "deck"))
    dp.ramps(iters=900)
    return dp, "bunker"


# --- the finish: what a style lays inside --------------------------------------------------------------------------

def dungeon_style():
    """A stone-brick style from the grammar's own parts: fills by marks.field and facade patterns."""
    SB, MOSSY, CRACK, CHIS, COB = (B.STONEBRICK, 0), (B.STONEBRICK, 1), (B.STONEBRICK, 2), (B.STONEBRICK, 3), (B.COBBLE, 0)
    fills = {
        "flags": marks.field(lambda c: (SB, SB, SB, CRACK, SB, MOSSY, SB, CRACK)[(c.x * 7919 + c.z * 104729) % 8],
                             name="flags"),
        "checker": marks.field(facade.first_of(facade.border(1, CHIS), lambda c: SB if (c.x + c.z) % 2 else (B.STONE, 6)),
                               name="checker"),
        "plain": marks.field(facade.border(1, CHIS), under=SB, name="plain"),
    }
    return G.Style("dungeon", body=None, faces={}, seam=CHIS, fills=fills,
                   choose=lambda sec, lot: ["checker"] if "dais" in sec.tags or "hall" in sec.tags else ["flags"])


PACKS = {
    "dungeon": dict(style=dungeon_style, plinth=(B.STONEBRICK, 3), field=G.Mix((((B.STONEBRICK, 0), 6), ((B.STONEBRICK, 2), 2), ((B.STONEBRICK, 1), 1))),
                    frieze=(B.STONEBRICK, 3), cornice=lambda side: (B.STONEBRICK_STAIRS, stair(side, upside_down=True)),
                    pilaster=(B.STONEBRICK, 3), niche=(B.GLOWSTONE, 0), bay=6, ceiling=(B.STONEBRICK, 0), ceiling_rib=(B.STONEBRICK, 3),
                    corridor=(B.COBBLE, 0), deck=(B.STONEBRICK, 0), stair=B.STONEBRICK_STAIRS, rock=(B.STONE, 0)),
    "crypt": dict(style=lambda: marble.style(), plinth=marble.CHISELED, field=marble.QUARTZ, frieze=marble.DARK,
                  cornice=lambda side: (B.QUARTZ_STAIRS, stair(side, upside_down=True)), pilaster=marble.PILLAR,
                  niche=marble.LANTERN, bay=6, ceiling=marble.QUARTZ, ceiling_rib=marble.DARK, corridor=marble.POLISHED,
                  deck=marble.CHISELED, stair=B.QUARTZ_STAIRS, rock=marble.DIORITE),
    "bunker": dict(style=lambda: foundry.style(), plinth=foundry.BLACK, field=G.Mix(((foundry.SBRICK, 5), (foundry.CRACKED, 1))),
                   frieze=foundry.NETHER, cornice=lambda side: foundry.IRON, pilaster=foundry.IRON, niche=foundry.GLOW, bay=5,
                   ceiling=foundry.SMOOTH, ceiling_rib=foundry.IRON, corridor=foundry.ANDESITE, deck=foundry.IRON,
                   stair=B.STONEBRICK_STAIRS, rock=(B.STONE, 0), hazard=True),
}


def carve(dp, pack):
    w = World(-N // 2, -N // 2, N, N, sy=SY)
    w.ids[:, :SY - 12, :] = pack["rock"][0]
    w.dat[:, :SY - 12, :] = pack["rock"][1]
    ys = np.arange(SY)[None, :, None]
    air = dp.open[:, None, :] & (ys > dp.F[:, None, :]) & (ys <= (dp.F + dp.H)[:, None, :])
    w.ids[air] = 0
    w.dat[air] = 0
    return w, air


def finish(w, dp, pack, rng):
    """Floors by the style's fills; walls, ceilings, door frames, stairs and decks by the interior adapter."""
    style = pack["style"]()
    ox, oz = w.x0, w.z0
    # floors: every room a Section at its floor, the style chooses and lays the fill; corridors get theirs
    secs = []
    for rm in dp.rooms:
        m = rm["mask"] & (dp.F == rm["floor"])
        if m.sum() < 4:
            continue
        xs, zs = np.nonzero(m)
        boxes = tuple((int(x) + ox, int(z) + oz, int(x) + ox, int(z) + oz) for x, z in zip(xs, zs))
        secs.append((G.Section(boxes=boxes, y=rm["floor"], name=rm["name"], tags=frozenset(rm["tags"])), m))
    for sec, m in secs:
        ground = G.Ground([sec])
        lot = G.Lot(sec, 0, ground.inside(0, 0), sec.y, ground, {})
        style.fill(w, lot, rng)
        for x, z in sec.columns():                                        # the seam where the room meets its walls
            i, k = x - ox, z - oz
            if any(not dp.open[i + dx, k + dz] for dx, dz in DIR.values()):
                w.set(x, sec.y, z, *style.seam)
    other = dp.open & ~np.any([m for _, m in secs] or [np.zeros((N, N), bool)], axis=0)
    for i, k in np.argwhere(other):
        b = pack["corridor"]
        if pack.get("hazard") and dp.kind[i, k] == DOOR:
            b = foundry.YELLOW if (i + k) % 2 else foundry.BLACK
        w.ids[i, dp.F[i, k], k], w.dat[i, dp.F[i, k], k] = b
    # walls: every rock column beside open air, courses anchored at its floor and at its ceiling
    wall_faces = 0
    for side, (dx, dz) in DIR.items():
        opp = {"e": "w", "w": "e", "s": "n", "n": "s"}[side]
        beside = ~dp.open & np.roll(dp.open, (-dx, -dz), (0, 1))
        for i, k in np.argwhere(beside):
            j, l = i + dx, k + dz
            if not (0 <= j < N and 0 <= l < N):
                continue
            f, h = dp.F[j, l], dp.H[j, l]
            top = f + h
            along = (k if side in ("e", "w") else i)
            room = dp.kind[j, l] == ROOM and h >= 5
            bay = pack["bay"]
            pos = along % bay
            door_jamb = any(dp.kind[i + a, k + b] == DOOR for a, b in DIR.values() if 0 <= i + a < N and 0 <= k + b < N)
            for y in range(f + 1, top + 1):
                t = y - f                                                    # 1 at the plinth
                if door_jamb:
                    b = pack["pilaster"]
                elif t == 1:
                    b = pack["plinth"]
                elif y == top:
                    b = pack["frieze"]
                elif room and pos == 0 and y < top - 1:
                    b = pack["pilaster"]
                elif room and pos == bay // 2 and t == 3:
                    b = pack["niche"]
                else:
                    b = G.spec(pack["field"], opp, rng=rng)
                w.set(i + ox, y, k + oz, *b)
            if room and h >= 6:                                             # a cornice thrown out under the ceiling
                if w.ids[j, top, l] == 0:
                    w.set(j + ox, top, l + oz, *pack["cornice"](side))
            wall_faces += 1
    # ceilings: ribs every bay over rooms, the field between; corridors plain
    for i, k in np.argwhere(dp.open):
        y = dp.F[i, k] + dp.H[i, k] + 1
        if y >= SY:
            continue
        rib = dp.kind[i, k] == ROOM and ((i % pack["bay"]) == 0 or (k % pack["bay"]) == 0)
        w.ids[i, y, k], w.dat[i, y, k] = pack["ceiling_rib"] if rib else pack["ceiling"]
    # decks and steps, then stairs on every rise
    for vol, what in dp.solid:
        w.ids[vol], w.dat[vol] = pack[what]
    for i, y, k, rises in dp.stairs:
        if 0 <= y < SY and w.ids[i, y, k] == 0:
            w.ids[i, y, k], w.dat[i, y, k] = pack["stair"], stair(rises)
    return wall_faces


def dollhouse(w, dp, above=3):
    """The world with every column cut `above` blocks over the floor beside it: rooms open to the sky at waist
    height, each at its own depth, the walls left standing that high round it."""
    near = ndimage.grey_dilation(np.where(dp.open, dp.F, -99), size=(5, 5))
    cut = np.where(dp.open, dp.F, near) + above
    cut = np.where(cut < 0, int(dp.F[dp.open].min()) - 2, cut)              # rock away from any room: cut low
    ys = np.arange(SY)[None, :, None]
    ids, dat = w.ids.copy(), w.dat.copy()
    gone = ys > cut[:, None, :]
    ids[gone] = 0
    return ids, dat


def heights_plan(dp, out, title, scale=5):
    img = np.zeros((N, N, 3), float)
    img[:] = (60, 62, 68)
    lo, hi = dp.F[dp.open].min(), dp.F[dp.open].max()
    t = (dp.F - lo) / max(hi - lo, 1)
    ramp = np.stack([60 + 180 * t, 110 + 100 * t, 200 - 120 * t], -1)
    img[dp.open] = ramp[dp.open]
    for i, y, k, s in dp.stairs:
        img[i, k] = (250, 250, 250)
    im = Image.fromarray(img.astype(np.uint8).transpose(1, 0, 2)).resize((N * scale, N * scale), Image.NEAREST)
    ImageDraw.Draw(im).text((8, 6), f"{title}: floor heights y {lo} (blue) to {hi} (orange); stairs white", fill=(255, 255, 255))
    im.save(out)


def main(names):
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(1)
    for f in (dungeon, crypt, bunker):
        n = f.__name__
        if names and n not in names:
            continue
        dp, key = f()
        pack = PACKS[key]
        w, air = carve(dp, pack)
        faces = finish(w, dp, pack, rng)
        heights_plan(dp, f"{OUT}/{n}-heights.png", n)
        lo, hi = int(dp.F[dp.open].min()), int(dp.F[dp.open].max())
        ids, dat = dollhouse(w, dp, 4)
        render.iso(ids, dat, w.x0, w.z0, f"{OUT}/{n}-cut.png", 3, "se", ymin=lo - 3)
        render.iso(ids, dat, w.x0, w.z0, f"{OUT}/{n}-close.png", 6, "se", box=CLOSE[n], ymin=lo - 3)
        ids2, _ = dollhouse(w, dp, 12)
        render.iso(ids2, dat, w.x0, w.z0, f"{OUT}/{n}-tall.png", 6, "se", box=CLOSE[n], ymin=lo - 3)
        render.trim(f"{OUT}/{n}-tall.png")
        for p in ("cut", "close"):
            render.trim(f"{OUT}/{n}-{p}.png")
        cx = (CLOSE[n][1] + CLOSE[n][3]) // 2
        render.cutaway(w, f"{OUT}/{n}-section.png", [(-80, cx), (79, cx)], ymin=lo - 3, ymax=min(SY - 1, hi + 16), scale=4,
                       title=f"{n}: section west to east at z {cx}")
        print(f"{n:8s} floors y {lo}..{hi}  rooms {len(dp.rooms)}  stairs {len(dp.stairs)}  wall columns {faces}")


CLOSE = {"dungeon": (-40, -40, 20, 20), "crypt": (-30, -30, 30, 30), "bunker": (-30, -55, 30, -10)}

if __name__ == "__main__":
    main(sys.argv[1:])
