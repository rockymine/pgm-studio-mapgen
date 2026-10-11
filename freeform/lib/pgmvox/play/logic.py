"""What a match does over its course, stated as parts: conditions (filters), what happens when one comes true
(triggers and their actions), variables, kits handed out on a condition, and the objectives that move with the
match (payloads, a control point taken by one team alone). Each part writes itself; `Map(parts=[...])` takes them.

    released = After("25s", MatchStarted())
    parts = [Named("seekers-released", released),
             Trigger("seekers-released", [Fill(["seeker-cage"], "air")]),
             Give("seeker", All(Ref("seekers-released"), Team("seekers")))]

**A filter is a value, and a named filter is a part.** A filter object writes its element where it is used;
`Named(id, filter)` writes it once under <filters> for others to name by id, and `Ref(id)` names one. A string
where a filter is taken is its id, or one of PGM's own expressions (`not(x)`, `order=0`).
"""
from dataclasses import dataclass, field

from pgmvox.play.mapxml import E, union
from pgmvox.play.objectives import Objective, turn_point


# ---- filters ---------------------------------------------------------------------------------------------------------
class Filter:
    def element(self):
        raise NotImplementedError


def _el(f):
    """A filter as an element: a Filter object, or a string naming one."""
    return f.element() if isinstance(f, Filter) else E("filter", id=f)


def _attr(f):
    """A filter as an attribute value: a string as it is; a filter object must be Named to be named."""
    if f is None or isinstance(f, str):
        return f
    raise ValueError("an attribute takes a filter's id: name the filter with Named")


@dataclass
class Ref(Filter):
    id: str

    def element(self):
        return E("filter", id=self.id)


@dataclass
class Team(Filter):
    team: str

    def element(self):
        return E("team", text=self.team)


@dataclass
class Not(Filter):
    of: object

    def element(self):
        return E("not", _el(self.of))


class All(Filter):
    def __init__(self, *of):
        self.of = of

    def element(self):
        return E("all", *[_el(f) for f in self.of])


class Any(Filter):
    def __init__(self, *of):
        self.of = of

    def element(self):
        return E("any", *[_el(f) for f in self.of])


@dataclass
class Completed(Filter):
    """An objective done: a destroyable broken, a point captured, a payload's leg pushed."""
    objective: str

    def element(self):
        return E("completed", text=self.objective)


@dataclass
class Holding(Filter):
    """Whoever holds an objective (a control point's owner)."""
    objective: str

    def element(self):
        return E("objective", text=self.objective)


class MatchStarted(Filter):
    def element(self):
        return E("match-started")


class MatchRunning(Filter):
    def element(self):
        return E("match-running")


class Participating(Filter):
    def element(self):
        return E("participating")


class Void(Filter):
    def element(self):
        return E("void")


@dataclass
class After(Filter):
    """`duration` after `of` came true; a `message` counts the time down ({0})."""
    duration: str
    of: object
    message: str = None

    def element(self):
        if isinstance(self.of, str):
            return E("after", duration=self.duration, filter=self.of, message=self.message)
        return E("after", _el(self.of), duration=self.duration, message=self.message)


@dataclass
class Time(Filter):
    """True from this long into the match."""
    after: str

    def element(self):
        return E("time", text=self.after)


@dataclass
class Material(Filter):
    name: str

    def element(self):
        return E("material", text=self.name)


@dataclass
class Cause(Filter):
    name: str

    def element(self):
        return E("cause", text=self.name)


@dataclass
class Entity(Filter):
    name: str

    def element(self):
        return E("entity", text=self.name)


@dataclass
class Pulse(Filter):
    """On for `duration` every `period` while `of` holds."""
    duration: str
    period: str
    of: str

    def element(self):
        return E("pulse", duration=self.duration, period=self.period, filter=self.of)


@dataclass
class Deny(Filter):
    of: object

    def element(self):
        return E("deny", _el(self.of))


@dataclass
class Named:
    """A filter written once under <filters>, for others to name by `id`."""
    id: str
    filter: Filter

    def write(self, doc):
        doc.filter(self.id, self.filter.element())


