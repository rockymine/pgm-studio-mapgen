"""Objectives that write themselves: each one stamps its blocks, names the cells it stands on, writes its own regions
and XML into a `mapxml.Doc`, and reads the built world back to say whether it came out playable.

    teams = Teams(("red-team", "Red", "red"), ("blue-team", "Blue", "blue"))
    O = Objectives(teams, Symmetry("half"))
    O.add(Spawn("red-team", (-24, 31, 0), yaw=-90, area=Box(-25, 31, -2, -22, 34, 1)))   # and blue's, turned
    O.add(Hill("hill", "the Hill", Box(-2, 33, -4, 1, 33, 3)), mirror=False)              # one, in the middle
    O.add(Wool("blue-team", "lime", slot=(-40, 31, 5)))                                   # and its image
    O.stamp(w); O.write(doc); print(O.check(w))

**The XML is the studio's shape.** Control points are written with the long attribute names the studio's writer
uses (`capture-region`, `progress-display-region`, `owner-display-region`) and the defaults its generator chose
from the corpus: not required, neutral state, incremental, progress shown, no crowd multiplier, with a score
limit beside them so the points count. Destroyables and cores name a `{id}-region`; a wool's monument is a named
`<block>` region. Proto 1.5.0, as every board and the studio write.

**Regions follow one convention.** A `Box` is inclusive blocks and is written with an exclusive max, because a
PGM cuboid spans `[min, max)`; a point is a block and is written at its centre (x + 0.5, y, z + 0.5), where a
player stands.

**Symmetry is drawn once.** `Objectives.add(obj)` adds the objective and, when it is a team's, its image under
the plan's `Symmetry` for the other team: its boxes and points turned, its yaws turned, its team and id swapped.
A neutral objective on the axis is added with `mirror=False`.
"""
import math
from dataclasses import dataclass, fields, replace

from .blocks import B, PASSABLE
from .mapxml import E, point as point_el
from .orient import OPS

DYES = {"white": 0, "orange": 1, "magenta": 2, "light_blue": 3, "yellow": 4, "lime": 5, "pink": 6, "gray": 7,
        "silver": 8, "light_gray": 8, "cyan": 9, "purple": 10, "blue": 11, "brown": 12, "green": 13, "red": 14,
        "black": 15}


# ---- geometry ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Box:
    """Inclusive blocks: Box(0, 10, 0, 3, 12, 3) is four by three by four."""
    x0: int
    y0: int
    z0: int
    x1: int
    y1: int
    z1: int

    def __post_init__(self):
        a, b = sorted((self.x0, self.x1)); c, d = sorted((self.y0, self.y1)); e, f = sorted((self.z0, self.z1))
        object.__setattr__(self, "x0", a); object.__setattr__(self, "x1", b)
        object.__setattr__(self, "y0", c); object.__setattr__(self, "y1", d)
        object.__setattr__(self, "z0", e); object.__setattr__(self, "z1", f)

    def cuboid(self):
        """The PGM cuboid, max exclusive."""
        return E("cuboid", min=f"{self.x0},{self.y0},{self.z0}", max=f"{self.x1 + 1},{self.y1 + 1},{self.z1 + 1}")

    def blocks(self):
        return [(x, y, z) for x in range(self.x0, self.x1 + 1) for y in range(self.y0, self.y1 + 1)
                for z in range(self.z0, self.z1 + 1)]

    def cells(self):
        return {(x, z) for x in range(self.x0, self.x1 + 1) for z in range(self.z0, self.z1 + 1)}

    def centre(self):
        return ((self.x0 + self.x1 + 1) / 2, (self.z0 + self.z1 + 1) / 2)

    def course(self, y0, y1=None):
        """The same plan at other heights."""
        return Box(self.x0, y0, self.z0, self.x1, y1 if y1 is not None else y0, self.z1)

    def image(self, sym):
        a = sym.point(self.x0, self.z0)
        b = sym.point(self.x1, self.z1)
        return Box(int(a[0]), self.y0, int(a[1]), int(b[0]), self.y1, int(b[1]))


def turn_point(p, sym):
    x, z = sym.point(p[0], p[2])
    return (int(x), p[1], int(z))


def turn_yaw(yaw, sym):
    """A yaw (0 south, 90 west) carried through a symmetry."""
    if yaw is None:
        return None
    t = math.radians(yaw)
    dx, dz = OPS[sym.op](-math.sin(t), math.cos(t))
    return int(round(math.degrees(math.atan2(-dx, dz)))) % 360


