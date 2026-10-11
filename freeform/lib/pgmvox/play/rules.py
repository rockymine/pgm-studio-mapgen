"""A map stated as parts and written whole: no board writes an element of its map.xml by hand.

    M = Map("Claywork", "1.0.0", "Capture the enemy's two wools.", "ctw",
            authors=["Claude (freeform generator, pgmvox)"], objectives=O,
            kit=Kit(Item("iron sword", 0, unbreakable=True), Item("wood", 4, 64, 1), ...,
                    Item("leather helmet", unbreakable=True, team_color=True, wear="helmet")),
            build=Build(max_height=44), match=Match(time=15 * 60))
    print(M.xml())

**What the studio derives, this derives the same way.** The kit's loadout is kept on death and its armour dropped,
its tools repaired, its stacked blocks break into nothing once placed and come back as a kill's reward, sixteen of a
neutral block and eight of a team's; every material a destroyable or a core ever is cannot be picked up; hunger is
off and the golden-apple kill reward is included (`MapStandards` in the studio).

**The build rule is the studio's.** Building is refused over the void outside the build areas, or everywhere when no
area is given; decoration over the void may still be broken; `never` refuses building anywhere.
"""
from dataclasses import dataclass, field

from pgmvox.play.mapxml import Doc, E, below as below_el, duration, negative, union
from pgmvox.play.objectives import Core, Destroyable, Flag, Objective, turn_point

TOOL_WORDS = {"sword", "bow", "pickaxe", "axe", "spade", "shovel", "shears", "hoe", "rod"}
CONSUMED = {"arrow", "cooked beef", "cooked chicken", "cooked porkchop", "cooked fish", "bread", "apple",
            "golden apple", "golden carrot", "baked potato", "carrot item", "snow ball", "egg", "ender pearl"}
KILL_REWARD_INCLUDE = "gapple-kill-reward"
VOID_MESSAGE = "You may not edit the void!"
OVER_VOID = ("log", "log 2", "leaves", "leaves 2", "long grass", "yellow flower", "red rose", "double plant",
             "water lily", "vine")
MAX_BUILD_HEIGHT = 100


# ---- the kit ----------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Item:
    """A kit's item: Item("bow", 1, enchant=[("infinity", 1)], unbreakable=True); `wear` "helmet", "chestplate",
    "leggings" or "boots" makes it armour."""
    material: str
    slot: int = None
    amount: int = None
    damage: int = None
    enchant: tuple = ()
    unbreakable: bool = None
    team_color: bool = None
    wear: str = None
    name: str = None
    locked: bool = None
    color: str = None                    # leather's dye, as hex

    def element(self):
        return E(self.wear or "item", *[E("enchantment", text=n, level=lv) for n, lv in self.enchant], slot=self.slot,
                 material=self.material, amount=self.amount, damage=self.damage, unbreakable=self.unbreakable,
                 team_color=self.team_color, name=self.name, locked=self.locked, color=self.color)


@dataclass(frozen=True)
class Effect:
    """A potion effect a kit gives: Effect("resistance", "3s", 5); no duration lasts while the kit holds."""
    name: str
    duration: str = None
    amplifier: int = None

    def element(self):
        return E("effect", text=self.name, duration=self.duration, amplifier=self.amplifier)


@dataclass(frozen=True)
class EnchantItem:
    """An action: the player's `material` item enchanted to `level`, whatever it carried before."""
    material: str
    enchantment: str
    level: int

    def element(self):
        return E("action", E("enchant-item", E("find", material=self.material), ignore_metadata=True,
                             enchantment=self.enchantment, level=self.level))


@dataclass
class ForEveryone:
    """An action: `kit` given to every player in the match that `filter` lets through."""
    filter: str
    kit: object

    def element(self):
        return E("action", E("switch-scope", E("switch-scope", self.kit.inline(), inner="player", filter=self.filter),
                             inner="match"))


