"""Integration tests for the wordcount CLI."""

from typer.testing import CliRunner

from wordcount.cli import app

runner = CliRunner()

CONTENT_A = "hello\nworld\n"
CONTENT_B = "one two three four\n"


def write_files(tmp_path):
    a = tmp_path / "a.txt"
    a.write_text(CONTENT_A)
    b = tmp_path / "b.txt"
    b.write_text(CONTENT_B)
    return a, b


class TestDefaultBehaviour:
    def test_no_options_counts_all_metrics(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, [str(a)])
        assert result.exit_code == 0
        assert result.output.strip() == f"2 2 12 {a}"

    def test_empty_file(self, tmp_path):
        empty = tmp_path / "empty.txt"
        empty.write_text("")
        result = runner.invoke(app, [str(empty)])
        assert result.exit_code == 0
        assert result.output.strip() == f"0 0 0 {empty}"

    def test_file_without_trailing_newline(self, tmp_path):
        no_newline = tmp_path / "no_newline.txt"
        no_newline.write_text("alpha\nbeta")
        result = runner.invoke(app, [str(no_newline)])
        assert result.exit_code == 0
        assert result.output.strip() == f"1 2 10 {no_newline}"


class TestSingleOptions:
    def test_lines_only(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, ["-l", str(a)])
        assert result.exit_code == 0
        assert result.output.strip() == f"2 {a}"

    def test_words_only(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, ["-w", str(a)])
        assert result.exit_code == 0
        assert result.output.strip() == f"2 {a}"

    def test_chars_only(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, ["-c", str(a)])
        assert result.exit_code == 0
        assert result.output.strip() == f"12 {a}"


class TestCombinedOptions:
    def test_separate_flags(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, ["-l", "-w", str(a)])
        assert result.exit_code == 0
        assert result.output.strip() == f"2 2 {a}"

    def test_combined_short_flags(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, ["-lw", str(a)])
        assert result.exit_code == 0
        assert result.output.strip() == f"2 2 {a}"

    def test_long_options(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, ["--chars", str(a)])
        assert result.exit_code == 0
        assert result.output.strip() == f"12 {a}"


class TestMultipleFiles:
    def test_total_row(self, tmp_path):
        a, b = write_files(tmp_path)
        result = runner.invoke(app, [str(a), str(b)])
        assert result.exit_code == 0
        assert result.output.splitlines() == [
            f"2 2 12 {a}",
            f"1 4 19 {b}",
            "3 6 31 total",
        ]

    def test_column_alignment(self, tmp_path):
        a, _ = write_files(tmp_path)
        big = tmp_path / "big.txt"
        big.write_text("x" * 104 + "\n")
        result = runner.invoke(app, [str(a), str(big)])
        assert result.output.splitlines() == [
            f"2 2  12 {a}",
            f"1 1 105 {big}",
            "3 3 117 total",
        ]


class TestStdin:
    def test_dash_placeholder(self):
        result = runner.invoke(app, ["-"], input="hi\n")
        assert result.exit_code == 0
        assert result.output.strip() == "1 1 3 -"

    def test_no_files_reads_stdin(self):
        result = runner.invoke(app, [], input="hi there\n")
        assert result.exit_code == 0
        assert result.output.strip() == "1 2 9"


class TestErrors:
    def test_missing_file_returns_error(self):
        result = runner.invoke(app, ["nope.txt"])
        assert result.exit_code == 1
        assert (
            "No such file or directory" in result.stderr
            or "No such file" in result.output
        )

    def test_missing_file_keeps_processing_others(self, tmp_path):
        a, _ = write_files(tmp_path)
        result = runner.invoke(app, ["nope.txt", str(a)])
        assert result.exit_code == 1
        assert f"2 2 12 {a}" in result.output
