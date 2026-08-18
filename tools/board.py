"""Render a PlanModel's cell rectangles as an ASCII grid. Cells, not blocks: the units the plan
is actually written in, so a width mismatch between two rects is visible as a width mismatch."""
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
        if mirrors:
            if sym == "rot_180":
                placed.append((pid, -x - w, -z - h, w, h, role, 1))

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
    print("  legend (upper = stated, lower = its rot_180 image)")
    for (pid, x, z, w, h, role, image) in placed:
        if image: continue
        bx0, bz0, bx1, bz1 = x * cell, z * cell, (x + w) * cell, (z + h) * cell
        print(f"    {glyphs[pid]}  {pid:<16} {role:<11} cells x {x:>3}..{x+w:<3} z {z:>3}..{z+h:<3}"
              f"   blocks x {bx0:>4}..{bx1:<4} z {bz0:>4}..{bz1:<4}   ({w}×{h} cells)")

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2] if len(sys.argv) > 2 else "")
