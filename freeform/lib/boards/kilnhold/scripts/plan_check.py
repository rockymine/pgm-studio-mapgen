"""Kilnhold's plan checked before a block is written: the walks the plan states against the destroy-goal rules and the
ramps, rooms and monuments against the numbers the plan gives them.

    python3 plan_check.py        one line per measurement, the value then its target
"""
import plan as P


def ramp_grades():
    """The steepest rise per cell over every ramp the plan states, in blocks: half a block is the target."""
    import kit
    worst = 0.0
    for nm, run, fall, floor, level in (("descent_w", "-x", True, P.GATE, P.DEEP), ("descent_e", "+x", True, P.GATE, P.DEEP),
                                        ("crown_ramp_w", "-x", False, P.MEZ, P.CROWN),
                                        ("crown_ramp_e", "+x", False, P.MEZ, P.CROWN)):
        pa = P.PASSAGES[nm]
        cells = kit.ramp_cells(pa["x"], pa["z"], run, floor, flat=0, fall=fall, level=level)
        height = {}
        for x, z, y, slab in cells:
            height.setdefault((x, z), y + (0.5 if slab else 1.0))
        order = sorted({(x if run[1] == "x" else z) for x, z in height}, reverse=run[0] == "-")
        along = {}
        for (x, z), h in height.items():
            along[x if run[1] == "x" else z] = h
        keys = sorted(along, reverse=run[0] == "-")
        for a, b in zip(keys, keys[1:]):
            worst = max(worst, abs(along[b] - along[a]))
    return worst


def measure():
    own = {k: P.route_length(f"spawn to the {k}") for k in ("Crown Beacon", "Pump Hall Monument", "flag")}
    front = P.route_length("enemy spawn to the gate hall dais")
    enemy = {k: front + P.route_length(f"dais to the {k}") for k in own}
    by_culvert = P.route_length("enemy spawn to the Pump Hall Monument by the culvert")
    by_ramp = P.route_length("enemy spawn to the Crown Beacon by the west ramp")
    by_east = P.route_length("enemy spawn to the flag by the east culvert")
    enemy["Pump Hall Monument"] = min(enemy["Pump Hall Monument"], by_culvert)
    enemy["Crown Beacon"] = min(enemy["Crown Beacon"], by_ramp)
    enemy["flag"] = min(enemy["flag"], by_east)
    return dict(own=own, enemy=enemy, front=front)


def rows(m):
    out = []
    for k, v in m["own"].items():
        goal = k != "flag"
        out.append((v, f"red spawn to the {k}, by the plan's route", "40-90 (a goal's own spawn)" if goal else "info",
                    (40 <= v <= 90) if goal else None))
    for k in ("Crown Beacon", "Pump Hall Monument"):
        r = m["enemy"][k] / m["own"][k]
        out.append((f"{m['enemy'][k]} / {m['own'][k]} = {r:.2f}", f"blue spawn to the {k} over red spawn to it", "3.0-4.0 (GO1)",
                    3.0 <= r <= 4.0))
    r = m["enemy"]["flag"] / m["own"]["flag"]
    out.append((f"{m['enemy']['flag']} / {m['own']['flag']} = {r:.2f}", "blue spawn to the flag over red spawn to it", "info", None))
    beacon_to_sump = (P.route_length("dais to the Crown Beacon") + P.route_length("dais to the Pump Hall Monument") - 2 * 10)
    out.append((beacon_to_sump, "red's two goals apart by the plan's routes (through the dais)", "35-65 (GO2)",
                35 <= beacon_to_sump <= 65))
    grades = ramp_grades()
    out.append((f"{grades:g}", "steepest rise a cell on any interior ramp, in blocks", "at most 0.5", grades <= 0.5 + 1e-9))
    for name, (x0, x1, z0, z1, floor, h) in P.ROOMS.items():
        out.append((h, f"{name}: height of air over its floor", "at least 5", h >= 5)) if name in ("gate_hall", "muster") else None
    box = P.monument_box(P.BEACON_AT, P.CROWN)
    out.append((box.y0 - P.CROWN - 1, "air under the Crown Beacon", "at least 3", box.y0 - P.CROWN - 1 >= 3))
    box = P.monument_box(P.PUMP_AT, P.DEEP)
    out.append((box.y0 - P.DEEP - 1, "air under the Pump Hall Monument", "at least 3", box.y0 - P.DEEP - 1 >= 3))
    img = P.objectives()
    beacons = [o for o in img.items if getattr(o, "id", "").endswith("beacon")]
    a, b = beacons[0].box, beacons[1].box
    exact = (a.x0 + b.x1 == -1 and a.z0 + b.z1 == -1 and a.y0 == b.y0)
    out.append(("exact" if exact else "off", "the monuments are each other's half turn", "exact", exact))
    return out


if __name__ == "__main__":
    m = measure()
    for v, what, target, ok in rows(m):
        print(f"{'  ' if ok or ok is None else '! '}{str(v):>16}  {what}  (target {target})")
