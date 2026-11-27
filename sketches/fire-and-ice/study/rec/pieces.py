"""Shared loader for the reconstruction study: the author's terrain split into pieces, each with its loft markers."""
import os, sys, collections
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools")))
from anvil import World

COLOUR = {(35, 3): "blue", (35, 4): "yellow", (35, 5): "lime", (35, 13): "green", (35, 8): "floor"}
MARK = {41: "gold", 57: "diamond", 133: "emerald", 42: "iron"}

def load(region):
    w = World(region)
    cells, marks, every = {}, [], {}
    for x, y, z, i, d in w.blocks():
        every[(x, y, z)] = (i, d)
        if not (-20 <= x <= 110 and -60 <= z <= 105): continue
        if (i, d) in COLOUR: cells[(x, y, z)] = COLOUR[(i, d)]
        if i in MARK: marks.append(((x, y, z), MARK[i]))
    pieces = []
    for colour in ("floor", "yellow", "blue", "lime", "green"):
        pts = {c for c, v in cells.items() if v == colour}
        seen = set()
        for c in sorted(pts):
            if c in seen: continue
            stack, comp = [c], []
            seen.add(c)
            while stack:
                p = stack.pop(); comp.append(p)
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        for dz in (-1, 0, 1):
                            q = (p[0] + dx, p[1] + dy, p[2] + dz)
                            if q in pts and q not in seen: seen.add(q); stack.append(q)
            ys = {p[1] for p in comp}
            if len(comp) < 60 or (colour == "floor" and len(ys) == 1): continue   # roof plates and scraps
            comp_set = set(comp)
            own = [(p, m) for p, m in marks if any((p[0] + a, p[1] + b, p[2] + e) in comp_set
                                                   for a in (-1, 0, 1) for b in (-1, 0, 1) for e in (-1, 0, 1))]
            pieces.append({"colour": colour, "cells": comp_set, "marks": own})
    return pieces, every
