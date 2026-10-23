"""Hollowstack's teams, spawns and monuments. Blue's are drawn; red's are their images under the half turn.

Each team defends two obsidian monuments on its own side: one floating over the Grove Shrine's altar in the
Underwood's mouth, one over the Vault's dais at the Undercroft's back. A wool here could not be defended; a monument
is broken where it stands, so the map asks to be held rather than raided.

    objectives()    pgmvox Objectives: two spawns, the observer, four monuments
"""
import layout as L
from pgmvox import B
from pgmvox.play.objectives import Box, Destroyable, Objectives, Observer, Spawn, Teams

SPAWN_AREA = Box(81, L.KEEP_Y + 1, 2, 92, L.KEEP_Y + 6, 10)
MAX_BUILD = 118


def shrine_at():
    s = L.SHRINE
    return (s["x0"] + s["x1"]) // 2, s["floor"] + 2, (s["z0"] + s["z1"]) // 2


def vault_at():
    vi0, vj0, vi1, vj1 = L.VAULT
    vx, vy, vz = L.cell_box(L.UNDERCROFT, vi1, vj1)
    _, _, vz0 = L.cell_box(L.UNDERCROFT, vi0, vj0)
    return vx + L.CELL - 3, vy + 2, (vz0 + vz + L.CELL - 1) // 2


def monument(x, top, z):
    """Three of obsidian floating three blocks over `top`, the block it hangs above."""
    return Box(x, top + 4, z, x, top + 6, z)


def objectives():
    O = Objectives(Teams(("blue-team", "Blue", "blue", 16), ("red-team", "Red", "red", 16)), L.SYM)
    O.add(Spawn("blue-team", L.SPAWN, yaw=90, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Observer((0.5, 112, 0.5), yaw=90), mirror=False)
    sx, sy, sz = shrine_at()
    vx, vy, vz = vault_at()
    O.add(Destroyable("blue-shrine", "Shrine Monument", "blue-team", monument(sx, sy - 1, sz), (B.OBSIDIAN, 0),
                      "obsidian"))
    O.add(Destroyable("blue-vault", "Vault Monument", "blue-team", monument(vx, vy - 1, vz), (B.OBSIDIAN, 0),
                      "obsidian"))
    return O
