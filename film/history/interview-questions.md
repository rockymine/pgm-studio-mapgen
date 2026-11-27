# Interview questions — rockymine, Ruediger, Tttie

Prepared on 2026-11-27 for the history film (`film/NEXT-history-film.md`). Answers come later. Each question
cites the moment in the record that prompts it, and the questions are ordered the way the film would use them:
origin, method, the turn, now. Questions the record already answers are left out. Where the record says what
happened, the question asks *why*, *how it felt* or *what was decided*, because those parts are not written down.

**What the record holds on each person.**

- **rockymine** is the author of the studio and of the gameplay law (`[author]` paragraphs in
  `pgm-studio/docs/gameplay/`). Most of the record is theirs.
- **Ruediger (Ruediger_LP)** appears in three places. He hand-finished Millrace with rockymine
  (`review/rockymine-ruediger-millrace.md`, committed 2026-09-02 in `11d926f1`). He is named in the name of the
  studio's worked example plan, "the plan behind the Ruediger-themed CTW map" (`pgm-studio/docs/tools/plan.md`,
  `tools/seeds/ruediger.*.json`, added 2026-08-13). And he is listed beside rockymine as an author of "Bridgid II"
  in a test fixture (`tests/PgmStudio.Pgm.Tests/AuthorIntentJsonTests.cs`). A corpus map called `ruedigers_octawool`
  also appears in `tools/PgmStudio.RoundTrip/corpus-goldens.json`. Whether he made the Ruediger-themed map is not
  stated.
- **Tttie: nothing is recorded.** I ran `git log --all -i --grep=tttie` and `--author=tttie`, a content search
  (`git log --all -G`) and `grep -ri tttie` over the working trees and every remote branch of pgm-studio and
  pgm-studio-mapgen. The only hit is the film brief itself. The questions for Tttie therefore presume no role. They
  start by asking what it was.

---

## rockymine — 13 questions

1. **Before the studio.** The record begins before pgm-studio. `CTW-Layout-Generator` was made with Google's AI
   Studio, `MinecraftLayoutEditor` was self-built and `pgm-map-studio` was the Python stage (brief, 2026-11-27).
   What exactly did you see on screen the first time something drawn in a browser came out as blocks you could
   download? What did you think it could become that day?
2. **A map as a graph.** You name capture-the-wool as first because the void steers the flow, and you name "read a
   map as a graph" as the first idea (brief). When did the graph stop being enough? Was there a map that broke it?
3. **Hub, approaches, frontline, middle.** `docs/generator/model.md` calls this vocabulary "an intentional
   abstraction whose product is a low-fidelity prototype", and it keeps the Thunder series outside it on purpose:
   "That is a limitation rather than a defect, it is the author's stated position, and it stays." What did holding
   that line cost you? Was there a moment you were tempted to stretch the model instead?
4. **The floating core.** On 2026-08-13 a filed and committed claim said that every generated destroy map was
   unwinnable. It was withdrawn the same day (`6eec9b8b`, B104), and CLAUDE.md gained the rule that gameplay has a
   human oracle. What did you feel when you read that claim? What does it say about which parts of map-making you
   can hand to a model?
5. **Plans pushed out of shape by hand.** The "Map Experiment" commits of 2026-08-30 (`f956c846`, `2b46169c`,
   `e335971c`) took "pure plan pieces" and "deformed [them] by adding new points to the sketch shapes", with "new
   layers … to indicate stacked and sunken terrain". What were you testing there, and did it change what the
   studio became?
6. **Your own rules.** `WHAT-A-BOARD-IS-MADE-OF.md` (2026-09-19) opens: "Every board in `specs/` passed every gate
   and several of them look wrong … None of it is enforced anywhere." Why did you leave taste unenforced and write
   it down instead? Do you still think it cannot be enforced?
7. **Trees and houses.** You say trees are hard and houses work well (brief). Your own trees went in on 2026-09-02
   (`b36147a0`, "Add rockymine's custom trees") and replaced the grown ones on Millrace. What is a good tree to you
   that a generator could not yet produce?
8. **Opening it up.** Reads went public and writes went behind a whitelist on 2026-09-26 (`8c6655a6`, RP80). The
   studio deployed itself to pgmstudio.de from 2026-09-28 (`31033891`). Who did you picture using it? Has anyone
   used it in a way you did not expect?
