"""Check the Vale's shaped ground before a block is written: from the harbour, every place reached on foot with no
jump and no drop past three, over the heights the landforms and the graded roads leave."""
from land import FOOTPATH, PLACES, ground
from pgmvox import plangraph as G
from pgmvox.plan import Raster
from pgmvox.plangraph import PlanRules

X, Z, H, river, sea, road = ground()
R = Raster.from_heights(H, int(X[0, 0]), int(Z[0, 0]), water=river.mask | sea.mask)
E = G.graph(R, {"ground"}, rules=PlanRules(jumps=False, max_drop=3))
D, _ = G.dijkstra(E, [PLACES["harbour"]])
for name, at in list(PLACES.items()) + [("the spire's foot", FOOTPATH[1])]:
    near = [(x, z) for x in range(at[0] - 3, at[0] + 4) for z in range(at[1] - 3, at[1] + 4) if (x, z) in D]
    print(f"{name}: " + (f"{min(D[c] for c in near):.0f} blocks of walk from the harbour" if near
                         else "NOT reached from the harbour"))
print(f"ground reached: {len(D)} of {int((R.K == R.kinds['ground']).sum())} dry columns")
