"""What a made structure is written with: the shapes, a theme's five buckets, a stack pinned to world Y, and
`Made` — one thing as named layers, a mass to a layer and one layer per slab height.

The rules it encodes are measured in `designing-a-structure`: two masses touching on one layer fuse, and a
wall inside the fused footprint leaves the perimeter the façade's stripe cycle is counted round; a door is a
one-course sill on the wall's own layer and a lintel on the layer every lintel shares, because an override
floored at the head keeps the wall it stands in.
"""
import math


def by_height(*bands, start=8):
    """A stack pinned to world Y from `start`, so every mass that states it lands its bands at the same
    heights. The last band claims everything past the stack, so a cycle is written out band by band."""
    stack = {"ending": "repeat", "bands": [{"material": m, "thickness": t} for m, t in bands]}
    return {"kind": "layered", "axis": "height", "from": start, "stack": stack}


def theme(wall, rim, surface, fill):
    return {"bedrock": {"relative": False, "value": 1}, "rimEdges": "boundary", "wallOnTerrainFaces": True,
            "rim": {"enabled": True, "depth": 1, "material": rim},
            "surface": {"enabled": True, "depth": 1, "material": surface},
            "wall": wall, "wallEnabled": True, "fill": fill}


def one(material):
    """A theme that answers one material in every bucket — for a thing too thin to have a core."""
    return theme(material, material, material, material)


def rect(shape_id, x0, z0, x1, z1, floor=0, height=1, theme="facade", **words):
    """A rectangle over the cells x0..x1, z0..z1 inclusive."""
    out = {"id": shape_id, "type": "rectangle", "operation": "add", "floor": floor, "base_height": height,
           "min_x": x0, "min_z": z0, "max_x": x1 + 1, "max_z": z1 + 1, "theme": theme}
    out.update(words)
    return out


def disc(shape_id, cx, cz, radius, floor=0, height=1, theme="tank", **words):
    out = {"id": shape_id, "type": "circle", "operation": "add", "floor": floor, "base_height": height,
           "center_x": cx, "center_z": cz, "radius": radius, "theme": theme}
    out.update(words)
    return out


def ring(cx, cz, outer, inner, gap=None, points=64):
    """An annulus as one even-odd outline, or — with `gap`, a (bearing, width in blocks) — a C that leaves
    the gap open: an opening in a round wall is ground nobody drew on, never a subtract."""
    if gap is None:
        def circle(radius, reverse=False):
            order = range(points - 1, -1, -1) if reverse else range(points)
            return [[round(cx + radius * math.cos(2 * math.pi * k / points), 2),
                     round(cz + radius * math.sin(2 * math.pi * k / points), 2)] for k in order]
        out, hole = circle(outer), circle(max(0.5, inner), reverse=True)
        return out + [out[0]] + hole + [hole[0]]
    bearing, width = gap
    def arc(radius, reverse=False):
        half = min(math.pi * 0.95, (width / 2) / max(radius, 0.5))
        a0, a1 = bearing + half, bearing + 2 * math.pi - half
        steps = [a0 + (a1 - a0) * k / points for k in range(points + 1)]
        if reverse:
            steps.reverse()
        return [[round(cx + radius * math.cos(a), 2), round(cz + radius * math.sin(a), 2)] for a in steps]
    return arc(outer) + arc(max(0.5, inner), reverse=True)


def polygon(shape_id, vertices, floor=0, height=1, theme="dome"):
    return {"id": shape_id, "type": "polygon", "operation": "add", "floor": floor, "base_height": height,
            "vertices": vertices, "theme": theme}


class Made:
    """One made thing as named layers. A layer is a mass, or one height's worth of slabs across every mass:
    two masses that touch on one layer fuse, and a wall inside a fused footprint has no place on the
    perimeter, so the façade's stripe cycle reads it as a pier from the ground to the parapet."""

    def __init__(self, name, lintel="lintel", bay=4, storey=5, base_y=8, facade="facade", slab="slab"):
        self.name, self.layers, self.lintel = name, {}, lintel
        self.bay, self.storey, self.base_y, self.facade, self.slab = bay, storey, base_y, facade, slab

    def put(self, layer, *shapes):
        self.layers.setdefault(layer, []).extend(shapes)

    def mass(self, key, x0, z0, bays_x, bays_z, storeys, facade=None, floor=0, slabs="slab"):
        """A block on the module: its walls and ground floor on a layer of its own, one slab a storey on
        the layer every mass's slab at that height shares. A mass standing on another's roof states `floor`
        and its own `slabs` prefix, since its first floor is not at the height the ground masses' is and a
        layer holds one span per column. Answers its cell bounds and wall height."""
        x1, z1 = x0 + bays_x * self.bay, z0 + bays_z * self.bay
        height = storeys * self.storey + 2                  # the storeys, the roof slab and a parapet
        self.put(key, rect(f"{key}-walls", x0, z0, x1, z1, floor=floor, height=height,
                           theme=facade or self.facade),
                 rect(f"{key}-floor", x0 + 1, z0 + 1, x1 - 1, z1 - 1, floor=floor, theme=self.slab,
                      override=True))
        for storey in range(1, storeys + 1):
            self.put(f"{slabs}-{storey}", rect(f"{key}-slab-{storey}", x0 + 1, z0 + 1, x1 - 1, z1 - 1,
                                               floor=floor + storey * self.storey, theme=self.slab))
        return (x0, z0, x1, z1), height

    def door(self, key, layer, x0, z0, x1, z1, top, head=4, floor=0):
        """A sill and a lintel. The sill is a one-course override on the wall's own layer, which replaces the
        wall's column with the floor course; the lintel is the wall above the head, and since that is a
        second span over the same column it goes on the layer every door's lintel shares. An override floored
        at the head would not do both: an override standing in a wall keeps the wall from its own floor."""
        self.put(layer, rect(f"{key}-sill", x0, z0, x1, z1, floor=floor, theme=self.slab, override=True))
        self.put("lintels", rect(f"{key}-lintel", x0, z0, x1, z1, floor=head, height=top - head,
                                 theme=self.lintel))

    def build(self, mirrors=False, seat=None):
        out = []
        for key, shapes in self.layers.items():
            for shape in shapes:
                shape["id"] = f"{self.name}-{shape['id']}"
            layer_id = f"{self.name}-{key}"
            out.append({"id": layer_id, "name": layer_id, "base_y": self.base_y, "kind": "made",
                        "part_of": self.name, **({"seat": seat} if seat else {}),
                        "layout": {"shapes": shapes, "groups": [{"id": layer_id, "name": layer_id,
                                   "mirrors": mirrors, "shapeIds": [s["id"] for s in shapes]}]}})
        return out


