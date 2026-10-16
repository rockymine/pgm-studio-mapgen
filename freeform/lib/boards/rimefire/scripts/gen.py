"""Generate Rimefire from land.py and paint.py."""
import os
import sys

import numpy as np

import land as LND
import paint as PNT
from pgmvox import B, World, rng
from pgmvox.geom import noise, shapes
from pgmvox.surface import terrain as T

g = LND.ground()
H, land, X, Z = g["H"], g["land"], g["X"], g["Z"]
w = World(LND.X0, LND.Z0, LND.NX, LND.NZ, sy=LND.SY)
f = PNT.fields(g)
w.biome[:] = 35                                       # savanna: grass and oak leaves tinted a dry gold

# where the rock ends under each column: a cone hung from the edge, with spires
edge = shapes.edge_depth(land).astype(float)
spire = np.maximum(noise.fbm(H.shape, 14, 2, seed=81) - 0.1, 0) * 26
thick = 5 + 2.4 * np.maximum(edge, 0) ** 0.82 + spire * np.minimum(edge / 6, 1)
bottom = np.maximum(2, np.round(H - np.minimum(thick, 46))).astype(int)
deg, skins = PNT.lay_ground(w, g, f, bottom)
print("ground laid; slope >50:", int((deg[land] > 50).sum()), "cold columns:", int((skins[land] == 2).sum()),
      "dust:", int((skins[land] == 1).sum()), "warm:", int((skins[land] == 0).sum()))
import seam as SM

g["seam_floor"] = g["seam"] & land & (g["d"] < g["hw"] - 0.4)
cold_at = skins == 2
streams = SM.floor(w, g)
print("seam floor:", streams)
n_road = 0
for name, b, pts in g["roads"]:
    n_road += SM.road_surface(w, g, f, cold_at, pts, 3, len(name))
for name, pts in g["ramps"]:
    n_road += SM.road_surface(w, g, f, cold_at, pts, 3.4, 5)
steps = sum(SM.stairs(w, g, pts, cold_at, 4) for _, _, pts in g["roads"]) + sum(SM.stairs(w, g, pts, cold_at, 3) for _, pts in g["ramps"])
print("path columns:", n_road, "stairs:", steps)
for cx in (-40, 39):
    SM.timber_bridge(w, g, cx, 4)
SM.keystone(w, g)
import echo
import places as P

before_ids, before_dat, tiles0 = w.ids.copy(), w.dat.copy(), len(w.tiles)
claims = []
info = {"lodge": P.lodge(w, g, claims), "furnace": P.furnace(w, g, claims)}
P.hamlet(w, g, claims)
P.watchtower(w, g, claims)
P.waystation(w, g, claims)
print('road lamps:', P.road_lamps(w, g))
print('lava falls:', P.lava_falls(w, g))
print('hoodoos:', P.hoodoos(w, g, [(52, -32, 6, 14, 26), (-56, -22, 4, 10, 18), (30, -22, 3, 8, 14), (-24, -86, 3, 12, 20)]))
print("echoed:", echo.mirror_changes(w, before_ids, before_dat, tiles0))
claims += [(n, -1 - x1, -1 - z1, -1 - x0, -1 - z0) for n, x0, z0, x1, z1 in claims]
import dress as DR
trees_n, planted = DR.forest(w, g, f, skins, claims)
print('trees:', trees_n)
print('litter:', DR.litter(w, g, skins, planted))
print('shrubs:', DR.shrubs(w, g, skins, claims, planted))
print('features:', DR.features(w, g, skins, claims, planted))
print('cover:', DR.cover(w, g, f, skins, claims))
# a snow layer needs something solid under it
under = np.zeros(w.ids.shape, bool)
under[:, 1:, :] = (w.ids[:, :-1, :] == B.AIR) | (w.ids[:, :-1, :] == B.SNOW_LAYER)
hang = (w.ids == B.SNOW_LAYER) & under
w.ids[hang] = B.AIR
w.dat[hang] = 0
print("snow layers removed from over air:", int(hang.sum()))
import plan as PLAN
from pgmvox.play.rules import mark_ground

PLAN.objectives().stamp(w)
print("ground marked:", mark_ground(w))
w.save(sys.argv[1], "Rimefire", (-14, LND.LEVEL + 2, -73))
