"""Render a PlanModel's cell rectangles as an ASCII grid. Cells, not blocks: the units the plan is
actually written in, so a width mismatch between two rects is visible as a width mismatch — and so is
a hole, because a hole in a plan is not a subtraction but a gap the pieces enclose."""
import json, sys

GLYPH = {}

def render(plan, note=""):
    cell = plan["globals"]["cell"]
    items = []
    for piece in plan["pieces"]:
        x, z, w, h = piece["rect"]
        items.append((piece["id"], x, z, w, h, piece.get("role", "piece"), piece.get("mirrors", True)))
    for zone in plan.get("zones", []):
        x, z, w, h = zone["rect"]
        items.append((zone["id"], x, z, w, h, zone.get("kind", "build"), True))

    sym = plan["globals"].get("symmetry", "rot_180")
    placed = []
    for (pid, x, z, w, h, role, mirrors) in items:
        placed.append((pid, x, z, w, h, role, 0))
        if mirrors and sym == "rot_180":
            image = (-x - w, -z - h, w, h)
            # a rect centred on the origin is its own image; drawing it twice reads as a collision
            if image != (x, z, w, h):
                placed.append((pid, *image, role, 1))

    minX = min(p[1] for p in placed); maxX = max(p[1] + p[3] for p in placed)
    minZ = min(p[2] for p in placed); maxZ = max(p[2] + p[4] for p in placed)

    glyphs, nxt = {}, 0
    pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for (pid, *_rest) in placed:
        if pid not in glyphs:
            glyphs[pid] = pool[nxt]; nxt += 1

    grid = [[" "] * (maxX - minX) for _ in range(maxZ - minZ)]
    for (pid, x, z, w, h, role, image) in placed:
        ch = glyphs[pid]
        if image: ch = ch.lower() if ch.isupper() else ch.upper()
        for zz in range(z, z + h):
            for xx in range(x, x + w):
                cur = grid[zz - minZ][xx - minX]
                grid[zz - minZ][xx - minX] = ch if cur == " " else "#"

    # A hole is ground ringed by the board and covered by nothing. Two definitions exist and both
    # matter: `PlanVoids.Declare` counts pieces only and names every enclosed terrain void a `void-N`
    # buffer on each compile, author or no author; `BoardDeriver` (docs/gameplay/match-flow.md §6.8)
    # counts the declared build regions as enclosing too, because a band a route crosses is a side of
    # the hole it forks around. This renders the second, which is the one flow is measured against —
    # so zones count as sides here. Flood the empty cells from outside the frame; what it cannot
    # reach is enclosed.
    outside, stack = set(), []
    for x in range(minX - 1, maxX + 1):
        stack += [(x, minZ - 1), (x, maxZ)]
    for z in range(minZ - 1, maxZ + 1):
        stack += [(minX - 1, z), (maxX, z)]
    while stack:
        cx, cz = stack.pop()
        if (cx, cz) in outside: continue
        if not (minX - 1 <= cx <= maxX and minZ - 1 <= cz <= maxZ): continue
        if minX <= cx < maxX and minZ <= cz < maxZ and grid[cz - minZ][cx - minX] != " ": continue
        outside.add((cx, cz))
        stack += [(cx + 1, cz), (cx - 1, cz), (cx, cz + 1), (cx, cz - 1)]
    holes = 0
    for zz in range(minZ, maxZ):
        for xx in range(minX, maxX):
            if grid[zz - minZ][xx - minX] == " " and (xx, zz) not in outside:
                grid[zz - minZ][xx - minX] = "o"; holes += 1

    print(f"=== {plan['meta']['name']}{note} — cell grid, 1 char = {cell}×{cell} blocks, "
          f"{maxX-minX}×{maxZ-minZ} cells = {(maxX-minX)*cell}×{(maxZ-minZ)*cell} blocks")
    header = "     " + "".join(str(abs(x) % 10) for x in range(minX, maxX))
    print(header)
    print("     " + "".join("-" if x == 0 else " " for x in range(minX, maxX)))
    for zi, row in enumerate(grid):
        z = minZ + zi
        mark = "<<< z=0" if z == 0 else ""
        print(f"{z:>4} |" + "".join(row) + "|" + mark)
    print()
    if holes:
        print(f"  o  = enclosed void — {holes} cells the board rings and nothing covers (pieces and build")
        print(f"       zones both count as sides, per match-flow.md §6.8). A hole is made by ARRANGEMENT,")
        print(f"       never by subtraction: a buffer drawn over a piece is inert by design, and the")
        print(f"       compiler declares every enclosed void a `void-N` buffer on each compile anyway.")
    print("  legend (upper = stated, lower = its rot_180 image)")
    for (pid, x, z, w, h, role, image) in placed:
        if image: continue
        bx0, bz0, bx1, bz1 = x * cell, z * cell, (x + w) * cell, (z + h) * cell
        print(f"    {glyphs[pid]}  {pid:<16} {role:<11} cells x {x:>3}..{x+w:<3} z {z:>3}..{z+h:<3}"
              f"   blocks x {bx0:>4}..{bx1:<4} z {bz0:>4}..{bz1:<4}   ({w}×{h} cells)")

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2] if len(sys.argv) > 2 else "")
