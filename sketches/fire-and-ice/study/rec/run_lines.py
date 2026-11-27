import os, sys, pickle, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, sys.argv[2])
from pieces import load
from reconstruct import score
from lines import fit_lofts, components
pieces, every = load(sys.argv[1])
PAIRING = sys.argv[3] if len(sys.argv) > 3 else "arc"
rebuilt_all, rows, per_piece = {}, [], []
for k, piece in enumerate(pieces):
    t0 = time.time()
    marks = [p for p, _ in piece["marks"]]
    main = fit_lofts(piece["cells"], marks, pairing=PAIRING)
    built = main["lofts"].build(main["frame"], main["window"])
    free = []
    for comp in components(main["extra"]):
        compset = set(comp)
        own = [p for p in marks if any((p[0] + a, p[1] + b, p[2] + e) in compset for a in (-1, 0, 1) for b in (-1, 0, 1) for e in (-1, 0, 1))]
        f = fit_lofts(comp, own, pairing=PAIRING)
        built |= f["lofts"].build(f["frame"], f["window"]); free.append(f)
    ex, rec, prec = score(piece["cells"], built)
    per_piece.append(built)
    for c in built: rebuilt_all.setdefault(c, piece["colour"])
    lines = main["lines"] + sum(f["lines"] for f in free); points = main["points"] + sum(f["points"] for f in free)
    print(f"{k:2d} {piece['colour']:6s} {len(piece['cells']):5d} -> {len(built):5d} | lines along {'uv'[main['lofts'].along]}: "
          f"{main['lines']:3d} lines ({main['marker_lines']} at markers, {main['edge_lines']} at edge bends, {main['height_lines']} at height bends), {main['points']:4d} points ({main['markers']} markers)"
          + (f" + {len(free)} free lofts ({sum(f['lines'] for f in free)} lines)" if free else "")
          + f" | exact {ex:5.1%}  original within 1: {rec:5.1%}  rebuilt within 1: {prec:5.1%}  ({time.time()-t0:.0f}s)", flush=True)
    rows.append((k, piece["colour"], ex, rec, prec, lines, points))
pickle.dump({"rebuilt": rebuilt_all, "pieces": [(p["colour"], p["cells"]) for p in pieces], "rows": rows, "per_piece": per_piece},
            open(sys.argv[2] + f"/rebuilt_lines_{PAIRING}.pkl", "wb"))
