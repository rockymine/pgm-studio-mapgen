"""A map stated as parts and written whole: no board writes an element of its map.xml by hand.

    M = Map("Claywork", "1.0.0", "Capture the enemy's two wools.", "ctw",
            authors=["Claude (freeform generator, pgmvox)"], objectives=O,
            kit=Kit(Item("iron sword", 0, unbreakable=True), Item("wood", 4, 64, 1), ...,
                    Item("leather helmet", unbreakable=True, team_color=True, wear="helmet")),
            build=Build(max_height=44), match=Match(time=15 * 60))
    print(M.xml())

**What the studio derives, this derives the same way.** The kit's loadout is kept on death and its armour dropped,
its tools repaired, its stacked blocks break into nothing once placed and come back as a kill's reward, sixteen of a
neutral block and eight of a team's; every material a destroyable or a core ever is cannot be picked up, nor what the
world's own blocks drop (saplings, seeds, flint); hunger is off and the golden-apple kill reward is included
(`MapStandards` in the studio).

**The build rule is the studio's.** Building is refused over the void outside the build areas, or everywhere when no
area is given; decoration over the void may still be broken; `never` refuses building anywhere.
"""
import os
import sys
from dataclasses import dataclass, field

import numpy as np

from pgmvox.core.blocks import LIQUID
from pgmvox.play.mapxml import Doc, E, below as below_el, duration, negative, union
from pgmvox.play.objectives import Core, Destroyable, Flag, Objective, Spawn, turn_point

TOOL_WORDS = {"sword", "bow", "pickaxe", "axe", "spade", "shovel", "shears", "hoe", "rod"}
CONSUMED = {"arrow", "cooked beef", "cooked chicken", "cooked porkchop", "cooked fish", "bread", "apple",
            "golden apple", "golden carrot", "baked potato", "carrot item", "snow ball", "egg", "ender pearl"}
KILL_REWARD_INCLUDE = "gapple-kill-reward"
VOID_MESSAGE = "You may not edit the void!"
TERRAIN_DROPS = {30: ["string"], 31: ["seeds", "long grass"], 175: ["double plant", "seeds"], 18: ["sapling", "apple"],
                 161: ["sapling"], 6: ["sapling"], 38: ["red rose"], 37: ["yellow flower"], 13: ["flint", "gravel"],
                 39: ["brown mushroom"], 40: ["red mushroom"], 73: ["redstone"], 74: ["redstone"], 83: ["sugar cane"],
                 81: ["cactus"], 103: ["melon", "melon seeds"], 86: ["pumpkin"], 106: ["vine"]}
OVER_VOID = ("log", "log 2", "leaves", "leaves 2", "long grass", "yellow flower", "red rose", "double plant",
             "water lily", "vine")


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
    effects: tuple = ()                  # a potion's Effects
    grenade: float = None                # a thrown item that explodes with this power

    def element(self):
        return E(self.wear or "item", *[E("enchantment", text=n, level=lv) for n, lv in self.enchant],
                 *[e.element() for e in self.effects], slot=self.slot, material=self.material, amount=self.amount,
                 damage=self.damage, unbreakable=self.unbreakable, team_color=self.team_color, name=self.name,
                 locked=self.locked, color=self.color, grenade=None if self.grenade is None else True,
                 grenade_power=self.grenade)


