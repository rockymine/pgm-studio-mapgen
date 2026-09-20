#!/usr/bin/env python3
"""Gate the briefs on one paragraph, one claim.

    tools/prose-check.py [--fix-report] [path ...]

An instruction an agent reads once and acts on is not read the way a person reads
an essay: it is scanned for the sentence that applies, and a paragraph carrying six
claims hides five of them. This measures the tail rather than the average, because
the average was always fine and the tail is where the run goes wrong.

Two limits, both on PROSE paragraphs only — a table, a fenced block, a list and a
heading are none of this rule's business:

  words      a paragraph over the word cap is doing more than one job
  sentences  a paragraph over the sentence cap is usually two paragraphs

Exit 1 if anything is over. `--fix-report` prints the offenders with their opening
words so the pass has a work list rather than a count.
"""
import re, sys, glob, os

WORD_CAP = 110
SENTENCE_CAP = 4

DEFAULT = ["AUTHORING-BRIEF.md", "GENERATION-NOTES.md", "COMPOSER-ADAPTATION-BRIEF.md",
           "REVAMP-BRIEF.md", "SCULPTING-WITH-LAYERS.md",
           ".claude/skills/pgm-board/SKILL.md", ".claude/skills/pgm-board-warmup/SKILL.md"]

SKIP = ("```", "|", "- ", "* ", "#", ">", "    ", "\t")

# An ordered list item — "1. ", "12) " — is a list, and a list is not prose.
ORDERED = re.compile(r"^\d+[.)]\s")


def is_prose(block):
    head = block.lstrip()
    return not head.startswith(SKIP) and not ORDERED.match(head)


def paragraphs(text):
    """Prose paragraphs, with fenced blocks removed so a code comment is never counted."""
    out, fenced = [], False
    block = []
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.strip():
            block.append(line)
        elif block:
            out.append("\n".join(block)); block = []
    if block:
        out.append("\n".join(block))
    return [b for b in out if is_prose(b)]


def sentences(para):
    return len([s for s in re.split(r"(?<=[.!?])\s+", para.strip()) if s])


def words_of(text):
    """Every word of the prose, in order, lowercased and stripped of markup. A
    restructuring pass moves paragraph boundaries and may split a sentence in two;
    it must not drop a claim, so the word sequence is what is compared."""
    body = "\n\n".join(paragraphs(text))
    body = re.sub(r"[*_`]", "", body)
    return re.findall(r"[a-z0-9]+", body.lower())


def preserved(before, after):
    """True where the after-text still says everything the before-text said.

    The comparison is over the BAG of words rather than their order, because moving
    a sentence into a paragraph of its own is the whole point of a restructuring
    pass and an order-sensitive diff reports every such move as a loss. What it does
    catch is the thing that matters: a word that used to be in the document and is
    not any more."""
    import collections
    a = collections.Counter(words_of(open(before).read()))
    b = collections.Counter(words_of(open(after).read()))
    lost = a - b
    gained = b - a
    if lost:
        print("LOST %d word(s): %s" % (sum(lost.values()),
              ", ".join("%s x%d" % (w, n) for w, n in lost.most_common(25))))
        return False
    print("preserved: %d distinct words, none lost%s"
          % (len(a), ("; %d added" % sum(gained.values())) if gained else ""))
    return True


def main(argv):
    if "--preserved" in argv:
        i = argv.index("--preserved")
        return 0 if preserved(argv[i + 1], argv[i + 2]) else 1
    report = "--fix-report" in argv
    paths = [a for a in argv if not a.startswith("--")] or DEFAULT
    bad = 0
    for path in paths:
        if not os.path.exists(path):
            continue
        for i, para in enumerate(paragraphs(open(path).read())):
            flat = " ".join(para.split())
            words, sents = len(flat.split()), sentences(flat)
            if words <= WORD_CAP and sents <= SENTENCE_CAP:
                continue
            bad += 1
            why = []
            if words > WORD_CAP: why.append("%d words" % words)
            if sents > SENTENCE_CAP: why.append("%d sentences" % sents)
            print("%-44s %s" % (path, ", ".join(why)))
            if report:
                print("      %s" % flat[:130])
    print("\n%d paragraph(s) over the cap (%d words, %d sentences)" % (bad, WORD_CAP, SENTENCE_CAP))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
