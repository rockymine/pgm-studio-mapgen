"""Read the built Loomfall back, on the blocks.

1. THE WOOL. Every carpet's cell is wool in its pattern, none of it white, and nothing solid directly under any of it,
   so every trampled block can fall.
2. THE FALLS. From every cell of wool, straight down through the built blocks to the first thing above the kill
   height: the same carpet the plan says, or nothing.
3. NOWHERE TO WAIT. Every block above the kill height that is not a carpet's wool is a lantern six and more over the
   top carpet: nothing a player could reach and stand on to wait out the match.

    python3 walk.py <build-dir>
"""
import sys

import numpy as np

import plan as P
import render_iso


def main(build):
    x0, z0, ids, dat = render_iso.load(build)

    def at(x, y, z):
        return int(ids[x - x0, y, z - z0]), int(dat[x - x0, y, z - z0])

    out = []
    wrong, white, held = [], 0, []
    owner = {}
    for k, c in enumerate(P.CARPETS):
        y = c[5]
        for x, z in P.cells(c):
            b, d = at(x, y, z)
            owner[(x, y, z)] = k
            if b != 35 or d != P.pattern(k, x, z):
                wrong.append((k + 1, x, z, b, d))
            if b == 35 and d == 0:
                white += 1
            if at(x, y - 1, z)[0] != 0:
                held.append((k + 1, x, z, at(x, y - 1, z)[0]))
    out.append(f"carpet cells not their pattern's wool: {len(wrong)}; white: {white}; held up from below: {len(held)}"
               + (f" {held[:4]}" if held else ""))
    mism = 0
    for k, c in enumerate(P.CARPETS):
        y = c[5]
        for x, z in P.cells(c):
            land = None
            for yy in range(y - 1, P.KILL_Y - 1, -1):
                if ids[x - x0, yy, z - z0]:
                    land = owner.get((x, yy, z), "something else")
                    break
            if land != P.below(k, x, z):
                mism += 1
    out.append(f"cells whose fall lands elsewhere than the plan says: {mism}")
    top_y = P.CARPETS[0][5]
    stray = []
    for y in range(P.KILL_Y, ids.shape[1]):
        xs, zs = np.nonzero(ids[:, y, :])
        for i, j in zip(xs, zs):
            x, z = int(i) + x0, int(j) + z0
            if (x, y, z) in owner:
                continue
            if y >= top_y + 5:
                continue                                          # a lantern, out of anyone's reach
            stray.append((x, y, z, int(ids[i, y, j])))
    out.append(f"blocks above the kill height a player could reach and stand on: {len(stray)}" + (f" {stray[:5]}" if stray else ""))
    roof = int(np.nonzero(ids[:, :P.KILL_Y, :].any(axis=(0, 2)))[0].max())
    out.append(f"the city's highest block: {roof}, under the kill height of {P.KILL_Y}")
    print("\n".join(out))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