def centre_el(p, **attrs):
    """A point element at a block's centre, where a player stands in it."""
    return point_el(p[0] + 0.5, p[1], p[2] + 0.5, **attrs)


def _stands(w, p):
    """Whether a player can stand with their feet in block p: the two blocks passable, the one under not."""
    x, y, z = p
    return (w.inside(x, y - 1, z) and w.id(x, y, z) in PASSABLE and w.id(x, y + 1, z) in PASSABLE
            and w.id(x, y - 1, z) not in PASSABLE)


# ---- teams ------------------------------------------------------------------------------------------------
class Teams:
    """The teams, as (id, name, colour) or (id, name, colour, max players; 8 if not given). Two teams swap
    under the board's symmetry."""

    def __init__(self, *teams):
        self.teams = [tuple(t[:3]) for t in teams]
        self.max = {t[0]: (t[3] if len(t) > 3 else 8) for t in teams}

    def other(self, team):
        ids = [t[0] for t in self.teams]
        if team is None or len(ids) != 2 or team not in ids:
            return team
        return ids[1 - ids.index(team)]

    def next(self, team, k=1):
        """The team k after this one in the order given, round again past the last: the team a quarter turn
        carries a part to. For two teams it is the other."""
        ids = [t[0] for t in self.teams]
        if team is None or team not in ids:
            return team
        return ids[(ids.index(team) + k) % len(ids)]

    def short(self, team):
        return team[:-5] if team and team.endswith("-team") else team

    def write(self, doc):
        doc.teams(*[(tid, colour, self.max[tid], name) for tid, name, colour in self.teams])
        for tid, _, _ in self.teams:
            doc.filter(f"only-{self.short(tid)}", E("team", text=tid))
            doc.filter(f"not-{self.short(tid)}", E("not", E("team", text=tid)))


# ---- the objectives ---------------------------------------------------------------------------------------
class Objective:
    def image(self, sym, teams):
        """This objective for the next team, through the symmetry: the other team of two, or under a quarter turn
        the team after it in the order the teams were given."""
        new = self.turned(sym)
        team = getattr(self, "team", None)
        other = teams.next(team)
        changes = {}
        if team is not None:
            changes["team"] = other
        if getattr(self, "keeper", None):
            changes["keeper"] = teams.next(self.keeper)
        if "id" in {f.name for f in fields(self)} and self.id and team and teams.short(team) in self.id:
            changes["id"] = self.id.replace(teams.short(team), teams.short(other))
        return replace(new, **changes) if changes else new

    def turned(self, sym):
        return self

    def stamp(self, w):
        pass

    def write(self, doc, teams):
        pass

    def check(self, w):
        return []

    def cells(self):
        return set()

    def marker(self):
        """(x, z, letter) for the sketch, or None."""
        return None


@dataclass
class Spawn(Objective):
    """A team's spawn: the block their feet stand in, the way they face, a kit, and the area kept to them.
    protect: True keeps every block of the area as it is; a tuple of material names lets those be mined there
    and grow back (a spawn's iron), everything else kept; False writes no rule."""
    team: str
    at: tuple
    yaw: int = 0
    kit: str = None
    area: Box = None
    protect: object = True

    def turned(self, sym):
        return replace(self, at=turn_point(self.at, sym), yaw=turn_yaw(self.yaw, sym),
                       area=self.area.image(sym) if self.area else None)

    def write(self, doc, teams):
        doc.child("spawns").append(E("spawn", E("region", centre_el(self.at)), team=self.team, kit=self.kit,
                                     yaw=self.yaw))
        if self.area:
            rid = doc.region(f"{teams.short(self.team)}-spawn", self.area.cuboid())
            if self.protect:
                others = [t for t, _, _ in teams.teams if t != self.team]
                if others:
                    doc.apply(enter=f"only-{teams.short(self.team)}", region=rid,
                              message="You may not enter the enemy spawn!")
                if isinstance(self.protect, (tuple, list)):
                    mats = E("any", *[E("material", text=m) for m in self.protect])
                    doc.filter("spawn-minable", mats)
                    doc.filter("spawn-minable-regrowth", E("all", E("filter", id="spawn-minable"),
                                                          E("cause", text="world")))
                    doc.apply(block_place="spawn-minable-regrowth", block_break="spawn-minable", region=rid,
                              message="You may not edit the spawn!")
                    doc.child("renewables").append(E("renewable", region=rid, renew_filter="spawn-minable"))
                else:
                    doc.apply(block="never", region=rid, message="You may not build in a spawn!")

    def check(self, w):
        return [] if _stands(w, self.at) else [f"{self.team} spawn at {self.at}: nowhere to stand"]

    def cells(self):
        return self.area.cells() if self.area else {(self.at[0], self.at[2])}

    def marker(self):
        return (self.at[0], self.at[2], "S")


