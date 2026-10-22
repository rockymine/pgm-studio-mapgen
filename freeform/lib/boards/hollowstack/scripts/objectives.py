"""Hollowstack's teams, spawns and wools. Blue's are drawn; red's are their images under the half turn.

Blue carries two wools home that red keeps: lime from red's Grove Shrine and yellow from red's Vault; red carries
orange and light blue from blue's. Each wool lies where blue's own rooms are, turned onto red's side.

    objectives()    pgmvox Objectives: two spawns, the observer, four wools
"""
import layout as L
import places as P
from pgmvox.play.objectives import Box, Objectives, Observer, Spawn, Teams, Wool, turn_point

SPAWN_AREA = Box(81, L.KEEP_Y + 1, 2, 92, L.KEEP_Y + 6, 10)
MAX_BUILD = 118


def room(box):
    return Box(*box)


def objectives():
    O = Objectives(Teams(("blue-team", "Blue", "blue", 16), ("red-team", "Red", "red", 16)), L.SYM)
    O.add(Spawn("blue-team", L.SPAWN, yaw=90, kit="spawn-kit", area=SPAWN_AREA))
    O.add(Observer((0.5, 112, 0.5), yaw=90), mirror=False)
    s = L.SHRINE
    shrine_at = ((s["x0"] + s["x1"]) // 2, s["floor"] + 2, (s["z0"] + s["z1"]) // 2)
    vi0, vj0, vi1, vj1 = L.VAULT
    vx, vy, vz = L.cell_box(L.UNDERCROFT, vi1, vj1)
    _, _, vz0 = L.cell_box(L.UNDERCROFT, vi0, vj0)
    vault_at = (vx + L.CELL - 3, vy + 2, (vz0 + vz + L.CELL - 1) // 2)
    shrine_room, vault_room = room(P.shrine_room()), room(P.vault_room())
    O.add(Wool("blue-team", "lime", slot=L.MONUMENTS[0], found=turn_point(shrine_at, L.SYM),
               room=shrine_room.image(L.SYM)), color="orange")
    O.add(Wool("blue-team", "yellow", slot=L.MONUMENTS[1], found=turn_point(vault_at, L.SYM),
               room=vault_room.image(L.SYM)), color="light_blue")
    return O
