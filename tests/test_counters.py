"""Unit tests for the pure counting helpers."""

from wordcount.counters import count_text


class TestLines:
    def test_multiple_lines(self):
        counts = count_text("one\ntwo\nthree\n")
        assert counts.lines == 3

    def test_single_line_without_trailing_newline(self):
        counts = count_text("one")
        assert counts.lines == 0

    def test_multiple_lines_without_trailing_newline(self):
        counts = count_text("one\ntwo\nthree")
        assert counts.lines == 2

    def test_empty_text(self):
        counts = count_text("")
        assert counts.lines == 0

    def test_double_newline_counts_line(self):
        counts = count_text("one\n\n")
        assert counts.lines == 2


class TestWords:
    def test_space_separated(self):
        counts = count_text("hello world\n")
        assert counts.words == 2

    def test_tabs_and_newlines_separate_words(self):
        counts = count_text("one\ttwo\nthree")
        assert counts.words == 3

    def test_empty_text(self):
        counts = count_text("")
        assert counts.words == 0

    def test_whitespace_only(self):
        counts = count_text("   \n\t  ")
        assert counts.words == 0

    def test_unicode_words(self):
        counts = count_text("café ñandú 日本語")
        assert counts.words == 3


class TestChars:
    def test_ascii(self):
        counts = count_text("abc")
        assert counts.chars == 3

    def test_unicode_characters(self):
        counts = count_text("café😀")
        assert counts.chars == 5

    def test_empty_text(self):
        counts = count_text("")
        assert counts.chars == 0


class TestCombined:
    def test_all_metrics_together(self):
        counts = count_text("one two\nthree\n")
        assert (counts.lines, counts.words, counts.chars) == (2, 3, 14)
