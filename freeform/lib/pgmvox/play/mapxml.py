"""The element builder the typed parts of a map write through: `play.rules.Map` and `play.objectives` call it, a
board does not.

    d = Doc("Spark", "1.0.0", "Knock the other players off!", "blitz")
    d.region("pad", cuboid((0, 64, 0), (2, 65, 2))); d.apply(region="pad", velocity="0,2,0")
    print(d.tostring())

E(tag, *children, text=None, **attrs) makes an element; attribute names with a trailing underscore lose it
(class_=), and underscores in the middle become hyphens (max_overfill= -> max-overfill).
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom


def _attr(k):
    return k.rstrip("_").replace("_", "-")


def E(tag, *children, text=None, **attrs):
    el = ET.Element(tag, {_attr(k): _fmt(v) for k, v in attrs.items() if v is not None})
    for c in children:
        if c is None:
            continue
        if isinstance(c, (list, tuple)):
            for cc in c:
                el.append(cc)
        else:
            el.append(c)
    if text is not None:
        el.text = str(text)
    return el


def _fmt(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def point(x, y, z, **attrs):
    return E("point", text=f"{_fmt(x)},{_fmt(y)},{_fmt(z)}", **attrs)


def cuboid(min_, max_, **attrs):
    """A cuboid from block-corner min to max (max exclusive, as PGM reads a cuboid's bounds)."""
    return E("cuboid", min=",".join(_fmt(v) for v in min_), max=",".join(_fmt(v) for v in max_), **attrs)


def cylinder(base, radius, height, **attrs):
    return E("cylinder", base=",".join(_fmt(v) for v in base), radius=radius, height=height, **attrs)


def circle(center, radius, **attrs):
    return E("circle", center=",".join(_fmt(v) for v in center), radius=radius, **attrs)


def below(y, **attrs):
    return E("below", y=y, **attrs)


def negative(*children, **attrs):
    return E("negative", *children, **attrs)


def union(*children, **attrs):
    return E("union", *children, **attrs)


def duration(seconds):
    """PGM's duration text: 90 -> "1m30s"."""
    m, s = divmod(int(seconds), 60)
    return (f"{m}m" if m else "") + (f"{s}s" if s or not m else "")


class Doc:
    def __init__(self, name, version, objective, gamemode=None, proto="1.5.0"):
        self.root = E("map", proto=proto)
        self.root.append(E("name", text=name))
        self.root.append(E("version", text=version))
        self.root.append(E("objective", text=objective))
        for mode in ([gamemode] if isinstance(gamemode, str) else gamemode or []):
            self.root.append(E("gamemode", text=mode))           # one tag each: a board may mix modes

    def add(self, el):
        self.root.append(el)
        return el

    def child(self, *path, **attrs):
        """The element at a path of tags under <map>, made on first use with attrs: doc.child("king", "hills")."""
        el = self.root
        for k, tag in enumerate(path):
            found = el.find(tag)
            if found is None:
                found = ET.SubElement(el, tag, {_attr(a): _fmt(v) for a, v in attrs.items() if v is not None}
                                      if k == len(path) - 1 else {})
            el = found
        return el

    def ids(self):
        return {e.get("id") for e in self.root.iter() if e.get("id")}

    def region(self, id_, el):
        """A named region under <regions>: el is a shape element (cuboid, block, point, union ...) given the id.
        An id already taken is refused, since a duplicate silently re-points every reference to it."""
        if id_ in self.ids():
            raise ValueError(f"region id {id_!r} is taken")
        el.set("id", id_)
        self.child("regions").append(el)
        return id_

    def filter(self, id_, el):
        """A named filter under <filters>; an id given twice with the same filter is kept once."""
        existing = self.root.find(f".//filters/*[@id='{id_}']")
        if existing is not None:
            return id_
        el.set("id", id_)
        self.child("filters").append(el)
        return id_

    def apply(self, **attrs):
        """An applicator under <regions>: doc.apply(enter="only-red", region="red-spawn", message="...")."""
        el = E("apply", **attrs)
        self.child("regions").append(el)
        return el

    def teams(self, *teams):
        """teams: (id, colour, max, display name)."""
        return self.add(E("teams", [E("team", text=name, id=tid, color=col, max=mx) for tid, col, mx, name in teams]))

    def kit(self, id_, *items, force=None, **attrs):
        """A kit under <kits>: doc.kit("spawn-kit", *elements)."""
        el = E("kit", *items, id=id_, force=force, **attrs)
        self.child("kits").append(el)
        return el

    def tostring(self):
        raw = ET.tostring(self.root, encoding="unicode")
        return minidom.parseString(raw).toprettyxml(indent="    ").split("\n", 1)[1]

    def write(self, path):
        with open(path, "w") as f:
            f.write(self.tostring())
        return path