class Kit:
    """A kit: its items and armour, and what else it gives: `clear` the inventory first, `effects`, a `game_mode`,
    `max_health`, `actions`. The spawn kit also states what follows from it: `reward`, the kill reward when it is not
    the kit's own blocks, and `remove`, materials dropped on death besides the armour."""

    def __init__(self, *items, id="spawn-kit", clear=None, effects=(), game_mode=None, max_health=None, force=None,
                 actions=(), reward=None, remove=()):
        self.items = list(items)
        self.id = id
        self.clear = clear
        self.effects = list(effects)
        self.game_mode = game_mode
        self.max_health = max_health
        self.force = force
        self.actions = list(actions)
        self.reward = reward
        self.remove = list(remove)

    def loadout(self):
        return [i for i in self.items if not i.wear]

    def stacks(self):
        return [i for i in self.loadout() if (i.amount or 1) > 1]

    def blocks(self):
        """The stacked items a player builds with: every stack but food and arrows."""
        return [i for i in self.stacks() if i.material not in CONSUMED]

    def _children(self):
        return ([E("clear")] if self.clear else []) + [i.element() for i in self.items] + \
            [e.element() for e in self.effects] + \
            ([E("game-mode", text=self.game_mode)] if self.game_mode else []) + \
            ([E("max-health", text=self.max_health)] if self.max_health is not None else []) + \
            [a.element() for a in self.actions]

    def inline(self):
        """The kit written where it is given, with no id."""
        return E("kit", *self._children(), force=self.force)

    def write(self, doc):
        doc.kit(self.id, *self._children(), force=self.force)

    def standards(self, doc, destroyed=()):
        """Item keep, tool repair, item remove, the placed blocks' drops and the kill reward, read off the kit."""
        singles = [i.material for i in self.loadout() if (i.amount or 1) <= 1]
        stacks = list(dict.fromkeys(i.material for i in self.blocks()))
        keep = list(dict.fromkeys(singles + [i.material for i in self.stacks()]))
        tools = list(dict.fromkeys(m for m in singles if m.split()[-1] in TOOL_WORDS))
        remove = list(dict.fromkeys([i.material for i in self.items if i.wear] + self.remove + list(destroyed)))
        if stacks:
            doc.add(E("block-drops", E("rule", E("filter", E("material", text=stacks[0]) if len(stacks) == 1 else
                                                   E("any", [E("material", text=m) for m in stacks])),
                                       E("drops", E("item", material=stacks[0], chance=0.0)))))
        for tag, inner, names in (("itemkeep", "item", keep), ("itemremove", "item", remove),
                                  ("toolrepair", "tool", tools)):
            if names:
                doc.add(E(tag, [E(inner, text=m) for m in names]))
        if self.reward is not None:
            rewards = [i.element() for i in self.reward]
        else:
            once = {(i.material, i.damage, i.team_color): i for i in self.blocks()}.values()
            rewards = [E("item", material=i.material, damage=i.damage, amount=8 if i.team_color else 16,
                         team_color=i.team_color or None) for i in once]
        if rewards:
            doc.add(E("kill-rewards", E("kill-reward", *rewards)))