@dataclass
class KillReward:
    """What a kill pays: `items`, only while the killer's streak is at `streak` kills when given."""
    items: list
    streak: int = None

    def element(self):
        return E("kill-reward", E("filter", E("kill-streak", count=self.streak)) if self.streak else None,
                 *[i.element() for i in self.items])


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
    """A kit: its items and armour, and what else it gives: `clear` the inventory first (True, or "effects" to clear
    the potion effects too), `effects`, a `game_mode`, `max_health`, `health`, `food` (saturation and food level
    filled to it), `knockback_reduction`, `actions`; `parents` are kits given with it. `deduct_items` False gives an
    item the player already carries again. The kits a map's players spawn with also state what follows from them:
    `reward`, the kill reward when it is not the kits' own blocks (Items, paid every kill, and KillRewards for a
    streak), and `remove`, materials dropped on death besides the armour."""

    def __init__(self, *items, id="spawn-kit", clear=None, effects=(), game_mode=None, max_health=None, health=None,
                 food=None, knockback_reduction=None, force=None, deduct_items=None, parents=(), actions=(),
                 reward=None, remove=()):
        self.items = list(items)
        self.id = id
        self.clear = clear
        self.effects = list(effects)
        self.game_mode = game_mode
        self.max_health = max_health
        self.health = health
        self.food = food
        self.knockback_reduction = knockback_reduction
        self.force = force
        self.deduct_items = deduct_items
        self.parents = list(parents)
        self.actions = list(actions)
        self.reward = reward
        self.remove = list(remove)

    def lineage(self):
        """This kit and every kit it is given with, parents first."""
        out = []
        for p in self.parents:
            out += [k for k in p.lineage() if k not in out]
        return out + [self]

    def loadout(self):
        return [i for i in self.items if not i.wear]

    def _children(self):
        clear = None
        if self.clear:
            clear = E("clear", effects=True) if self.clear == "effects" else E("clear")
        stats = [("max-health", self.max_health), ("health", self.health), ("saturation", self.food),
                 ("foodlevel", self.food), ("knockback-reduction", self.knockback_reduction)]
        return [clear] + [i.element() for i in self.items] + [e.element() for e in self.effects] + \
            ([E("game-mode", text=self.game_mode)] if self.game_mode else []) + \
            [E(tag, text=v) for tag, v in stats if v is not None] + [a.element() for a in self.actions]

    def _attrs(self):
        return dict(force=self.force, deduct_items=self.deduct_items,
                    parents=",".join(p.id for p in self.parents) or None)

    def inline(self):
        """The kit written where it is given, with no id."""
        return E("kit", *self._children(), **self._attrs())

    def write(self, doc):
        doc.kit(self.id, *self._children(), **self._attrs())


def standards(doc, kits, destroyed=(), terrain=()):
    """Item keep, tool repair, item remove, the placed blocks' drops and the kill reward, read off the kits players
    spawn with: everything they carry is kept and its tools repaired, armour and `remove` dropped, stacked blocks
    break into nothing and come back as a kill's reward. What the `terrain`'s block ids drop is removed too, unless a
    kit carries it."""
    items = [i for k in kits for i in k.items]
    loadout = [i for i in items if not i.wear]
    stacked = [i for i in loadout if (i.amount or 1) > 1]
    blocks = [i for i in stacked if i.material not in CONSUMED]
    singles = [i.material for i in loadout if (i.amount or 1) <= 1]
    stacks = list(dict.fromkeys(i.material for i in blocks))
    keep = list(dict.fromkeys(singles + [i.material for i in stacked]))
    tools = list(dict.fromkeys(m for m in singles if m.split()[-1] in TOOL_WORDS))
    drops = [d for i in sorted(terrain) for d in TERRAIN_DROPS.get(i, ()) if d not in keep]
    remove = list(dict.fromkeys([i.material for i in items if i.wear] + [m for k in kits for m in k.remove] +
                                list(destroyed) + drops))
    if stacks:
        doc.add(E("block-drops", E("rule", E("filter", E("material", text=stacks[0]) if len(stacks) == 1 else
                                               E("any", [E("material", text=m) for m in stacks])),
                                   E("drops", E("item", material=stacks[0], chance=0.0)))))
    for tag, inner, names in (("itemkeep", "item", keep), ("itemremove", "item", remove),
                              ("toolrepair", "tool", tools)):
        if names:
            doc.add(E(tag, [E(inner, text=m) for m in names]))
    stated = [k.reward for k in kits if k.reward is not None]
    if stated:
        rewards = [r if isinstance(r, KillReward) else KillReward([r]) for r in stated[0]]
        plain = [r for r in rewards if r.streak is None]
        rewards = ([KillReward([i for r in plain for i in r.items])] if plain else []) + \
            [r for r in rewards if r.streak is not None]
    else:
        once = {(i.material, i.damage, i.team_color): i for i in blocks}.values()
        rewards = [KillReward([Item(i.material, amount=8 if i.team_color else 16, damage=i.damage,
                                    team_color=i.team_color or None) for i in once])] if once else []
    if rewards:
        doc.add(E("kill-rewards", *[r.element() for r in rewards]))