# ---- actions ---------------------------------------------------------------------------------------------------------
@dataclass
class Fill:
    """Fill a region with a material: `region` a region's id, or a list of Boxes."""
    region: object
    material: str = "air"

    def element(self, doc):
        return E("fill", region=_region(doc, self.region), material=self.material)


@dataclass
class Message:
    """A line sent to everyone in the action's scope (PGM reads it from the `text` attribute)."""
    text: str
    id: str = None

    def element(self, doc):
        el = E("message", id=self.id)
        el.set("text", self.text)
        return el


@dataclass
class SetVar:
    var: str
    value: object
    scope: str = None

    def element(self, doc):
        return E("set", var=self.var, value=self.value)


@dataclass
class KillEntities:
    filter: str

    def element(self, doc):
        return E("kill-entities", filter=self.filter)


@dataclass
class Act:
    """Actions done together: only where `filter` holds when given, named `id` when given."""
    actions: list
    filter: str = None
    id: str = None
    scope: str = None

    def element(self, doc):
        return E("action", *[a.element(doc) for a in self.actions], filter=self.filter, id=self.id, scope=self.scope)


@dataclass
class Area:
    """A region named for actions and rules to refer to: one Box, or the union of several."""
    id: str
    boxes: list

    def write(self, doc):
        doc.region(self.id, self.boxes[0].cuboid() if len(self.boxes) == 1 else
                   union(*[b.cuboid() for b in self.boxes]))


def _region(doc, r):
    if isinstance(r, str):
        return r
    shape = r[0].cuboid() if len(r) == 1 else union(*[b.cuboid() for b in r])
    n = 1
    while f"fill-{n}" in doc.ids():
        n += 1
    return doc.region(f"fill-{n}", shape)


@dataclass
class Trigger:
    """When `when` comes true, do `actions` (a list, or the id of a named action)."""
    when: object
    actions: object
    scope: str = "match"

    def write(self, doc):
        when = self.when if isinstance(self.when, str) else None
        inner = [] if when is not None else [E("filter", _el(self.when))]
        if isinstance(self.actions, str):
            doc.child("actions").append(E("trigger", *inner, filter=when, action=self.actions, scope=self.scope))
            return
        acts = self.actions if isinstance(self.actions, Act) else Act(self.actions)
        doc.child("actions").append(E("trigger", *inner, acts.element(doc), filter=when, scope=self.scope))


@dataclass
class Action:
    """A named action under <actions>, for a trigger to name."""
    id: str
    actions: list
    scope: str = "match"

    def write(self, doc):
        doc.child("actions").append(E("action", *[a.element(doc) for a in self.actions], id=self.id, scope=self.scope))


@dataclass
class Variable:
    id: str
    scope: str = "match"
    default: object = 0

    def write(self, doc):
        doc.child("variables").append(E("variable", id=self.id, scope=self.scope, default=self.default))


@dataclass
class Give:
    """A kit given whenever `filter` comes true: a kit's id, or a Kit written in place."""
    kit: object
    filter: object

    def write(self, doc):
        kit = self.kit if isinstance(self.kit, str) else None
        inner = [] if kit else [self.kit.inline()]
        filt = self.filter if isinstance(self.filter, str) else None
        if filt is None:
            inner.append(E("filter", _el(self.filter)))
        doc.child("kits").append(E("give", *inner, kit=kit, filter=filt))


# ---- objectives that move with the match ------------------------------------------------------------------------
@dataclass
class ControlPoint(Objective):
    """A control point (<control-points>): captured standing in `box`, shown on `progress` (default the box), taken
    by those `capture_filter` lets in, owned at the start by `initial_owner`, kept once taken when `permanent`."""
    id: str
    name: str
    box: object
    progress: object = None
    capture_time: str = None
    capture_filter: str = None
    initial_owner: str = None
    permanent: bool = None
    show_progress: bool = None
    team: str = None

    def turned(self, sym):
        from dataclasses import replace
        return replace(self, box=self.box.image(sym), progress=self.progress.image(sym) if self.progress else None)

    def write(self, doc, teams):
        cap = doc.region(f"{self.id}-capture", self.box.cuboid())
        shown = doc.region(f"{self.id}-ring", self.progress.cuboid()) if self.progress else cap
        doc.child("control-points").append(E("control-point", id=self.id, name=self.name, capture=cap,
                                             progress=shown, captured=shown, initial_owner=self.initial_owner,
                                             capture_filter=self.capture_filter, permanent=self.permanent,
                                             capture_time=self.capture_time, show_progress=self.show_progress))

    def cells(self):
        return self.box.cells()