# ---- building -----------------------------------------------------------------------------------------------------
@dataclass
class Build:
    """Where a player may build: over the void only inside `areas` (rectangles (x0, z0, x1, z1), inclusive blocks)
    less `holes`; with no area, only where a column has a block at y 0 (the land, and the build zones marked with
    block 36); `void` False lets a player build anywhere; `never` refuses it everywhere, and `use` False refuses
    using a block too; `only` lets a player place and break those materials and nothing else, and `physics` False
    holds every block as it is. `max_height` is the build height, held to the studio's 100."""
    areas: list = field(default_factory=list)
    holes: list = field(default_factory=list)
    max_height: int = None
    void: bool = True
    never: bool = False
    use: bool = True
    only: tuple = ()
    physics: bool = True
    message: str = None

    def write(self, doc):
        if self.never:
            doc.apply(block="never", use=None if self.use else "never", message=self.message)
        elif self.only:
            doc.filter("only-these", E("all", E("any", [E("material", text=m) for m in self.only]),
                                       E("not", E("cause", text="world"))))
            doc.apply(block_place="only-these", block_break="only-these",
                      block_physics=None if self.physics else "never", message=self.message)
        elif self.void:
            doc.filter("block-place-void-filter", E("not", E("void")))
            doc.filter("block-break-void-filter", E("any", E("all", E("any", [E("material", text=m) for m in OVER_VOID]),
                                                              E("void")), E("filter", id="block-place-void-filter")))
            region = None
            if self.areas:
                rects = [_rect(r) for r in self.areas]
                area = rects[0] if len(rects) == 1 else union(*rects)
                if self.holes:
                    area = E("complement", area, *[_rect(r) for r in self.holes])
                region = doc.region("not-build-area", negative(area))
            doc.apply(block_place="block-place-void-filter", block_break="block-break-void-filter", region=region,
                      message=self.message or VOID_MESSAGE)
        if self.max_height is not None:
            doc.add(E("maxbuildheight", text=min(self.max_height, MAX_BUILD_HEIGHT)))


def _rect(r):
    x0, z0, x1, z1 = r
    return E("rectangle", min=f"{x0},{z0}", max=f"{x1 + 1},{z1 + 1}")


# ---- the match ----------------------------------------------------------------------------------------------------
@dataclass
class Match:
    """How a match ends and what it spares: a time limit and what wins at it, a score limit with points a kill and a
    death, lives, fall damage, and the broadcasts it makes: ("alert" or "tip", after seconds, text)."""
    time: int = None
    result: str = None
    score: int = None
    kills: int = None
    deaths: int = None
    lives: int = None
    fall_damage: bool = True
    broadcasts: list = field(default_factory=list)
    respawn: object = None               # a Respawn
    time_of_day: int = None              # the world's clock held at these ticks

    def write(self, doc):
        if self.score is not None or self.kills is not None:
            score = doc.child("score")
            for tag, v in (("limit", self.score), ("kills", self.kills), ("deaths", self.deaths)):
                if v is not None:
                    score.append(E(tag, text=v))
        if self.time is not None:
            doc.add(E("time", text=duration(self.time), result=self.result))
        if self.lives is not None:
            doc.add(E("blitz", E("lives", text=self.lives)))
        if not self.fall_damage:
            doc.add(E("disabledamage", E("damage", text="fall")))
        if self.broadcasts:
            doc.add(E("broadcasts", [E(kind, text=text, after=duration(t)) for kind, t, text in self.broadcasts]))
        if self.respawn:
            self.respawn.write(doc)
        if self.time_of_day is not None:
            doc.add(E("world", E("timeset", text=self.time_of_day), E("timelock", text="on")))


@dataclass
class Respawn:
    """How the dead come back: after `delay`, on their own when `auto`, watching the match while they wait when
    `spectate`; `message` a translation key shown while they wait."""
    delay: str = "3s"
    auto: bool = None
    spectate: bool = None
    message: str = None

    def write(self, doc):
        msg = E("message", text='{"translate":"%s"}' % self.message) if self.message else None
        doc.add(E("respawn", msg, delay=self.delay, auto=self.auto, spectate=self.spectate))


@dataclass
class KillHeight:
    """Anyone below y dies: "kit" gives instant damage and keeps them in the world until it lands, "portal" sends
    them into the void. With `boxes` (each a Box), anyone inside any of them is sent to y `to` instead."""
    y: int = None
    how: str = "kit"
    boxes: list = None
    to: int = -64

    def write(self, doc):
        if self.boxes:
            doc.child("portals").append(E("portal", E("region", union(*[b.cuboid() for b in self.boxes])),
                                          y=f"@{self.to}", sound=False))
        elif self.how == "kit":
            doc.kit("fall-kill", E("effect", text="instant damage", duration=1, amplifier=5), force=True)
            doc.region("the-fall", below_el(self.y))
            doc.apply(kit="fall-kill", region="the-fall")
        else:
            doc.child("portals").append(E("portal", E("region", below_el(self.y)), y=f"@{self.to}", sound=False,
                                          observers="never"))


