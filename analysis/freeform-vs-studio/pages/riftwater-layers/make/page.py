import os; D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "out"); ROOT = os.path.abspath(os.path.join(D, *[".."] * 5))
import json, base64, html
FJ = json.load(open(f"{OUT}/frames.json")); frames = {f["id"]: f for f in FJ["frames"]}
LIB, OWN, MIX = "Bibliothek", "eigener Code", "Bibliothek + eigener Code"
steps = [
 ("Umriss", "outline", "Inselumriss", "shapes.island · noise.line", MIX,
  "Der Kasten der roten Hälfte, jede Seite um eine wandernde Linie eingerückt. Die Ostkante ist die Lippe der Kluft: zerfranst, in Buchten gebissen und gerade gehalten unter der Stadt, an der Alten Brücke und an den Fällen. Die Lippe rechnet das Board noch selbst (_rift_edge)."),
 ("Gelände", "base", "Grundhöhe aus Termen", "field.terms · Ramp · Gauss · Noise · mix", LIB,
  "Drei Felder: nördlich des Flusses 48,5 mit zwei Rampen und einem Hügel bei (−44, −78), südlich 47,2 mit zwei Rampen, im Westen 52,5. Das Westfeld wird zwischen x −70 und −80 eingeblendet, dann kommt Rauschen in zwei Größen dazu. Die Kante in der Mitte ist die Grenze Nord/Süd, die das Tal im nächsten Schritt aufnimmt. Der Hügel unter Stadt und Kapelle entsteht hier und nirgends sonst: An der Kapelle (−46, −75) liegt der Boden auf 55 = 48,5 Grundhöhe + 2,5 aus der Rampe, die von der Kluft nach Westen steigt, + 4,1 aus dem Gauß-Hügel + 0,3 Rauschen. Kein späterer Schritt ändert dort etwas außer dem Runden auf ganze Blöcke. Die Terme einzeln stehen unter dem Bild."),
 ("Gelände", "valley", "Flusstal", "landform.profile ×2 (mode cut)", MIX,
  "Ein Querschnitt quer zur Flusslinie: auf der Stadtseite ein Steilufer über 7 Blöcke, auf der Feldseite ein flaches Ufer über 14. Beide senken nur. Der Talboden einen Block über dem Wasser ist noch eine Zeile Board-Code."),
 ("Gelände", "pond", "Mühlteich und Landzunge", "–", OWN,
  "Eine Ellipse mit Rauschen, ihr Ufer weich ins Gelände geblendet, eine Landzunge aus einer Linie. Das macht das Board von Hand; landform.lake würde es können, wird hier aber nicht benutzt."),
 ("Gelände", "ridge", "Bergrücken im Westen", "landform.ridge", LIB,
  "Der Fuß wandert um x −100 (noise.line), der Kamm liegt bei 73 ± 5 mit einem Buckel, die Krone ist rau, zwei Sporne greifen nach Osten, und der Hang ist in Terrassen von 3 Blöcken geschnitten. Er hebt nur."),
 ("Gelände", "westfall", "Abfall am Westrand", "–", OWN,
  "Ganz im Westen (x −114 bis −120) fällt das Gelände um 7 Blöcke ab. Eine Zeile Board-Code; als Ebene wäre es eine Rampe aus field.terms."),
 ("Gelände", "shoulder", "Spawn-Schulter", "landform.level (mode lift) · shapes.ellipse_distance", LIB,
  "Ein Oval um (−97, −7) mit rauem Rand, eben auf 59 für das Wachhaus, nach außen weich ins Gelände. Es hebt nur."),
 ("Gelände", "squares", "Marktplatz und Anger", "landform.blend", LIB,
  "Wo die Monumente stehen, wird der Boden auf ihre Höhe gebracht und über 8 Blöcke weich angeglichen."),
 ("Gelände", "knoll", "Lone Oak Knoll", "landform.spire (rz)", LIB,
  "Eine ovale Kuppe, 16 Blöcke quer und 20 lang, 6,5 Blöcke über dem Boden an ihrer Stelle."),
 ("Wasser", "river", "Flussbett", "landform.watercourse", LIB,
  "Das Bett wird 4 tief geschnitten, das Wasser steht 3 hoch, das Wehr wird zur Stufe. Der Fluss steigt nie an."),
 ("Wasser", "waterbeds", "Teichboden und Abfluss", "–", OWN,
  "Teichboden, Abfluss und das Bett unter jedem nassen Feld rechnet das Board selbst; der Teich bekommt eine Schüssel bis 3,5 Blöcke tief."),
 ("Wege und Plätze", "routes", "Wege", "landform.grade", LIB,
  "Jeder Weg wird der Reihe nach ins Gelände gelegt, Straßen 5, Gassen 3, Pfade 2 breit, mit höchstens 0,25 Steigung. Ein später Weg verändert keinen früheren."),
 ("Wege und Plätze", "plazas", "Platz und Anger exakt", "–", OWN,
  "Platz auf 52 mit abgerundeten Ecken, Anger auf 50. Nur noch 7 Spalten ändern sich, weil blend die Arbeit schon gemacht hat."),
 ("Wege und Plätze", "sinkhole", "Erdfall", "landform.crater", LIB,
  "Kein Polygon: ein Mittelpunkt (−50, 38) und ein Radius von 10,5. Die Schüssel reicht bis zum Höhlenboden auf 38, der Boden ist 1,5 Blöcke um die Mitte flach, dann steigt die Wand einen Block pro Block bis zum Rand: zu Fuß begehbar. Sie senkt nur. Unten auf der Seite steht sie als Datensatz."),
 ("Wege und Plätze", "spoil", "Abraumhalde", "landform.mound · shapes.ellipse_distance", LIB,
  "Auch kein Polygon: eine Ellipse um (−101, 79), 7 Blöcke quer und 5,6 lang, 6 Blöcke hoch in der Mitte, nach außen als 1 − d^1,6 flacher werdend. Sie hebt nur."),
 ("Unterseite", "underside", "Unterseite der Insel", "terrain.island_bottom", LIB,
  "Wie tief der Fels unter jeder Spalte reicht (hier dunkler = tiefer): unter der Kluft sofort 26 Blöcke und dann 1,2 pro Block, sonst 4 Blöcke am Rand und 0,9 pro Block nach innen."),
 ("Boden und Anstrich", "w-lay", "Boden legen", "terrain.lay · Strata · beds · by_angle", LIB,
  "Jede Spalte bis zur Höhe: Fels in Bänken, die der Oberfläche folgen, Erde je nach Neigung, oben der Block nach Neigung. Unter der Unterseite bleibt nichts."),
 ("Boden und Anstrich", "w-paint", "Malschichten", "terrain.Paint (9 Schichten)", LIB,
  "Wo welche der 9 Malschichten gewonnen hat; grün ist, wo keine greift und Gras bleibt. Gelb und grau am Fluss: Sand und Kies an der Uferlippe. Braun: grobe Erde an Kanten (33–38°) und Flecken an Hängen (38–55°). Grau-weiß: Stein, Andesit und Bruchstein ab 55°. Die erste Schicht, die passt, gewinnt."),
 ("Boden und Anstrich", "w-fill_water", "Wasser", "terrain.fill_water", LIB,
  "Bett und Wasser in jeder nassen Spalte: im stehenden Wasser Ton, Sand und Erde, im Fluss Kies, Sand und Andesit."),
 ("Boden und Anstrich", "w-waterfall", "Wasserfall", "terrain.waterfall", LIB,
  "Der Fluss fällt über die Lippe in die Kluft bis y 8, nur in Luft."),
 ("Raum 3D", "w-under", "Höhlen und Mine", "under.tunnel · chamber · dress_cave · gallery · shaft", LIB,
  "Die Höhle hinter dem Fall, der Gang zum Erdfall, der Kerker und die Mine mit Schacht. Markiert sind die Spalten, unter deren Oberfläche etwas ausgehöhlt oder gebaut wurde."),
 ("Bauten", "w-works", "Häuser, Bauwerke, Straßen", "build.house · site · stairs · parapet · facade.carpet · route.pave", MIX,
  "29 Häuser auf ihren Bauplätzen, der Platz als Teppich, die Treppen der Terrasse, der Wachturm mit Brüstung und die gepflasterten Straßen kommen aus der Bibliothek. Mühle mit Rad und Wehr, Steinbrücke, der Stumpf der Alten Brücke, Förderturm, Schornstein, Schmiede und Brunnen sind Board-Code: dafür hat die Bibliothek noch keine Bausteine."),
 ("Bauten", "w-stalls", "Marktstände", "props.stalls", LIB, "Eine Reihe Stände an der Westkante des Platzes."),
 ("Ausstattung", "w-dress_before_field", "Bäume", "trees.plant · trees.scatter", LIB,
  "Die Wälder aus den gebauten Bäumen der Bibliothek, Einzelbäume abseits der Monumente und die große Eiche auf der Kuppe."),
 ("Ausstattung", "w-crop_field", "Feld", "props.crop_field · props.scarecrow", LIB,
  "Weizen, Karotten und Kartoffeln in Streifen, ein Graben in jedem Streifen, Zaun mit Tor, Vogelscheuche."),
 ("Ausstattung", "w-dress", "Rest der Ausstattung", "–", OWN, "Der Holzplatz mit Stümpfen und zwei Holzstapeln, Ranken an der Kluftwand, Gras, Farn und Blumen auf dem offenen Gras."),
 ("Symmetrie", "w-mirror", "Blaue Hälfte", "orient.turn_world", LIB,
  "Die rote Hälfte wird an der Kluft gespiegelt, die Wolle wird umgefärbt. Ab hier zeigt das Bild das ganze Board."),
 ("Spielteile", "w-objectives", "Monumente und Spawns", "objectives", LIB,
  "Die vier Monumente, drei Blöcke über dem Boden schwebend, und die Spawns werden zuletzt gesetzt."),
]
unused = [
 ("landform.canyon", "Schlucht entlang einer Linie, nur senkend"), ("landform.lake", "See mit Ufer – hier von Hand gemacht"),
 ("landform.coast", "Küste und Meer an einem Umriss"), ("landform.butte", "Tafelberg mit Klippe und Schutthang"),
 ("landform.scarp", "Stufe im Gelände entlang einer Linie"), ("landform.stage", "gestufte Bühne in Ringen"),
 ("landform.spire_sites / spire_field", "Felsnadeln und Hoodoos, zufällig verteilt"),
 ("field.Tilt", "schiefe Ebene"), ("noise.ragged", "zerfranste Kante in ganzen Blöcken"),
 ("terrain.slab", "schwebende Plattformen auf eigener Höhe"), ("terrain.underside · root_depth", "Unterseite als Kegel mit Riefen und Zapfen"),
 ("terrain.mountain_ring", "Bergkranz außerhalb des Spielfelds"), ("terrain.cloud_deck", "Wolkendecke unter der Insel"),
 ("terrain.bed_offset", "Gesteinsbänke, die kippen und sich falten"),
 ("forms.arch", "Felsbogen"), ("forms.tower · skirt · root_vines", "Karsttürme, Karstwände unter Plattformen, Ranken"),
 ("forms.masonry_tower", "gemauerter Turm mit Leiter"), ("under.bore", "senkrechte Bohrung, durch die ein Core ausläuft"),
 ("props.lamps · brazier · rubble", "Laternenreihe, Feuerschale, Geröll"), ("trees.dead_tree", "toter Baum"),
]
img = lambda n: "data:image/png;base64," + base64.b64encode(open(f"{OUT}/img/{n}.png", "rb").read()).decode()
data = []
for group, fid, title, fn, kind, text in steps:
    f = frames[fid]
    data.append(dict(group=group, title=title, fn=fn, kind=kind, text=text, img=img(f["img"]), changed=f["changed"], w=f["w"], h=f.get("h"), unit=f.get("unit"), id=fid,
                     relief=fid not in ("outline",) and not fid.startswith("w-") or fid == "w-paint"))