9. **Starting over: pgmvox.** `docs/pgmvox-port.md` (2026-10-15) sets the goal: "a board built through the deployed
   studio that the author cannot tell apart, by quality, from one built with pgmvox". The 10 October experiment
   came first (`analysis/freeform-vs-studio/experiment/RESULTS.md`). What made you decide the first approach was
   limiting? Was that decision a relief or a loss?
10. **Measuring the rules.** The brief says the maps got clearly better but nobody measured which rule caused which
    gain, and that some rules still raise findings they should not. Name one rule you would bet made the biggest
    difference, and one you suspect does harm.
11. **Building it yourself.** On the fire-and-ice branch the composition was rejected on eleven counts, from "the
    surface was not closed" to "a ramp led into the void" (`sketches/fire-and-ice/study/LESSONS.md`, commits
    2026-11-02 to 11-07). Then "the author then built the map themselves". What was the moment you stopped
    correcting and picked up the tool yourself? What did you do first in that world?
12. **What a human sees.** You placed the east end of the middle "by eye" at the lane corner (97, 53). You gave the
    colours meaning: yellow connects, light blue climbs. You ruled that a retaining wall "does a big job or it is
    not there" (`LESSONS.md`, `study/variants/BRIEF.md`). Which of these judgements do you think a tool could learn
    one day, and which never?
13. **Letting the agents find it.** "The author stopped it, because the point was to see what agents find on their
    own" — the first variant launch had named a ravine you liked (`LESSONS.md`). Of the five accepted variants
    (Eismulde, Gletscherzungen, Pingo-Furt, Bunker unterm Berg, Firnsattel), which one surprised you, and would you
    build it into the map?

*Possible closer for rockymine:* the newest studio branch `ccr-875c17a4-2yjgux` is backlog clean-up and UI work,
and "the verification pipeline is not yet where it should be" (brief). What would "where it should be" look like?

---

## Ruediger (Ruediger_LP) — 11 questions

1. **How you came in.** The record first names you with rockymine as an author of "Bridgid II"
   (`AuthorIntentJsonTests.cs`), and the studio's worked example is "the plan behind the Ruediger-themed CTW map"
   (`docs/tools/plan.md`). How did you and rockymine start making maps together? What is that Ruediger-themed map
   to you?
2. **First look at an AI map.** Millrace (`opus5-millrace`) was built by Opus 5 through the studio, and the
   BOARDS-BUILT row describes it as "the basin flooded, walled in stone brick and bridged twice". When you first
   walked it in game, before touching anything, what did you think of it?
3. **Who did what.** The account is written in rockymine's voice ("myself (rockymine) and Ruediger_LP spent 5
   hours"). Which parts of those five hours were yours?
4. **What you kept.** "The terrain, spawn platform, spawn house, objetives, canal walls, water levels, bridges,
   boulders, and most house placements were kept intact" (review). Fable's diff measured "29,954 of 35,610 columns
   keep their surface height exactly" (`review/fable-millrace-revamp.md`). Was there something you wanted to move
   and decided to leave alone?
5. **The stone.** The stone body became a six-stone voronoi built with placeholder wools (`//r 22 #vor[7][35,22]`
   and the rest, review). How did you arrive at that recipe? Is it one you have used on maps before?
6. **The old-school dress.** "The destroyables received a sort of 'dress'. … pretty old-school style element
   actually. very old maps used these." (review). Why bring it back? What does it say to a player who knows the
   old maps?
7. **The tug and the statue.** The ship was replaced by "a 'Schlepper' that pulls heavy ships". The statue was taken
   from the Opus 5 Automaton map, team-coloured and given a diamond (review). Whose ideas were those, and why those
   two objects?
8. **Bugs found by hand.** You found holes at the bottom of the world under the walls and the ramp, "likely a bug in
   the script" (review). What else did you notice that a player would never see but a map maker would?
9. **The restatement.** Fable 5.1 restated your hand work as studio documents (`maps/dtcm/millrace_revamp`,
   `review/fable-millrace-revamp.md`, 2026-09-02). Have you seen it? Does it read as your work?