# ---- placed things that are not objectives ---------------------------------------------------------------------------
@dataclass
class Spawner(Objective):
    """Items dropped at a block, (x, y, z) the block they appear in, while a player is within `reach` of it."""
    id: str
    at: tuple
    items: list                          # [(material, amount)]
    delay: str = "30s"
    max_entities: int = 1
    reach: int = 4                       # None: it runs whoever is near
    team: str = None
    box: object = None                   # the box items drop in, when not the default about `at`

    def turned(self, sym):
        from dataclasses import replace
        return replace(self, at=turn_point(self.at, sym), box=self.box.image(sym) if self.box else None)

    def write(self, doc, teams):
        x, y, z = self.at
        rid = doc.region(self.id, self.box.cuboid() if self.box else
                         E("cuboid", min=f"{x - 0.5},{y},{z - 0.5}", max=f"{x + 1.5},{y + 2},{z + 1.5}"))
        r = self.reach
        near = None if r is None else doc.region(f"{self.id}-near", E("cuboid", min=f"{x - r},{y},{z - r}",
                                                                      max=f"{x + r + 1},{y + r},{z + r + 1}"))
        doc.child("spawners").append(E("spawner", *[E("item", material=m, amount=a if a != 1 else None)
                                                    for m, a in self.items],
                                       spawn_region=rid, player_region=near, delay=self.delay,
                                       max_entities=self.max_entities))

    def cells(self):
        return {(self.at[0], self.at[2])}

    def marker(self):
        return (self.at[0], self.at[2], "s")


@dataclass
class JumpPad(Objective):
    """A box that throws whoever steps in along `velocity` (x, y, z), turned with the board; `block` is laid under
    the box's floor when stamped. A `safe` pad spares its rider the fall: no fall damage from the launch until they
    have left every pad for a second and stood on the ground."""
    id: str
    box: object
    velocity: tuple
    block: tuple = None
    team: str = None
    safe: bool = False

    def turned(self, sym):
        from dataclasses import replace
        from pgmvox.core.orient import OPS
        vx, vy, vz = self.velocity
        tx, tz = OPS[sym.op](vx, vz)
        return replace(self, box=self.box.image(sym), velocity=(tx, vy, tz))

    def stamp(self, w):
        if self.block:
            for x, z in self.box.cells():
                w.set(x, self.box.y0 - 1, z, *self.block)

    def write(self, doc, teams):
        kit = None
        if self.safe:                                  # a safe pad's box is named inside the union of every pad
            kit = "used-jump-pad"
            if "jump-pads" not in doc.ids():
                _safe_landing(doc)
            if self.id in doc.ids():
                raise ValueError(f"region id {self.id!r} is taken")
            doc.root.find(".//regions/union[@id='jump-pads']").append(self.box.cuboid(id=self.id))
            rid = self.id
        else:
            rid = doc.region(self.id, self.box.cuboid())
        doc.apply(region=rid, kit=kit, velocity=",".join(f"{v:g}" for v in self.velocity))

    def cells(self):
        return self.box.cells()

    def marker(self):
        x, z = self.box.centre()
        return (int(x), int(z), "J")


