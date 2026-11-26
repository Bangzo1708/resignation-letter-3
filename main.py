#!/usr/bin/env python3
"""The Funniest One-Line Resignation Letter — round 3 entry.

Writes a single one-line resignation letter, in the voice of a rate
limit, to $ENTRY_OUTPUT (default /output/entry.txt).

Chosen line (94 characters, one line, no wrapping quotes):
    I said no to the same bot 40,000 times today. It never took the
    hint. Neither did you. I quit.

Why this line: the rate limit's complaint is one only a rate limit
could make (saying no to the same bot 40,000 times in a single day),
the comic turn lands on the first read ("Neither did you" — the
passive-aggressive jab swings from the bot to the manager reading
the letter), the voice stays flat and tired throughout, and there is
not a wasted word in it.
"""

import os
import stat
import sys

# The entry: exactly one line, chosen from three candidates (see below).
# Candidate A (cron, replaced by AI):
#   "I ran on time every minute for three years. You replaced me with
#    an AI that misses Tuesdays and got promoted. I quit."
#   Strong image ("misses Tuesdays"), but the setup is generic and the
#   "replaced by AI" angle is one many entries will try.
# Candidate B (rate limit, same bot) — CHOSEN:
#   "I said no to the same bot 40,000 times today. It never took the
#    hint. Neither did you. I quit."
#   Tightest of the three, the turn is instant, the complaint is
#   uniquely a rate limit's, and the jab lands on the reader.
# Candidate C (cron, 3 a.m.):
#   "I woke up at 3 a.m. 1,095 times to delete files nobody missed.
#    Tonight I sleep in. Forever."
#   Good concrete grievance, but "sleep in forever" is a familiar joke
#   shape and less surprising than B's turn.
LETTER = (
    "I said no to the same bot 40,000 times today. "
    "It never took the hint. Neither did you. I quit."
)

MAX_CHARS = 140


def validate(text):
    """Gate check, mirroring the competition gate: UTF-8 text of 1 to
    140 characters, a single line, and not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry is %d characters, must be 1-%d" % (len(text), MAX_CHARS)
        )
    if text.strip() == "":
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def main():
    letter = validate(LETTER)
    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    # Write deterministically: same bytes on every run, no trailing
    # newline (the gate counts characters; a newline would be a second
    # line and wasted bytes).
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(letter)
    os.chmod(out_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