@dataclass
class Observer(Objective):
    """Where observers and the dead appear: <default> in <spawns>."""
    at: tuple
    yaw: int = 0

    def write(self, doc, teams):
        doc.child("spawns").append(E("default", E("region", centre_el(self.at)), yaw=self.yaw))


@dataclass
class Hill(Objective):
    """A control point (King of the Hill): a pad one course thick and the box over it a player captures in.
    The pad is the progress and the owner display, as the boards drew it."""
    id: str
    name: str
    pad: Box
    capture_height: int = 5
    points: int = 1
    capture_time: str = "5s"
    block: tuple = None                  # the pad's block when stamped; None leaves the ground as built
    team: str = None

    def turned(self, sym):
        return replace(self, pad=self.pad.image(sym))

    def capture_box(self):
        return self.pad.course(self.pad.y0, self.pad.y0 + self.capture_height - 1)

    def stamp(self, w):
        if self.block:
            for x, y, z in self.pad.blocks():
                w.set(x, y, z, *self.block)

    def write(self, doc, teams):
        cap = doc.region(f"{self.id}-capture", self.capture_box().cuboid())
        pad = doc.region(f"{self.id}-pad", self.pad.cuboid())
        hills = doc.child("king", "hills", required=False, neutral_state=True, incremental=True, show_progress=True,
                          time_multiplier=0, permanent=False)
        hills.append(E("hill", id=self.id, name=self.name, capture_region=cap, progress_display_region=pad,
                       owner_display_region=pad, capture_time=self.capture_time, points=self.points))
        doc.child("score")

    def check(self, w):
        bad = []
        cap = self.capture_box()
        floor = [w.id(x, cap.y0 - 1, z) not in PASSABLE or w.id(x, cap.y0, z) not in PASSABLE for x, z in cap.cells()]
        if not all(floor):
            bad.append(f"hill {self.id}: {floor.count(False)} of its columns have nothing to stand on")
        return bad

    def cells(self):
        return self.pad.cells()

    def marker(self):
        x, z = self.pad.centre()
        return (int(x), int(z), "A")


@dataclass
class Flag(Objective):
    """A flag and its posts (CTF, King of the Flag): each post a block the flag stands in, named, with a yaw."""
    id: str
    name: str
    color: str
    posts: list                          # [(name, (x, y, z), yaw)]
    shared: bool = True
    points_rate: float = 1
    respawn_time: str = "15s"
    return_time: str = "0s"
    team: str = None

    def turned(self, sym):
        return replace(self, posts=[(n, turn_point(p, sym), turn_yaw(y, sym)) for n, p, y in self.posts])

    def write(self, doc, teams):
        posts = E("post", *[E("post", text=f"{p[0] + 0.5},{p[1]},{p[2] + 0.5}", name=n, yaw=y)
                            for n, p, y in self.posts], return_time=self.return_time, respawn_time=self.respawn_time)
        doc.child("flags").append(E("flag", posts, id=self.id, name=self.name, color=self.color,
                                    shared=self.shared, points_rate=self.points_rate, owner=self.team))
        doc.child("score")

    def check(self, w):
        return [f"flag {self.id}: post {n} at {p} has nowhere to stand" for n, p, _ in self.posts if not _stands(w, p)]

    def cells(self):
        return {(p[0], p[2]) for _, p, _ in self.posts}

    def marker(self):
        _, p, _ = self.posts[0]
        return (p[0], p[2], "F")