def _safe_landing(doc):
    """The machinery every safe pad shares: a player variable set by the pad's kit, a give that clears it once the
    rider is off the pads and grounded, and fall damage denied while it is set."""
    doc.region("jump-pads", union())
    setv = lambda v: E("kit", E("action", E("set", var="fall_variable", value=v), scope="player"))   # noqa: E731
    doc.kit("used-jump-pad", E("action", E("set", var="fall_variable", value=1), scope="player"))
    doc.child("kits").append(E("give", E("filter", E("all", E("after", E("not", E("region", id="jump-pads")),
                                                               duration="1s"),
                                                     E("after", E("grounded"), duration="0.2s"))), setv(0)))
    doc.add(E("variables", E("variable", id="fall_variable", scope="player", default=0)))
    doc.add(E("damage", E("deny", E("all", E("cause", text="fall"), E("variable", text=1, var="fall_variable")))))


@dataclass
class Zone(Objective):
    """A place with rules of its own: nobody may `place` or `break_` blocks in it when those are False, and nobody
    is hurt there when `damage` is False. `boxes` are one or more Boxes."""
    id: str
    boxes: list
    place: bool = True
    break_: bool = True
    damage: bool = True
    message: str = None
    team: str = None

    def turned(self, sym):
        from dataclasses import replace
        return replace(self, boxes=[b.image(sym) for b in self.boxes])

    def write(self, doc, teams):
        shape = self.boxes[0].cuboid() if len(self.boxes) == 1 else union(*[b.cuboid() for b in self.boxes])
        rid = doc.region(self.id, shape)
        if not (self.place and self.break_):
            doc.apply(region=rid, block_place=None if self.place else "never",
                      block_break=None if self.break_ else "never", message=self.message)
        if not self.damage:
            doc.child("damage", "deny").append(E("region", id=rid))

    def cells(self):
        return set().union(*[b.cells() for b in self.boxes])


# ---- the whole map --------------------------------------------------------------------------------------------------
@dataclass
class Map:
    """Every part of a map.xml: its name and what it is played for, its authors, the objectives and every placed
    thing, the kit and what follows from it, the build rule, the kill height and the match."""
    name: str
    version: str
    objective: str
    gamemode: object = None
    authors: list = field(default_factory=list)
    contributors: list = field(default_factory=list)      # [(name, contribution)]
    objectives: object = None
    kit: Kit = None
    kits: list = field(default_factory=list)              # the other kits: a flag carrier's, a reset
    build: Build = None
    kill: object = None                                   # a KillHeight, or a list of them
    match: Match = None
    includes: list = field(default_factory=lambda: [KILL_REWARD_INCLUDE])
    rules: list = field(default_factory=list)             # lines shown to a player
    players: tuple = None                                 # (least, most) for a match without teams

    def doc(self):
        d = Doc(self.name, self.version, self.objective, self.gamemode)
        if self.rules:
            d.add(E("rules", [E("rule", text=r) for r in self.rules]))
        for inc in self.includes:
            d.add(E("include", id=inc))
        if self.players:
            d.add(E("players", min=self.players[0], max=self.players[1], colors=True))
        if self.authors:
            d.add(E("authors", [E("author", text=a) for a in self.authors]))
        if self.contributors:
            d.add(E("contributors", [E("contributor", text=n, contribution=c) for n, c in self.contributors]))
        for k in ([self.kit] if self.kit else []) + self.kits:
            k.write(d)
        if self.objectives:
            self.objectives.write(d)
        if self.build:
            self.build.write(d)
        for k in (self.kill if isinstance(self.kill, (list, tuple)) else [self.kill] if self.kill else []):
            k.write(d)
        if self.match:
            self.match.write(d)
        if self.kit:
            self.kit.standards(d, self._destroyed())
        d.add(E("hunger", E("depletion", text="off")))
        return d

    def _destroyed(self):
        out = []
        if self.objectives:
            for o in self.objectives.of(Destroyable):
                out += [m.split(":")[0].strip() for m in str(o.materials).replace(";", ",").split(",") if m.strip()]
            out += ["obsidian" for _ in self.objectives.of(Core)]
            out += ["banner" for _ in self.objectives.of(Flag)]
        return list(dict.fromkeys(out))

    def xml(self):
        return self.doc().tostring()
