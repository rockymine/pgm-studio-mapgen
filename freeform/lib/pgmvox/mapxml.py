"""Writing a PGM map.xml: an element builder and the pieces every board's writer repeated.

    d = Doc("Spark", "1.0.0", "Knock the other players off!", "blitz")
    d.players(2, 64)
    d.root.append(E("kits", E("kit", E("item", slot=0, material="stick"), id="stick")))
    d.spawns(E("spawn", E("regions", point(0.5, 65, 0.5, yaw=90)), kit="stick"), default=point(0.5, 90, 0.5))
    d.kill_below(40)
    d.time(5 * 60); d.blitz(lives=1); d.no_fall_damage(); d.no_hunger(); d.lock_time(6000)
    d.write("map.xml")

E(tag, *children, text=None, **attrs) makes an element; attribute names with a trailing underscore lose it
(class_=), and underscores in the middle become hyphens (max_overfill= -> max-overfill). The rules of play are
the board's; this module only spares it the boilerplate. For a mode the studio supports, its intent document
and codec are the better writer.
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
        if gamemode:
            self.root.append(E("gamemode", text=gamemode))

    def add(self, el):
        self.root.append(el)
        return el

    def rules(self, *lines):
        return self.add(E("rules", [E("rule", text=s) for s in lines]))

    def players(self, lo, hi, colors=True):
        return self.add(E("players", min=lo, max=hi, colors=colors))

    def teams(self, *teams):
        """teams: (id, colour, max, display name)."""
        return self.add(E("teams", [E("team", text=name, id=tid, color=col, max=mx) for tid, col, mx, name in teams]))

    def spawns(self, *spawns, default=None):
        kids = list(spawns)
        if default is not None:
            kids.append(E("default", E("region", default)) if default.tag != "default" else default)
        return self.add(E("spawns", kids))

    def kill_below(self, y):
        """A portal that sends anyone below y into the void, the way the arcade boards end a fall."""
        return self.add(E("portals", E("portal", E("region", below(y)), y="@-64", sound=False, observers="never")))

    def time(self, seconds, result=None):
        return self.add(E("time", text=duration(seconds), result=result))

    def blitz(self, lives=1, filter_=None):
        return self.add(E("blitz", E("lives", text=lives), filter=filter_))

    def no_fall_damage(self):
        return self.add(E("disabledamage", E("damage", text="fall")))

    def no_hunger(self):
        return self.add(E("hunger", E("depletion", text="off")))

    def lock_time(self, ticks=6000):
        return self.add(E("world", E("timeset", text=ticks), E("timelock", text="on")))

    def broadcasts(self, *items):
        """items: ("alert" or "tip", after seconds, text)."""
        return self.add(E("broadcasts", [E(kind, text=text, after=duration(t)) for kind, t, text in items]))

    def itemremove(self, *materials):
        return self.add(E("itemremove", [E("item", text=m) for m in materials]))

    def tostring(self):
        raw = ET.tostring(self.root, encoding="unicode")
        return minidom.parseString(raw).toprettyxml(indent="    ").split("\n", 1)[1]

    def write(self, path):
        with open(path, "w") as f:
            f.write(self.tostring())
        return path
