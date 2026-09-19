"""Command-line interface for wordcount."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional, Tuple

import typer

from wordcount.counters import Counts, count_text

app = typer.Typer(help="Count lines, words and characters of files.")
DEFAULT_METRICS = ("lines", "words", "chars")


def _read_source(name: str) -> str:
    """Read file contents, or stdin when ``name`` is the dash placeholder."""
    if name == "-":
        return sys.stdin.read()
    return Path(name).read_text()


@app.command()
def main(
    files: List[str] = typer.Argument(
        None,
        help="Files to count. Use '-' for stdin, or omit to read stdin.",
    ),
    lines: bool = typer.Option(False, "-l", "--lines", help="Print line counts."),
    words: bool = typer.Option(False, "-w", "--words", help="Print word counts."),
    chars: bool = typer.Option(False, "-c", "--chars", help="Print character counts."),
) -> None:
    """Count lines, words and characters of files."""
    selected = [
        m
        for m, enabled in (
            (DEFAULT_METRICS[0], lines),
            (DEFAULT_METRICS[1], words),
            (DEFAULT_METRICS[2], chars),
        )
        if enabled
    ]
    if not selected:
        selected = list(DEFAULT_METRICS)

    records: List[Tuple[Counts, Optional[str]]] = []
    had_error = False

    if not files:
        records.append((count_text(sys.stdin.read()), None))
    else:
        for name in files:
            try:
                records.append((count_text(_read_source(name)), name))
            except FileNotFoundError:
                had_error = True
                typer.echo(f"wordcount: {name}: No such file or directory", err=True)

    if records:
        _print_records(records, selected)

    if had_error:
        raise typer.Exit(1)


def _print_records(
    records: List[Tuple[Counts, Optional[str]]], metrics: List[str]
) -> None:
    """Print counts right-aligned per column, optionally with a total row."""
    columns = [[getattr(counts, metric) for counts, _ in records] for metric in metrics]
    widths = [max(len(str(value)) for value in column) for column in columns]

    def format_row(counts: Counts, label: Optional[str]) -> str:
        values = [getattr(counts, metric) for metric in metrics]
        fields = " ".join(f"{value:>{width}}" for value, width in zip(values, widths))
        return f"{fields} {label}" if label else fields

    for counts, label in records:
        typer.echo(format_row(counts, label))

    if len(records) > 1:
        total = Counts(
            lines=sum(counts.lines for counts, _ in records),
            words=sum(counts.words for counts, _ in records),
            chars=sum(counts.chars for counts, _ in records),
        )
        typer.echo(format_row(total, "total"))


if __name__ == "__main__":
    app()