@dataclass
class Wool(Objective):
    """A wool to capture (CTW). `team` is the team that captures it, so it is the other team that keeps it: the
    wool lies at `found` in the keepers' `room`, and `team` places it at `slot` on its own side, the air cell over a
    bedrock pedestal with the dyed glass over it, as the studio stamps a monument. Drawn once, its image is the
    other team's wool of another colour: O.add(Wool("blue-team", "lime", slot, found, room), color="magenta").

    It stamps its monument and its wool; writes the wool, its monument, the room's entry rule, and with `spawner`
    a spawner giving the wool to a player in the room (at spawn_at, default over `found`); and its check looks for
    the slot and the wool. Objectives.write adds each team's rooms' block protection (protect_room)."""
    team: str
    color: str
    slot: tuple
    found: tuple = None
    room: Box = None                     # the room the wool is kept in; its keepers are not the team placing it
    spawner: bool = True
    spawn_at: tuple = None
    delay: str = "1.5s"
    protect_room: bool = True
    keeper: str = None                   # the team keeping it: the other team of two; name it for more than two

    def turned(self, sym):
        return replace(self, slot=turn_point(self.slot, sym), found=turn_point(self.found, sym) if self.found else None,
                       room=self.room.image(sym) if self.room else None,
                       spawn_at=turn_point(self.spawn_at, sym) if self.spawn_at else None)

    def keeper_of(self, teams):
        return self.keeper or teams.other(self.team)

    @property
    def id(self):
        return f"{self.color}-monument"

    def stamp(self, w):
        x, y, z = self.slot
        w.set(x, y - 1, z, B.BEDROCK)
        w.set(x, y, z, B.AIR)
        w.set(x, y + 1, z, B.STAINED_GLASS, DYES[self.color])
        if self.found:
            w.set(*self.found, B.WOOL, DYES[self.color])

    def write(self, doc, teams):
        mid = doc.region(f"{self.color}-{teams.short(self.team)}-monument",
                         E("block", text=f"{self.slot[0]},{self.slot[1]},{self.slot[2]}"))
        loc = self.found or self.slot
        doc.child("wools", craftable=False).append(
            E("wool", team=self.team, color=self.color.replace("_", " "), monument=mid,
              location=f"{loc[0] + 0.5},{loc[1]},{loc[2] + 0.5}"))
        if self.room and f"{self.color}-room" not in doc.ids():   # a wool three teams capture has one room
            keeper = self.keeper_of(teams)
            rid = doc.region(f"{self.color}-room", self.room.cuboid())
            doc.apply(enter=f"not-{teams.short(keeper)}", region=rid, message="You may not enter your own wool room!")
            if self.spawner and self.found:
                sx, sy, sz = self.spawn_at or (self.found[0], self.found[1] + 1, self.found[2])
                doc.region(f"{self.color}-wool-spawn", point_el(sx + 0.5, sy, sz + 0.5))
                doc.child("spawners").append(E("spawner", E("item", material="wool", damage=DYES[self.color]),
                                               spawn_region=f"{self.color}-wool-spawn", player_region=rid,
                                               delay=self.delay))

    def check(self, w):
        x, y, z = self.slot
        bad = []
        if w.id(x, y, z) != B.AIR:
            bad.append(f"wool {self.color}: the monument slot {self.slot} is not air")
        if w.id(x, y - 1, z) in PASSABLE:
            bad.append(f"wool {self.color}: nothing under the slot to place on")
        if self.found and w.get(*self.found) != (B.WOOL, DYES[self.color]):
            bad.append(f"wool {self.color}: no wool at {self.found}")
        return bad

    def cells(self):
        return {(self.slot[0], self.slot[2])}

    def marker(self):
        out = [(self.slot[0], self.slot[2], "W")]
        if self.found:
            out.append((self.found[0], self.found[2], "w"))                # the room, in its wool's place
        return out


WOOLROOM_MATERIALS = ("wood", "stained clay", "web")


def wool_rooms(doc, teams, wools, materials=WOOLROOM_MATERIALS):
    """Each keeping team's rooms in one region, and their blocks kept from the other team except what an attacker
    brings in: `materials`, and water a player places."""
    if not any(o.room and o.protect_room for o in wools):
        return
    doc.filter("woolroom-materials", E("any", *[E("material", text=m) for m in materials],
                                       E("all", E("cause", text="player"),
                                         E("any", E("material", text="water"), E("material", text="stationary water")))))
    for keeper, _, _ in teams.teams:
        rooms = [o for o in wools if o.room and o.protect_room and o.keeper_of(teams) == keeper]
        rooms = list({o.color: o for o in rooms}.values())
        if not rooms:
            continue
        t = teams.short(keeper)
        doc.region(f"{t}s-woolrooms", E("union", *[E("region", id=f"{o.color}-room") for o in rooms]))
        doc.filter(f"{t}s-woolrooms-filter", E("all", E("filter", id=f"not-{t}"), E("filter", id="woolroom-materials")))
        doc.apply(block=f"{t}s-woolrooms-filter", region=f"{t}s-woolrooms", message="You may not edit the wool room!")