phases = [
 ("Info", "Name, Größe, Symmetrie", "bleibt"),
 ("Draw: Rechteck, Polygon, Polylinie, Lasso", "Formen zeichnen und stapeln", "Die Werkzeuge bleiben. Sie zeichnen den Bereich oder die Linie einer Ebene: den Inselumriss, den Bereich eines Hügels, die Linie eines Flusses, einer Schlucht oder eines Grats."),
 ("Draw: bauen ⇄ schneiden", "positive und negative Formen, Löcher", "wird zum Modus einer Ebene: heben, senken oder setzen. Löcher durch die Insel, Grüfte und Gänge werden 3D-Ebenen (Tunnel, Kammer, Bohrung) statt Ausschnitt mit Deckel."),
 ("Draw: Stockwerke", "übereinanderliegende Ebenen", "schwebende Plattformen werden eine Ebenenart (slab) mit eigener Höhe."),
 ("Relief", "Höhenmarken und Grain", "Höhenmarken bleiben eine Ebenenart unter vielen. Dazu kommen die neuen Formen als Ebenen (Terme, Querschnitt, Grat, ebene Fläche, Kuppe, Krater, Fluss, Weg …), und Rauschen wird eine eigene Ebene mit Bereich."),
 ("Theme", "ein Thema pro Form", "wird zu Malschichten: jede mit Bedingungen (Neigung, Bereich, Rauschen), die erste passende gewinnt. Themen bleiben als Material, das eine Schicht aufträgt."),
 ("Dressing", "Bäume, Felsen, Bodenbewuchs, Wasser, Gebäude", "bleibt als Ebenengruppe; Feld, Wasserfall und Wasser nach Füllstand kommen dazu."),
 ("Review mit Notizen", "Kameras und Anmerkungen", "bleibt. Notizen hängen dann an Ebenen und Orten, nicht nur an Positionen."),
 ("History", "Verlauf des Dokuments", "bleibt, und jede Ebene zeigt, welche Spalten sie geändert hat – so wie die Markierung unten."),
]
rows = "".join(f"<tr><th scope='row'>{html.escape(a)}</th><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>" for a, b, c in phases)
un = "".join(f"<li><code>{html.escape(a)}</code> – {html.escape(b)}</li>" for a, b in unused)
for t in FJ["terms"]:
    t["img"] = img(t["img"])
for k, v in FJ["shapes"].items():
    v["before"], v["after"] = img(v["before"]), img(v["after"])
forms = json.load(open(f"{OUT}/forms.json"))
for t in forms: t["img"] = img(t["img"])
soft = json.load(open(f"{OUT}/soft.json"))
for t in soft["tiles"]: t["img"] = img(t["img"])
extra = dict(soft=soft, forms=forms, terms=FJ["terms"], shapes=FJ["shapes"], legend=FJ["legend"], places=FJ["places"], X_MIN=FJ["X_MIN"], Z_MIN=FJ["Z_MIN"], nz=FJ["nz"])
page = open(f"{D}/template.html").read().replace("%EXTRA%", json.dumps(extra)).replace("%OVERLAY%", img("overlay")).replace("%ROWS%", rows).replace("%UNUSED%", un).replace("%DATA%", json.dumps(data))
open(os.path.join(D, "..", "index.html"), "w").write(page)
print(len(page))