@dataclass
class Payload(Objective):
    """A leg of a payload: the cart pushed to `location`, open to those `player_filter` lets push, shown while
    `display_filter` holds."""
    id: str
    name: str
    location: tuple
    player_filter: str = None
    display_filter: str = None
    team: str = None

    def turned(self, sym):
        from dataclasses import replace
        return replace(self, location=turn_point(self.location, sym))

    def write(self, doc, teams):
        x, y, z = self.location
        doc.child("payloads").append(E("payload", id=self.id, name=self.name, location=f"{x},{y},{z}",
                                       player_filter=self.player_filter, display_filter=self.display_filter))


@dataclass
class Payloads:
    """How every payload leg is pushed (an experiment PGM must have switched on: experiments.payload)."""
    capture_filter: str
    capture_time: str = "60s"
    radius: float = 3.5
    permanent: bool = True
    decay_rate: float = 0.1
    recovery_rate: float = 0.5
    contested_rate: float = 0
    time_multiplier: float = 0.1

    def write(self, doc):
        el = doc.child("payloads")
        for k, v in (("permanent", self.permanent), ("radius", self.radius), ("capture-filter", self.capture_filter),
                     ("capture-time", self.capture_time), ("decay-rate", self.decay_rate),
                     ("recovery-rate", self.recovery_rate), ("contested-rate", self.contested_rate),
                     ("time-multiplier", self.time_multiplier)):
            el.set(k, "true" if v is True else f"{v:g}" if isinstance(v, float) else str(v))


# ---- world rules --------------------------------------------------------------------------------------------------
@dataclass
class Gamerules:
    rules: dict

    def write(self, doc):
        doc.add(E("gamerules", [E(k, text=str(v).lower() if isinstance(v, bool) else v)
                                for k, v in self.rules.items()]))


@dataclass
class Damage:
    """Damage allowed by `allow` and refused by `deny`, each a list of filters, and `only` filters every hurt must
    pass."""
    allow: list = field(default_factory=list)
    deny: list = field(default_factory=list)
    only: list = field(default_factory=list)

    def write(self, doc):
        el = doc.child("damage")
        for f in self.allow:
            el.append(E("allow", _el(f)))
        for f in self.deny:
            el.append(E("deny", _el(f)))
        for f in self.only:
            el.append(_el(f))


@dataclass
class BlockDrop:
    """What a block drops and what it turns into: where `filter` holds (a filter) or in `region` (a Box)."""
    filter: object = None
    region: object = None
    drops: list = field(default_factory=list)      # Items
    replacement: str = None
    trample: bool = None

    def write(self, doc):
        rid = None
        if self.region is not None:
            n = 1
            while f"drop-{n}" in doc.ids():
                n += 1
            rid = doc.region(f"drop-{n}", self.region.cuboid())
        doc.child("block-drops").append(E("rule", E("filter", _el(self.filter)) if self.filter else None,
                                          E("drops", *[i.element() for i in self.drops]) if self.drops else None,
                                          E("replacement", text=self.replacement) if self.replacement else None,
                                          region=rid, trample=self.trample))


@dataclass
class Falling:
    """Blocks `filter` lets fall once a player has touched them, after `delay` ticks; nothing holds them up."""
    filter: object
    delay: int = 10

    def write(self, doc):
        doc.child("falling-blocks").append(E("rule", E("filter", _el(self.filter)), E("sticky", E("never")),
                                             delay=self.delay))


@dataclass
class Compass:
    """The compass points at the nearest player `filter` lets through, named `name`."""
    filter: str
    name: str = None
    show_player: bool = None

    def write(self, doc):
        doc.add(E("compass", E("player", filter=self.filter, show_player=self.show_player, name=self.name),
                  show_distance=True))