10. **Starting from AI ground.** Would you start a map of your own from a studio board? What would it have to get
    right before you would rather finish it than build from scratch?
11. **The hand-built map.** rockymine built the newest map, the fire-and-ice CTW + DTC hybrid set inside a
    mountain, by hand (`sketches/fire-and-ice/`, 2026-11). Have you seen it or helped with it? If you have, how
    does building one from nothing compare with finishing the AI's map?

---

## Tttie — 10 questions

*The repositories record nothing about Tttie, so no question presumes a role. Each one is tied to a public moment
that anyone close to the project or to PGM mapping might have met.*

1. **Who you are in this.** How would you describe your part in the year of these maps? Are you a player, a map
   maker, a tester, someone who watched it happen, or something else?
2. **The PGM background.** The studio's reference for "what authors actually build" is about 350 community maps
   (`OvercastCommunity/CommunityMaps` and `PublicMaps`, `pgm-studio/CLAUDE.md`). What is your history with those
   maps, or with PGM servers?
3. **First sight.** When did you first see a map that a model had made? Which one was it? What did you think it
   was, before anyone told you?
4. **Is this normal?** The record states that CTW and DTC together are 3 of 742 maps in the corpus
   (`pgm-studio/docs/pgm/destroyables-and-cores.md`). The newest map, rockymine's hand-built one, is exactly that
   mix. From where you stand, what makes a hybrid map work, or not?
5. **Floating goals.** A model once concluded that every generated destroy map was unwinnable because the core
   floated a few blocks above the ground. The core floats on purpose (`6eec9b8b`, 2026-08-13). What other thing
   about PGM maps would an outsider get wrong?
6. **The studio in a browser.** pgmstudio.de has been public to read since late September 2026 (`8c6655a6`,
   `31033891`). Have you used it? What did you try, and where did it stop you?
7. **The contest.** Six AI entries were built for a "Fire and Ice" contest on 2026-10-16, and all six chose Destroy
   the Core (BOARDS-BUILT on `claude/minecraft-bunker-walls-k90feq`). The contest was later cancelled
   (`sketches/fire-and-ice/study/LESSONS.md`). Did you know about the contest? What would have won it?
8. **The low point.** rockymine remembers a 500-block-wide map with its monuments and core in one line as a low
   (brief). Have you seen it? What does a map like that tell you about how a model thinks?
9. **Maps side by side.** The film will show maps from across the year next to each other. Looking at an early one
   and a recent one, what is the first difference you notice, and the first that you would notice playing?
10. **What it is for.** Should AI-made maps ever be played on a public server? Would you want to know that a map
    was made that way?

---

## Shared — 5 questions for all three

1. **The line.** Where is the line today between what the tool does well and what still needs a person? Has that
   line moved this year, and when did you notice it move?
2. **A map that is good.** The studio gates many things, but "no gate asks whether a board looks like anything"
   (`WHAT-A-BOARD-IS-MADE-OF.md`). Gameplay is "the author's call; it cannot be derived from the code"
   (`study/variants/BRIEF.md`). How do you know a map is good before anyone has played it?
3. **Hand versus generated.** In September, rockymine and Ruediger finished an AI map by hand. In November,
   rockymine built one from nothing to learn where the tool falls short. Which of the two taught more, and what?
4. **Naming the models.** The film names Opus, Sonnet, Haiku, Grok and Fable. If you could hand one sentence of
   advice to the next model that drives the studio, what would it be?
5. **One map.** Of everything made this year, by hand, by a model or by both, which single map would you show
   someone who has never played PGM, and why that one?

---

*Sources read: `pgm-studio/CLAUDE.md`; `pgm-studio/docs/gameplay/` (`approaches.md`, `match-flow.md` headings and
§10.5); `docs/backlog-strategy.md` opening; `docs/pgmvox-port.md` opening; `docs/generator/model.md` opening;
`docs/tools/plan.md` §worked example; pgm-studio-mapgen `CLAUDE.md`, `README.md`, `BOARDS-BUILT.md`, `review/rockymine-ruediger-millrace.md`,
`review/fable-millrace-revamp.md` opening, `WHAT-A-BOARD-IS-MADE-OF.md` opening; branch
`claude/compassionate-cerf-fg7m17` at `4486636d` (see `film/history/research/04-hand-built.md`).*
