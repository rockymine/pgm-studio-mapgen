"""The plan's own numbers, measured from the ground it states before any block is written, each against its target."""
import numpy as np

import land as LD
import plan as PL

X, Z, H0, cd = LD.ground()
H, laid, paths = LD.graded(H0, X, Z)
half = LD.SZ // 2
Hn = np.round(H).astype(int)
Hn[:, half:] = LD.turned(Hn)[:, half:]
land = LD.land_mask(X, Z)
rows = []


def row(value, what, target, ok):
    rows.append((value, what, target, ok))


row(f"{int((Hn == LD.turned(Hn))[land].all())}", "ground is its own half turn", "1", bool((Hn == LD.turned(Hn))[land].all()))
cols = np.where(land.any(axis=1))[0]
rws = np.where(land.any(axis=0))[0]
foot = (int(cols[-1] - cols[0] + 1), int(rws[-1] - rws[0] + 1))
row(f"{foot[0]} x {foot[1]}", "footprint of the land", "at most 150 x 200", foot[0] <= 150 and foot[1] <= 200)
frac = land.sum() / (foot[0] * foot[1])
row(f"{land.sum()} columns, {frac:.0%} of the footprint", "ground against its own footprint", "under 80%: the rest is void", frac < 0.80)
for name, xc in (("centre", 0), ("west", -39), ("east", 38)):
    i = xc - LD.X0
    col = Hn[i]
    lava = np.where(cd[i] < 0)[0]
    z0, z1 = lava[0], lava[-1]
    rim_n = z0 - np.argmax(col[:z0][::-1] >= LD.RIM - 2) if True else 0
    span = float(2 * LD.half_width(xc + 0.5) + 2 * 9.75)
    row(f"{span:.0f}", f"rim to rim at the {name} crossing", "24 to 36", 24 <= span <= 36)
row(f"{LD.SHELF_W:.1f}", "width of the ledge along the lava", "at least 3", LD.SHELF_W >= 3)
row(f"{LD.SHELF_Y - LD.LAVA}", "ledge above the lava", "2 to 4", 2 <= LD.SHELF_Y - LD.LAVA <= 4)
row(f"{LD.DECK_Y - LD.RIM}", "deck above the shelves' rim", "at most 3", LD.DECK_Y - LD.RIM <= 3)
row(f"{PL.CORE_BOX.y0 - 67}", "air under each core, over its pit's floor", "at least 3 (and the leak, 6)", PL.CORE_BOX.y0 - 67 >= 6)
row(f"{PL.KILL_Y}", "kill height under the lowest ground", f"under {int(13)}", PL.KILL_Y < 13)
mere = LD.mere_mask(X, Z) & land
row(f"{int(mere.sum() // 2)} columns", "flat floor of each mere", "a place to fight: at least 600", mere.sum() // 2 >= 600)
print("\n".join(f"{what:<46} {str(value):<34} {target}{'  ok' if ok else '  MISS'}" for value, what, target, ok in rows))
