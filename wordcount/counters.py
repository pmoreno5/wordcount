"""Pure counting helpers used by the wordcount CLI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Counts:
    """Line, word and character counts for a piece of text."""

    lines: int
    words: int
    chars: int


def count_text(text: str) -> Counts:
    """Count lines, words and characters in ``text``.

    A line is a string terminated by a newline, matching ``wc``: a final
    chunk without a trailing newline is not counted as a line. Words are
    maximal sequences of non-whitespace characters. Characters are counted
    as code points.
    """
    lines = text.count("\n")
    words = len(text.split())
    chars = len(text)
    return Counts(lines=lines, words=words, chars=chars)
