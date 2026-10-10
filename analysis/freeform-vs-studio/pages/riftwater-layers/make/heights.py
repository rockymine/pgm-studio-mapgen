"""Run the Riftwater port's land() verbatim with a snapshot after each step; save the stack."""
import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import sys, os, inspect, textwrap, pickle, numpy as np
B = os.path.join(ROOT, "freeform/lib/ports/riftwater/scripts")
sys.path.insert(0, B); sys.path.insert(0, os.path.join(ROOT, "freeform/lib"))
os.chdir(B)
import plan as P
src = textwrap.dedent(inspect.getsource(P.land.__wrapped__ if hasattr(P.land, "__wrapped__") else P.land))
src = "\n".join(l for l in src.splitlines() if not l.startswith("@"))
# (text the step ends with, label, the array to snapshot)
marks = [
    ("south=noise.line(sh, \"x\", 16, seed=24, amp=5, base=2, clip=(0, 7)))", "outline", "land"),
    ("h = F.terms(Xf, Zf, h, F.Noise(n_small, 0.8), F.Noise(n_big, 1.2))", "base", "h"),
    ("h = np.where(in_reach & (d_r <= w), level + 1, h)", "valley", "h"),
    ("h = np.where(spit < 1.6, np.maximum(h, POND_LEVEL + 1), h)", "pond", "h"),
    ("terrace=(3, 0.45, 0.25))", "ridge", "h"),
    ("h -= 7 * smoothstep(-114, -120, Xf)", "westfall", "h"),
    ("h = LF.level(h, sd, 59, inner=1.0, outer=1.55, mode=\"lift\")", "shoulder", "h"),
    ("h = LF.blend(h, np.full(sh, float(lvl)), np.hypot(Xf - mx, Zf - mz) < r + 8, width=8)", "squares", "h"),
    ("taper=0.7, jag=0.0)", "knoll", "h"),
    ("H, river = LF.watercourse(H, Xf, Zf, riv, width=2 * 3.3, depth=4, water=3, bank=1, fall_min=2, reach_min=4)", "river", "H"),
    ("Hi = np.where(water > 0, np.minimum(Hi, water - 1), Hi)", "waterbeds", "Hi"),
    ("laid |= shapes.polyline(Xf, Zf, pts)[0] <= wdt / 2", "routes", "Hi"),
    ("Hi[L.green] = 50", "plazas", "Hi"),
    ("Hi = funnel", "sinkhole", "Hi"),
    ("Hi = np.where(L.spoil, np.round(LF.mound(Hi, dd, ph_, power=1.6)).astype(int), Hi)", "spoil", "Hi"),
    ("floor=4 + 3 * fbm(sh, 16, 2, seed=52))", "underside", "bottom"),
]
lines = src.splitlines(); out = []
pending = {m[0]: m for m in marks}
for line in lines:
    out.append(line)
    for key, (k, label, var) in list(pending.items()):
        if line.strip().endswith(key) or line.strip() == key:
            out.append("    " + f"_snap({label!r}, {var})")       # every step ends at the function's level
            del pending[key]
assert not pending, pending
STACK = []
def _snap(label, a):
    if STACK and STACK[-1][0] == label: STACK[-1] = (label, np.array(a, float))
    else: STACK.append((label, np.array(a, float)))
TERMS = []
import types
_F = types.SimpleNamespace(**{k: getattr(P.F, k) for k in dir(P.F) if not k.startswith("__")})
def _terms(X, Z, base, *parts):
    TERMS.append((np.array(base, float) if not np.isscalar(base) else float(base), [(type(q).__name__, {k: v for k, v in vars(q).items() if k != "field"}, np.array(q.value(X, Z), float)) for q in parts]))
    return P.F.terms(X, Z, base, *parts)
_F.terms = _terms
ns = dict(vars(P)); ns["_snap"] = _snap; ns["F"] = _F
exec(compile("\n".join(out), "land", "exec"), ns)
L = ns["land"]()
assert np.array_equal(L.H, P.land().H), "the instrumented land() must build the same ground"
pickle.dump(dict(stack=STACK, X=L.X, Z=L.Z, land=L.land, H=L.H, water=L.water, X_MIN=P.X_MIN, Z_MIN=P.Z_MIN, terms=TERMS, places=P.PLACES, sinkhole=P.SINKHOLE, spoil=P.SPOIL),
            open(sys.argv[1], "wb"))
print([s[0] for s in STACK])
