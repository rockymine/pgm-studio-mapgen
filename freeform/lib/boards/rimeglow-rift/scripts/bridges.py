"""The three crossings of the rift. Each is stated for the north half and written twice, so the two halves wear
their own materials and meet at the seam: the causeway an arch of stone over the lava, the two side bridges
timber through-trusses."""
import math

from pgmvox import B

DECK = 59                                   # the top block of every deck, level with the gate plazas


def causeway(S, H):
    """The central arch bridge: 8 wide (x -4 to 3), z -20 to -1 in the north half."""
    a = 12.0
    for x in range(-4, 4):
        for z in range(-20, 0):
            px, pz = S.xz(x, z)
            ground = int(H[px - S.w.x0, pz - S.w.z0])
            S.set(x, DECK, z, ("pave_a", "pave_b", "pave_c", "pave_a")[(x + 4 + z // 3) % 4])
            S.set(x, DECK - 1, z, "wall")
            zc = z + 0.5
            intrados = 45 + 12 * math.sqrt(1 - zc * zc / (a * a)) if abs(zc) < a else 99
            for y in range(max(ground, 30), DECK - 1):
                if y >= intrados:
                    S.set(x, y, z, "wall" if y <= intrados + 1.2 else "wall_b")
    for z in range(-20, 0):
        for x in (-4, 3):
            S.set(x, DECK + 1, z, "post")
        if z % 4 == 2:                                               # a pier of the parapet, lit
            for x in (-4, 3):
                S.set(x, DECK + 1, z, "wall")
                S.set(x, DECK + 2, z, "wall")
                S.set(x, DECK + 3, z, "light")
    for x in range(-4, 4):                                           # the seam: a stripe of the other half's colour
        S.set(x, DECK, -1, "hot")
    # the fascia: a course standing proud of each edge on corbels, and a keystone in the crown of the arch
    for z in range(-20, 0):
        for x, face in ((-5, "e"), (4, "w")):
            S.set(x, DECK - 1, z, "plinth")
            if z % 2 == 0:
                S.stair(x, DECK - 2, z, "wall", face, upside=True)
    for x in (-5, 4):
        for z in range(-20, -17):
            S.set(x, DECK, z, "plinth")
    for x in range(-4, 4):
        for y in (DECK - 3, DECK - 2):
            S.set(x, y, -1, "hot") if x in (-4, 3) else None


def trestle(S, H, xc):
    """A side bridge, 5 wide between two trusses: z -18 to -1 in the north half, xc its centre column."""
    for z in range(-18, 0):
        for dx in range(-2, 3):
            S.set(xc + dx, DECK, z, ("plank", "plank_b")[(z // 2 + abs(dx)) % 2])
        S.log(xc, DECK - 1, z, "z")
        S.log(xc - 2, DECK - 1, z, "z")
        S.log(xc + 2, DECK - 1, z, "z")
        for dx in (-3, 3):                                           # the chords, top and bottom
            S.log(xc + dx, DECK, z, "z")
            S.log(xc + dx, DECK + 5, z, "z")
    for z in range(-18, 0, 4):                                       # posts, and a portal beam across the top
        for dx in (-3, 3):
            for y in range(DECK + 1, DECK + 5):
                S.log(xc + dx, y, z)
        for dx in range(-2, 3):
            S.log(xc + dx, DECK + 5, z, "x")
        S.set(xc, DECK + 4, z, "light")
        for y in range(DECK - 3, DECK - 1):                          # a lamp hung under each bent, over the lava
            S.set(xc, y, z, (B.IRON_BARS, 0))
        S.set(xc, DECK - 4, z, "light")
        for z2 in range(z + 1, min(z + 4, 0)):                       # diagonals rising to the middle
            for dx in (-3, 3):
                S.set(xc + dx, DECK + (z2 - z), z2, "fence")