# ---- building -----------------------------------------------------------------------------------------------------
@dataclass
class Build:
    """Where a player may build: over the void only inside `areas` (rectangles (x0, z0, x1, z1), inclusive blocks)
    less `holes`; with no area, only where a column has a block at y 0 (the land, and the build zones marked with
    block 36); `void` False lets a player build anywhere; `never` refuses it everywhere, and `use` False refuses
    using a block too; `only` lets a player place and break those materials and nothing else, and `physics` False
    holds every block as it is; `breakable` lets those materials be broken and nothing be placed; `rule` is a filter
    every block placed or broken must pass. `max_height` is the build height. `break_only` keeps the void rule and
    lets a player break those materials and nothing else, so the ground the map was built with stays: no pit, no
    tunnel, no middle dug to bedrock. The world carries the marks the void rule reads: `mark_ground` lays them."""
    areas: list = field(default_factory=list)
    holes: list = field(default_factory=list)
    max_height: int = None
    void: bool = True
    never: bool = False
    use: bool = True
    only: tuple = ()
    physics: bool = True
    breakable: tuple = ()
    rule: object = None
    message: str = None
    break_only: tuple = ()

    def write(self, doc):
        if self.break_only:                              # first, so it decides every break before the void rule
            doc.filter("break-only", E("any", [E("material", text=m) for m in self.break_only]))
            doc.apply(block_break="break-only", message="You may only break what was built!")
        if self.never:
            doc.apply(block="never", use=None if self.use else "never", message=self.message)
        elif self.rule is not None:
            doc.apply(block=_named(doc, "block-rule", self.rule), message=self.message)
        elif self.breakable:
            doc.filter("breakable", E("any", [E("material", text=m) for m in self.breakable]))
            doc.apply(block_break="breakable", block_place="never", message=self.message)
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
            doc.add(E("maxbuildheight", text=self.max_height))


MARK = 36                                # block 36 at y 0: PGM removes it on load and remembers the column as ground


def mark_ground(w):
    """Lay the mark PGM's void filter reads under every column holding a block that is neither air nor liquid, so a
    player may place and break blocks there: block 36 at y 0. A column with only a core or a monument in it is marked
    too, with the air under it, since its blocks must be broken and the hole under it built in. A board floating clear
    of y 0 has no ground PGM can see without it, and its void rule refuses every block. Returns the number of columns
    marked."""
    body = w.ids[:, 1:, :]
    ground = ((body != 0) & ~np.isin(body, list(LIQUID))).any(axis=1)
    w.ids[:, 0, :][ground] = MARK
    w.dat[:, 0, :][ground] = 0
    return int(ground.sum())


def terrain_of(script):
    """The block ids in the world of the board whose script this is, as `maps/INDEX.md` places it: what
    `Map(terrain=...)` reads the world's own drops off. Empty where the board has no world yet, or the library runs
    outside the repository."""
    from pgmvox.run import REPOSITORY_TOOLS
    if not os.path.isfile(os.path.join(REPOSITORY_TOOLS, "anvil.py")):
        return set()
    sys.path.insert(0, REPOSITORY_TOOLS)
    import anvil
    import worlds
    world = worlds.of(os.path.dirname(os.path.dirname(os.path.abspath(script))))
    if world is None or not os.path.isdir(os.path.join(world, "region")):
        return set()
    return anvil.World(os.path.join(world, "region")).ids()


def _named(doc, id_, f):
    """A filter's id: a string as it is, a filter object written under <filters> as `id_`."""
    return f if isinstance(f, str) else doc.filter(id_, f.element())


def _rect(r):
    x0, z0, x1, z1 = r
    return E("rectangle", min=f"{x0},{z0}", max=f"{x1 + 1},{z1 + 1}")


# ---- the match ----------------------------------------------------------------------------------------------------
@dataclass
class Match:
    """How a match ends and what it spares: a time limit (seconds, or PGM's text) and what wins at it, a score limit
    with points a kill and a death, a Blitz, fall damage, and the broadcasts it makes: ("alert" or "tip", after
    seconds or text, text), with the id of a filter saying who hears it as a fourth."""
    time: object = None
    result: str = None
    score: int = None
    kills: int = None
    deaths: int = None
    blitz: object = None                 # a Blitz
    fall_damage: bool = True
    broadcasts: list = field(default_factory=list)
    respawn: object = None               # a Respawn, or a list of them each for those its filter lets through
    time_of_day: int = None              # the world's clock held at these ticks
    rage: bool = False                   # every hit kills

    def write(self, doc):
        if self.rage:
            doc.add(E("rage"))
        if self.score is not None or self.kills is not None:
            score = doc.child("score")
            for tag, v in (("limit", self.score), ("kills", self.kills), ("deaths", self.deaths)):
                if v is not None:
                    score.append(E(tag, text=v))
        if self.time is not None:
            doc.add(E("time", text=duration(self.time), result=self.result))
        if self.blitz:
            self.blitz.write(doc)
        if not self.fall_damage:
            doc.add(E("disabledamage", E("damage", text="fall")))
        if self.broadcasts:
            doc.add(E("broadcasts", [E(b[0], text=b[2], after=duration(b[1]), filter=b[3] if len(b) > 3 else None)
                                     for b in self.broadcasts]))
        if isinstance(self.respawn, (list, tuple)):
            doc.add(E("respawns", [r.element() for r in self.respawn]))
        elif self.respawn:
            doc.add(self.respawn.element())
        if self.time_of_day is not None:
            doc.add(E("world", E("timeset", text=self.time_of_day), E("timelock", text="on")))