FLOAT = 3                                # a monument or core hangs this many blocks of air over the floor under it


def float_problems(kind, oid, box, w, least=FLOAT):
    """The author's rule: a monument or core never stands on the floor; it floats, `least` blocks of clear air
    between its lowest block and whatever is under it, in every column of it."""
    low = []
    for x in range(box.x0, box.x1 + 1):
        for z in range(box.z0, box.z1 + 1):
            ys = [y for y in range(box.y0, box.y1 + 1) if w.id(x, y, z) != B.AIR]
            if not ys:
                continue
            air = 0
            y = min(ys) - 1
            while y > 0 and w.id(x, y, z) == B.AIR:
                air += 1
                y -= 1
            if air < least:
                low.append(air)
    return [f"{kind} {oid}: {min(low)} of air under it, not {least}: it must float over the floor"] if low else []


@dataclass
class Destroyable(Objective):
    """A monument to break (DTM): a box of its material, owned by the team defending it. `heart` is a block for the
    box's middle that is not its material, as bedrock at the centre of a three-cube, so the monument cannot be
    tunnelled through its core."""
    id: str
    name: str
    team: str
    box: Box
    material: tuple = (B.OBSIDIAN, 0)
    materials: str = "obsidian"
    completion: str = "100%"
    heart: tuple = None

    def turned(self, sym):
        return replace(self, box=self.box.image(sym))

    def middle(self):
        b = self.box
        return ((b.x0 + b.x1) // 2, (b.y0 + b.y1) // 2, (b.z0 + b.z1) // 2)

    def stamp(self, w):
        for x, y, z in self.box.blocks():
            w.set(x, y, z, *self.material)
        if self.heart:
            w.set(*self.middle(), *self.heart)

    def write(self, doc, teams):
        rid = doc.region(f"{self.id}-region", self.box.cuboid())
        doc.child("destroyables").append(E("destroyable", id=self.id, name=self.name, owner=self.team,
                                           materials=self.materials, completion=self.completion, mode_changes=True,
                                           region=rid))

    def check(self, w):
        wrong = [p for p in self.box.blocks() if w.get(*p)[0] != self.material[0]
                 and not (self.heart and p == self.middle() and w.get(*p)[0] == self.heart[0])]
        bad = [f"destroyable {self.id}: {len(wrong)} blocks of its box are not its material"] if wrong else []
        return float_problems("destroyable", self.id, self.box, w) + bad

    def cells(self):
        return self.box.cells()

    def marker(self):
        x, z = self.box.centre()
        return (int(x), int(z), "M")


@dataclass
class Core(Objective):
    """A core to leak (DTC): an obsidian shell round lava, owned by the team defending it."""
    id: str
    name: str
    team: str
    box: Box
    leak: int = 5

    def turned(self, sym):
        return replace(self, box=self.box.image(sym))

    def stamp(self, w):
        b = self.box
        for x, y, z in b.blocks():
            inner = b.x0 < x < b.x1 and b.y0 < y < b.y1 and b.z0 < z < b.z1
            w.set(x, y, z, B.LAVA if inner else B.OBSIDIAN)

    def write(self, doc, teams):
        rid = doc.region(f"{self.id}-region", self.box.cuboid())
        doc.child("cores").append(E("core", id=self.id, name=self.name, team=self.team, leak=self.leak,
                                    mode_changes=True, region=rid))

    def check(self, w):
        b = self.box
        if min(b.x1 - b.x0, b.y1 - b.y0, b.z1 - b.z0) < 2:
            return [f"core {self.id}: too small to hold lava inside a shell"]
        lava = [p for p in b.blocks() if w.id(*p) in (B.LAVA, B.LAVA_FLOW)]
        return float_problems("core", self.id, b, w) + ([] if lava else [f"core {self.id}: no lava inside"])

    def cells(self):
        return self.box.cells()

    def marker(self):
        x, z = self.box.centre()
        return (int(x), int(z), "C")


@dataclass
class ScoreBox(Objective):
    """A box that scores for `team` when one of them walks in, and sends them home through a portal."""
    team: str
    box: Box
    points: int = 1
    home: tuple = None                   # where a scorer is sent, (x, y, z), or None to stay
    home_yaw: int = None

    def turned(self, sym):
        return replace(self, box=self.box.image(sym), home=turn_point(self.home, sym) if self.home else None,
                       home_yaw=turn_yaw(self.home_yaw, sym))

    def write(self, doc, teams):
        f = f"only-{teams.short(self.team)}"
        doc.child("score").append(E("box", E("region", self.box.cuboid()), points=self.points, filter=f))
        if self.home:
            x, y, z = self.home
            doc.child("portals").append(E("portal", E("region", self.box.cuboid()), x=f"@{x + 0.5}", y=f"@{y}",
                                          z=f"@{z + 0.5}", yaw=None if self.home_yaw is None else f"@{self.home_yaw}",
                                          filter=f))

    def check(self, w):
        solid = [p for p in self.box.blocks() if w.id(*p) not in PASSABLE]
        return [f"score box for {self.team}: {len(solid)} solid blocks inside"] if solid else []

    def cells(self):
        return self.box.cells()

    def marker(self):
        x, z = self.box.centre()
        return (int(x), int(z), "+")


@dataclass
class Portal(Objective):
    """A portal from a box to a block a player lands standing in, facing yaw, for those `filter` lets through."""
    id: str
    box: Box
    to: tuple
    yaw: int = None
    filter: str = None
    team: str = None

    def turned(self, sym):
        return replace(self, box=self.box.image(sym), to=turn_point(self.to, sym), yaw=turn_yaw(self.yaw, sym))

    def write(self, doc, teams):
        rid = doc.region(self.id, self.box.cuboid())
        x, y, z = self.to
        doc.child("portals").append(E("portal", region=rid, x=f"@{x + 0.5}", y=f"@{y}", z=f"@{z + 0.5}",
                                      yaw=None if self.yaw is None else f"@{self.yaw}", filter=self.filter))

    def check(self, w):
        return [] if _stands(w, self.to) else [f"portal {self.id}: lands at {self.to} with nowhere to stand"]

    def cells(self):
        return self.box.cells()

    def marker(self):
        x, z = self.box.centre()
        return (int(x), int(z), "P")


# ---- the set ----------------------------------------------------------------------------------------------
class Objectives:
    def __init__(self, teams=None, symmetry=None):
        self.teams = teams or Teams()
        self.symmetry = symmetry
        self.items = []

    def add(self, obj, mirror=True, **image):
        """Add an objective and, if it is a team's and the board is symmetric, its images for the other teams: one
        for a half turn or a mirror, three for a quarter turn, each the last carried on. `image` overrides fields
        of every image (a wool's colour, a name); a list or tuple value gives each image its own, in order."""
        self.items.append(obj)
        if mirror and self.symmetry is not None and getattr(obj, "team", None) is not None:
            prev = obj
            for k in range(getattr(self.symmetry, "order", 2) - 1):
                img = prev.image(self.symmetry, self.teams)
                if image:
                    img = replace(img, **{f: (v[k] if isinstance(v, (list, tuple)) and not isinstance(v, str)
                                              and f not in ("slot", "found", "at", "spawn_at") else v)
                                          for f, v in image.items()})
                if img is not prev:
                    self.items.append(img)
                prev = img
        return obj

    def of(self, kind):
        return [o for o in self.items if isinstance(o, kind)]

    def stamp(self, w):
        for o in self.items:
            o.stamp(w)

    def write(self, doc, limit=None):
        """Teams and their filters, then every objective's regions and XML; a score limit if given."""
        if self.teams.teams:
            self.teams.write(doc)
        for o in self.items:
            o.write(doc, self.teams)
        wool_rooms(doc, self.teams, self.of(Wool))
        if limit is not None:
            doc.child("score").append(E("limit", text=limit))
        return doc

    def check(self, w):
        """Every objective read back from the built world: a list of what is wrong, empty when nothing is."""
        out = []
        for o in self.items:
            out += o.check(w)
        claims = {}
        for o in self.items:
            for c in o.cells():
                claims.setdefault(c, []).append(o)
        clash = {(type(a).__name__, type(b).__name__) for os_ in claims.values() for a in os_ for b in os_
                 if a is not b and not isinstance(a, (Spawn, ScoreBox)) and not isinstance(b, (Spawn, ScoreBox))}
        out += [f"{a} and {b} claim the same ground" for a, b in sorted(clash) if a <= b]
        return out

    def markers(self):
        """(x, z, letter, team) for every objective the sketch draws."""
        out = []
        for o in self.items:
            m = o.marker()
            for one in (m if isinstance(m, list) else [m] if m else []):
                out.append((*one, getattr(o, "team", None)))
        return out

