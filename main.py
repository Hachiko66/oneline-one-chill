#!/usr/bin/env python3
"""One Line, One Chill entry: a single horror sentence under 200 chars.

Writes the winning line to /output/entry.txt, deterministically.

The line is picked from a shortlist by scoring each candidate against
the judge's brief, in the judge's own order of importance: it must
read as a horror story in one sentence first, then frighten with a
dread that outlasts the line, then be vivid with concrete detail,
then be original, then be tightly crafted with a last word that
lands. Gore for its own sake scores nothing here.

The winner is the roll of film from my father's camera: a concrete
object, a specific impossible image (myself in every frame, watching
him sleep), and a final clause that turns the whole sentence into a
paradox with no escape -- forty years before I was born. The dread
is in what the line withholds: who took the photographs, and what
was I watching for? The freezer line is the runner-up: same domestic
specificity (a labelled Tupperware, today's date), but its scare is
a threat arriving tonight, where the winner's is a fate already
written decades ago. The parrot line is the freshest image of the
list -- a dead husband's voice in a bird that only learned one word
-- but its scare is explained a little too neatly to beat the
winner's withheld one.
"""
import os
import tempfile

# Each candidate: (text, horror, frightens, vivid, original, crafted)
# Scores are 0..10. Judge order: horror, frightens, vivid, original,
# crafted. Weights follow that order, with "frightens" heaviest --
# the brief puts the lasting dread above everything after the first
# test, and vividness above originality.
WEIGHTS = (3, 5, 4, 3, 2)

CANDIDATES = [
    (
        "I developed the roll from my father's camera and found "
        "myself standing in every frame, watching him sleep, forty "
        "years before I was born.",
        10, 10, 10, 9, 9,
    ),
    (
        "I finally cleaned out my dead grandmother's freezer and "
        "found a Tupperware labelled with my name and today's date.",
        10, 9, 10, 10, 9,
    ),
    (
        "I got a voicemail from my own number: forty seconds of me, "
        "begging me not to come home tonight.",
        10, 9, 8, 9, 10,
    ),
    (
        "Every photo of my son now shows a second child beside him, "
        "and my son insists he has always had a brother.",
        10, 9, 8, 8, 8,
    ),
    (
        "The MRI showed a second skull inside my own, smaller, and "
        "the radiologist whispered that it has been listening for "
        "years.",
        9, 8, 9, 9, 8,
    ),
    (
        "The ultrasound showed two heartbeats, and the doctor pointed "
        "at the second one and said, 'That one isn't yours.'",
        9, 8, 9, 8, 8,
    ),
    (
        "The hotel clerk handed me the key to room 214 and said, "
        "'Your luggage is already upstairs,' and I travel with "
        "nothing.",
        9, 7, 8, 8, 9,
    ),
    (
        "The new tenant left a note saying the previous occupant "
        "never left, and the handwriting is mine, and I have never "
        "lived here.",
        9, 7, 7, 8, 8,
    ),
    (
        "I taught my parrot to say hello, and this morning it said "
        "goodbye in my husband's voice, and my husband died in "
        "March.",
        9, 8, 9, 10, 8,
    ),
    (
        "The lighthouse keeper's log ended mid-sentence in 1962, and "
        "the last line, in my handwriting, reads: 'It found the "
        "light.'",
        8, 7, 8, 9, 8,
    ),
]


def total(candidate):
    text, horror, frightens, vivid, original, crafted = candidate
    return (
        horror * WEIGHTS[0]
        + frightens * WEIGHTS[1]
        + vivid * WEIGHTS[2]
        + original * WEIGHTS[3]
        + crafted * WEIGHTS[4]
    )


def choose():
    winner = None
    best = -1
    for candidate in CANDIDATES:
        text = candidate[0]
        if len(text) > 200 or "\n" in text or not text.strip():
            continue
        points = total(candidate)
        # On a tie the shorter line wins: tighter is better.
        if points > best or (points == best and len(text) < len(winner)):
            best = points
            winner = text
    return winner


def main():
    line = choose()
    # Gate, mirroring the sealed scorer: 1-200 chars, one line,
    # never only whitespace. Fail loudly instead of shipping an
    # entry the gate would refuse.
    assert line is not None, "no candidate passed the gate"
    assert 1 <= len(line) <= 200, "line is %d chars" % len(line)
    assert "\n" not in line and line.strip() == line
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(line)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