@dataclass
class Blitz:
    """Each player has `lives`, those `filter` lets through (everyone when None); `broadcast` tells the match how
    many each has left."""
    lives: int = 1
    filter: str = None
    broadcast: bool = None

    def write(self, doc):
        doc.add(E("blitz", E("lives", text=self.lives),
                  E("broadcastLives", text="true") if self.broadcast else None, filter=self.filter))


@dataclass
class Respawn:
    """How the dead come back: after `delay`, on their own when `auto`, watching the match while they wait when
    `spectate`; `message` a translation key shown while they wait; `filter` the id of a filter saying whom this
    respawn is for, when the match has several."""
    delay: str = "3s"
    auto: bool = None
    spectate: bool = None
    message: str = None
    filter: str = None

    def element(self):
        msg = E("message", text='{"translate":"%s"}' % self.message) if self.message else None
        return E("respawn", msg, delay=self.delay, auto=self.auto, spectate=self.spectate, filter=self.filter)


@dataclass
class KillHeight:
    """Anyone below y is sent to y `to`, into the void, where they die and what they carry is gone with them; with
    `boxes` (each a Box), anyone inside any of them is. A player killed over the blocks under a floating board would
    drop their items onto them, out of everyone's reach."""
    y: int = None
    boxes: list = None
    to: int = -64

    def write(self, doc):
        if self.boxes:
            doc.child("portals").append(E("portal", E("region", union(*[b.cuboid() for b in self.boxes])),
                                          y=f"@{self.to}", sound=False))
        else:
            doc.child("portals").append(E("portal", E("region", below_el(self.y)), y=f"@{self.to}", sound=False,
                                          observers="never"))


@dataclass
class Crafting:
    """Recipes nobody may craft: `disable` names the results. A board that disables the crafting table, and holds
    none, leaves nothing to make a fence, a fence gate, iron bars or stairs from a kit's planks: the anti-climb
    staircases and the fence-gate crowns of a late match are not built."""
    disable: tuple = ("crafting table",)

    def write(self, doc):
        doc.add(E("crafting", [E("disable", text=m) for m in self.disable]))


@dataclass
class Renewables:
    """Ground that grows back: each box in `boxes` returns to the world it was built as, `rate` blocks a second
    over its whole volume, never within `avoid` blocks of a player; `grow` lets it come back only next to what
    already stands. A pit dug in front of a wall and a middle dug to bedrock fill in again."""
    boxes: list
    rate: float = 1.0
    avoid: int = 3
    grow: bool = True
    id: str = "renews"

    def write(self, doc):
        rid = doc.region(self.id, union(*[b.cuboid() for b in self.boxes]) if len(self.boxes) > 1
                         else self.boxes[0].cuboid())
        attrs = {"region": rid, "avoid-players": self.avoid}
        if self.rate != 1.0:
            attrs["rate"] = self.rate
        if self.grow:
            attrs["grow"] = "true"
        doc.add(E("renewables", E("renewable", **attrs)))


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
    """A place with rules of its own: nobody may `place` or `break_` blocks in it when those are False, nobody is hurt
    there when `damage` is False, only the team `enter` names may come in (nobody at all when it is "never"), and
    whoever is inside is given `kit`. `boxes` are one or more Boxes; a team's zone turns with the board, its id and
    the team let in carried to the other side."""
    id: str
    boxes: list
    place: bool = True
    break_: bool = True
    damage: bool = True
    message: str = None
    team: str = None
    enter: str = None                    # the only ones who may come in: a team's id
    enter_message: str = None
    kit: str = None

    def turned(self, sym):
        from dataclasses import replace
        return replace(self, boxes=[b.image(sym) for b in self.boxes])

    def image(self, sym, teams):
        from dataclasses import replace
        img = super().image(sym, teams)
        return replace(img, enter=teams.next(self.enter)) if self.enter and self.enter != "never" else img

    def write(self, doc, teams):
        shape = self.boxes[0].cuboid() if len(self.boxes) == 1 else union(*[b.cuboid() for b in self.boxes])
        rid = doc.region(self.id, shape)
        if self.enter:
            who = "never" if self.enter == "never" else f"only-{teams.short(self.enter)}"
            doc.apply(enter=who, region=rid, message=self.enter_message)
        if self.kit:
            doc.apply(region=rid, kit=self.kit)
        if not (self.place and self.break_):
            doc.apply(region=rid, block_place=None if self.place else "never",
                      block_break=None if self.break_ else "never", message=self.message)
        if not self.damage:
            doc.child("damage", "deny").append(E("region", id=rid))

    def cells(self):
        return set().union(*[b.cells() for b in self.boxes])


