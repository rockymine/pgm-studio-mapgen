# pgmvox operations and their parameters

Generated from the library's function signatures (pgmvox 0.23.0) for the recipe design in `../STUDIO-2-DESIGN.md`: every operation a recipe step could name, with each parameter a model would send and its default. The grid arguments (`w`, `H`, `X`, `Z`, `rng`) are the recipe's state, not parameters.

| op | parameters (defaults) |
|---|---|
| `landform.watercourse` | pts, width=6, depth=2, water=1, bank=4, fall_min=2, reach_min=10, lowest=None, into=None |
| `landform.lake` | centre, r, level, depth=3, shore=3, rz=None, jag=0.2, seed=0 |
| `landform.hold` | *waters |
| `landform.canyon` | pts, width=20, depth=12, floor=0.35, wall=2.5, ledges=0, downhill=False, lowest=None |
| `landform.spire` | centre, r, top, taper=1.6, jag=0.15, seed=0, rz=None, angle=0.0 |
| `landform.butte` | centre, r, top, cliff=1.5, talus=6, talus_height=0.3, jag=0.12, seed=0, rz=None, angle=0.0 |
| `landform.scarp` | pts, height, side=1, cliff=2, talus=5, talus_height=0.3, reach=None |
| `landform.terraces` | mask, step=4, base=None, riser=1.0 |
| `landform.stage` | centre, rings, jag=0.0, seed=0 |
| `landform.grade` | pts, width=5, max_grade=0.25, shoulder=4, water=None, keep=None |
| `landform.coast` | sea, outline=None, shelf=10, depth=6, slope=0.35 |
| `landform.blend` | Ha, Hb, mask, width=8 |
| `terrain.lay` | mask=None, top=None, under=(3, 0), rock=(1, 0), dirt_depth=None, snow_above=None, snow=(80, 0), bands=None, from_y=1, soil=((25, 3), (38, 2), (55, 1)), ledges=True, paint=None, bottom=None |
| `terrain.Strata` | choices, length=160, seed=0, start=0, below=(1, 0) |
| `terrain.bed_offset` | shape, dip=(0.0, 0.0), fold=0.0, cell=24, seed=0 |
| `terrain.beds` | strata, offset=None, flecks=(), seed=0 |
| `terrain.by_angle` | stops |
| `terrain.mountain_ring` | clear, rise=45.0, base=45.0, relief=45.0, crest=80.0, seed=21, cell=40, ridge_cell=20, massif=0.3, edge=None, smooth=2.5, square=0.0 |
| `terrain.root_depth` | mask, cone=3.2, power=0.85, rough=0.35, flutes=0.0, flute_cell=5, spires=0.0, spire_cell=18, cap=None, seed=0 |
| `terrain.underside` | mask, top_y, depth=<function>, paint=None, jitter=1 |
| `terrain.cloud_deck` | y, mask=None, seed=7, cell=14, puff=9, breaks=-0.25, materials=((35, 0), (80, 0)) |
| `noise.fbm` | shape, cell, octaves=4, seed=0, gain=0.5 |
| `noise.ridged` | shape, cell, octaves=4, seed=0, gain=0.5, sharpness=1.0 |
| `route.find` | start, goal, max_grade=0.15, cell=3, reach=4, turn=6.0, climb=2.0, steep=40.0, water=None, bridge=6.0, avoid=None, prefer=None, reuse=0.35, goals=None |
| `route.network` | places, order=None, width=4, **kw |
| `route.pave` | pts, width=4, surface=((13, 0), (3, 1), (4, 0)), weights=(0.6, 0.3, 0.1), water=None, deck=(5, 1), rail=(85, 0), clear=3, seed=0, level=None, keep=None |
| `route.steps` | pts, block=67, width=1 |
| `route.simplify` | pts, tolerance=1.5 |
| `route.smooth` | pts, rounds=2 |
| `under.tunnel` | pts, ground=None, cover=3, keep=None, lift=0.45 |
| `under.chamber` | cx, floor_y, cz, rx, h, rz=None, ground=None, cover=3, keep=None |
| `under.carve` | cells, floor=None, ground=None, cover=3, keep=None |
| `under.dress_cave` | box, ground=None, cover=2, keep=None, floors=((13, 0), (1, 5), (82, 0), (4, 0)), weights=(0.45, 0.25, 0.1, 0.2), mushrooms=0.015, stalactites=0.05, ores=300, stalagmites=900, ore_blocks=((16, 0.6), (15, 0.4)) |
| `under.gallery` | line, timber=(17, 1), fence=(188, 0), stair=67, every=4, rails=True, torches=12, floor=((13, 0), (1, 0), (1, 5)), ore=(15, 0) |
| `under.shaft` | x, z, bottom, top, wall=(5, 1), post=(17, 1), ladder_on='s', foot=3 |
| `forms.tower` | cx, cz, y0, top, r, rock, taper=(1.15, 0.7), ledge_every=9, ledge=0.8, bulge=1.4, cell=4, seed=0, through=(0, 95, 20), crown=(2, 0), crown_r=0.7, tree=None, vines=6 |
| `forms.skirt` | land, floor, rock, bulge=None, reach=(0.05, 0.3), moss=0.12, grass=0.5, undercut=-0.25, keep=None, seed=15 |
| `forms.root_vines` | land, floor, bottom, chance=0.05, under=9, length=(3, 10), keep=None |
| `build.House` | cx, cz, heading=0.0, L=9, W=6, floor=64, storeys=2, storey=4, style='town', jetty=False, door=1, chimney=True, roof='gable', pitch=1, overhang=1, windows=<factory> |
| `build.house` | h, ground_at=None |
| `build.site` | cells, floor_y, ground_at, margin=2, fill=(1, 0), top=(2, 0), under=(3, 0), clear=12 |
| `build.stairs` | x, z, rises, y0, n, block, width=1, under=None |
| `build.ladder` | x, z, y0, y1, on_wall |
| `build.parapet` | cells, y, block, crenel=None, rhythm=None |
| `trees.plant` | x, z, tree, turn=0, allowed=None, through={0, 161, 37, 38, 106, 175, 18, 31}, gives_way={1, 2, 3, 4, 13} |
| `trees.scatter` | zone, by_kind, weights, spacing=0.85, tries=4000, planted=None, ok=None, allowed=None |
| `props.stall` | x, y, z, facing='e', awning=14, stripe=0, post=(85, 0), goods=None, chest=True |
| `props.stalls` | line, y, facing='e', every=5, awnings=(14, 4, 11, 13), stripe=0 |
| `props.lamp` | x, y, z, height=3, post=(85, 0), light=(89, 0), cap=(126, 5) |
| `props.wool_chests` | box, floor, door='s' |
| `props.defence_chests` | cells, y, facing='s' |
| `grammar.Section` | boxes, y, name=None, fill=None, tags=frozenset(), motifs=(), tops=() |
| `grammar.Face` | courses, accent=None, floor=3 |
| `grammar.Accent` | module, frame, inner, every=2, phase=0, min_air=5, align='grid', margin=0 |
| `grammar.Style` | name, body, faces, seam, fills, choose, motifs=<factory>, params=<factory> |
| `grammar.lay` | ground, style, only=None, face_of=None, params=None, where=None, bodiless=() |
| `grammar.split` | box, nx, nz, y, name='section', **kw |
| `grammar.tile` | box, module, y, name='section', **kw |
| `brittle.build` | cells, only=None, dye=14, fill=None, style=Style(…), grown=None |
| `brittle.house` | layers, floor, dye, door=None, cobwebs=True, floor_block=(5, 0) |
| `brittle.tower` | box, base_y, tiers, dye, door=None, crown=(41, 0) |
| `noise.line` | shape, along, cell, octaves=2, seed=0, amp=1.0, base=0.0, clip=None |
| `noise.ragged` | shape, along, cell, amp, seed=0 |
| `shapes.island` | box, west=0, east=0, north=0, south=0, cuts=() |
| `shapes.ellipse_distance` | at, rx, rz=None, angle=0.0 |
| `shapes.scatter_points` | mask, n, min_d, taken=() |
| `field.terms` | base, *parts |
| `field.Ramp` | along, frm, to, rise |
| `field.Gauss` | at, r, rise, rz=None, power=2, angle=0.0 |
| `field.Tilt` | dx, dz, at=(0, 0) |
| `field.Noise` | field, rise |
| `field.mix` | a, b, weight |
| `landform.profile` | d, floor, steps, floor_ground=None, jag=0.0, talus=None, mode='set' |
| `landform.Step` | start, end, top, ground=None |
| `landform.level` | e, top='median', inner=1.0, outer=1.5, mode='set' |
| `landform.mound` | e, rise, power=1.6, mode='lift' |
| `landform.crater` | e, floor, r, flat=0.0, slope=1.0 |
| `landform.ridge` | coord, foot, reach, crest, rough=0.0, spurs=(), terrace=None |
| `landform.spire_sites` | box, n, r=(1.6, 3.4), rise=(8, 22), needles=0.7, spacing=2.5, keep_clear=(), seed=0, tries=400 |
| `landform.spire_field` | sites, needle=1.3, hoodoo=5.0 |
| `terrain.Paint` | block, slope=None, where=None, values=() |
| `terrain.fill_water` | level, bed, mask=None |
| `terrain.island_bottom` | top, land, sheer, taper=(4, 0.9), sheer_taper=(26, 1.2), rough=0.0, floor=0.0 |
| `terrain.slab` | floor, land, bands, root, plate=5, foundation=3, paint=None, rim=None, **lay_args |
| `terrain.waterfall` | level, at, toward='east', lip_from=None, to=None, to_y=8 |
| `forms.arch` | cells, t, deck, thick, rock, into=None, clear=0, ground=None |
| `forms.masonry_tower` | x0, z0, x1, z1, y0, height, wall=((98, 0), (98, 0), (98, 2)), corner=(98, 3), floor=(5, 5), slit=(101, 0), door=197, door_side='s', crown=(98, 0), crenel=(139, 0), light=(89, 0), ladder_on='n' |
| `props.crop_field` | box, y, crops, rows=9, ditch=4, tilt=0.0, ripe=(0.15, (4, 8)), fence='w', gate=None |
| `props.scarecrow` | x, z, facing='n' |
| `props.lamps` | path, every=12, post=(113, 0), light=(89, 0), height=2, side=3.0, start=6 |
| `props.brazier` | x, y, z, post=(113, 0), light=(89, 0), height=2, base=(139, 0) |
| `props.rubble` | x, y, z, r=1.6, blocks=((1, 5), (4, 0), (1, 0), (13, 0)), supported=True |
| `trees.dead_tree` | x, y, z, h, log=162, kind=1 |
| `under.bore` | at, r, y0, y1, seed=0, r_noise=0.0, fill=(0, 0), lip=None |

603 parameters over the operations listed
