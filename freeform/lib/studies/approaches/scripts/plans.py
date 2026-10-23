"""The eight approach forms drawn in plan as the studio draws them: ground, the room, the host past the mouth, the
voids a form leaves (cut as shafts when laid underground) and the seams its defence walls stand on.

    python3 plans.py                   # renders/forms.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                               # noqa: E402
from matplotlib.patches import Rectangle                                      # noqa: E402

from pgmvox.built import chambers as CH                                       # noqa: E402
from pgmvox.plan import approach as AP                                        # noqa: E402
from approaches import SIZES                                                  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders", "forms.png")
fig, axes = plt.subplots(2, 4, figsize=(16, 9))
fig.patch.set_facecolor("#16181d")
for ax, form in zip(axes.flat, AP.FORMS):
    a = AP.emit(form, *SIZES[form])
    cells, room, host, void = a.cells(), a.room, a.host(), CH._bays(a)
    floors, _, _ = CH.floors(a, 0, 1)
    ax.set_facecolor("#16181d")
    for (i, j) in cells:
        shade = 0.75 - 0.12 * (-floors[(i, j)])
        ax.add_patch(Rectangle((i, j), 1, 1, fc=(0.45, shade, 0.4) if (i, j) not in room else "#e0b030", ec="#16181d"))
    for (i, j) in host:
        ax.add_patch(Rectangle((i, j), 1, 1, fc="#4a78c8", ec="#16181d"))
    for (i, j) in void:
        ax.add_patch(Rectangle((i, j), 1, 1, fc="#000000", ec="#3a3f4a", hatch="////"))
    for e in AP.walls(a):
        p, q = sorted(tuple(e))
        if p[0] != q[0]:
            ax.plot([q[0], q[0]], [q[1], q[1] + 1], color="#ff5050", lw=5)
        else:
            ax.plot([q[0], q[0] + 1], [q[1], q[1]], color="#ff5050", lw=5)
    for k, p in enumerate(a.parts):
        cs = p.cells()
        ci = sum(c[0] for c in cs) / len(cs) + 0.5
        cj = sum(c[1] for c in cs) / len(cs) + 0.5
        ax.text(ci, cj, p.name, ha="center", va="center", fontsize=7, color="#101010")
    allc = cells | host | void
    ax.set_xlim(min(c[0] for c in allc) - 0.5, max(c[0] for c in allc) + 1.5)
    ax.set_ylim(max(c[1] for c in allc) + 1.5, min(c[1] for c in allc) - 0.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"{form}: reads {AP.classify(cells, room)}, {AP.doors(a)} way{'s' if AP.doors(a) > 1 else ''} in, "
                 f"{len(AP.walls(a))} wall{'s' if len(AP.walls(a)) > 1 else ''}", color="#e8e8e8", fontsize=10)
fig.suptitle("the studio's approach forms: blue the host, green the ground (darker a storey lower), gold the room, "
             "hatched the void, red the walls", color="#e8e8e8", fontsize=11)
plt.tight_layout()
plt.savefig(OUT, dpi=110, facecolor=fig.get_facecolor())
print("drew", OUT)