@dataclass
class Bounds(Objective):
    """The edge of play: nobody may go outside `box`, nor build out there when `build` is False."""
    box: object
    message: str = "You may not leave the map!"
    build: bool = True
    id: str = "outside"
    team: str = None

    def write(self, doc, teams):
        rid = doc.region(self.id, negative(self.box.cuboid()))
        doc.apply(enter="never", block=None if self.build else "never", region=rid, message=self.message)


# ---- shops ---------------------------------------------------------------------------------------------------------
@dataclass
class Offer:
    """An item for sale, at `price` of `currency`."""
    item: Item
    price: int
    currency: str

    def element(self):
        el = self.item.element()
        el.set("price", str(self.price))
        el.set("currency", self.currency)
        return el


@dataclass
class Shop:
    """A shop: its categories, each (id, icon material, [Offer, ...]), and the shopkeepers who open it."""
    id: str
    name: str
    categories: list

    def write(self, doc):
        doc.child("shops").append(E("shop", *[E("category", *[o.element() for o in offers], id=cid, material=icon)
                                              for cid, icon, offers in self.categories], id=self.id, name=self.name))


@dataclass
class Shopkeeper(Objective):
    """Someone standing at a block who opens `shop`, facing yaw; a team's keeper turns with the board."""
    shop: str
    name: str
    at: tuple
    yaw: int = 0
    team: str = None

    def turned(self, sym):
        from dataclasses import replace
        from pgmvox.play.objectives import turn_yaw
        return replace(self, at=turn_point(self.at, sym), yaw=turn_yaw(self.yaw, sym))

    def write(self, doc, teams):
        x, y, z = self.at
        doc.child("shopkeepers").append(E("shopkeeper", text=f"{x + 0.5},{y},{z + 0.5}", shop=self.shop,
                                          name=self.name, yaw=self.yaw))

    def cells(self):
        return {(self.at[0], self.at[2])}


# ---- the whole map --------------------------------------------------------------------------------------------------
@dataclass
class Map:
    """Every part of a map.xml: its name and what it is played for, its authors, the objectives and every placed
    thing, the kits and what follows from those players spawn with, the build rule, the kill height, the match, and
    `parts` that move with it (play.logic: named filters, triggers, variables, gives, gamerules)."""
    name: str
    version: str
    objective: str
    gamemode: object = None
    authors: list = field(default_factory=list)
    contributors: list = field(default_factory=list)      # [(name, contribution)]
    objectives: object = None
    kit: Kit = None
    kits: list = field(default_factory=list)              # the other kits: a team's, a flag carrier's, a reset
    build: Build = None
    kill: object = None                                   # a KillHeight, or a list of them
    match: Match = None
    includes: list = field(default_factory=lambda: [KILL_REWARD_INCLUDE])
    rules: list = field(default_factory=list)             # lines shown to a player
    players: tuple = None                                 # (least, most) for a match without teams
    shops: list = field(default_factory=list)
    parts: list = field(default_factory=list)
    terrain: set = field(default_factory=set)              # the world's block ids: terrain_of(__file__)

    def spawn_kits(self):
        """The kits players spawn with, and every kit given with them: the main kit and those a spawn names."""
        every = {k.id: k for k in ([self.kit] if self.kit else []) + self.kits}
        named = [s.kit for s in self.objectives.of(Spawn)] if self.objectives else []
        out = []
        for k in ([self.kit] if self.kit else []) + [every[n] for n in dict.fromkeys(named) if n in every]:
            out += [x for x in k.lineage() if x not in out]
        return out

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
        for shop in self.shops:
            shop.write(d)
        for part in self.parts:
            part.write(d)
        if self.build:
            self.build.write(d)
        for k in (self.kill if isinstance(self.kill, (list, tuple)) else [self.kill] if self.kill else []):
            k.write(d)
        if self.match:
            self.match.write(d)
        standards(d, self.spawn_kits(), self._destroyed(), self.terrain)
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
