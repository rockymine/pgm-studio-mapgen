"""Write the test grounds export_slopes.cs reads: ramps, a staircase, a cliff, noise, and holes.

    python3 pgmvox/data/slope_cases.py cases.json
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pgmvox import noise  # noqa: E402


def write(path, seed=5):
    rng = np.random.default_rng(seed)
    X, Z = np.meshgrid(np.arange(24), np.arange(20), indexing="ij")
    grounds = [X // 1, X // 2, X // 3, (X + Z) // 2, np.where(X > 11, 40, 34), 30 + 6 * noise.fbm((24, 20), 6, 3, seed=1),
               30 + 18 * noise.fbm((24, 20), 4, 3, seed=2), rng.integers(20, 40, (24, 20))]
    cases = []
    for k, g in enumerate(grounds):
        g = np.asarray(g).astype(int)
        hole = (np.hypot(X - 12, Z - 10) < 4) if k % 2 else (X + 2 * Z) % 11 == 0
        for m in (np.ones(g.shape, bool), ~hole):
            cases.append([[int(g[i, j]) if m[i, j] else None for j in range(g.shape[1])] for i in range(g.shape[0])])
    with open(path, "w") as f:
        json.dump(cases, f)


if __name__ == "__main__":
    write(sys.argv[1])
