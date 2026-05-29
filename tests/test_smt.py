"""Tests for the SMT backend.

SMT is unlike every other py2many target: its input cases are *not* runnable
Python. They declare constraints (datatypes, equations, a sudoku, ...) that
py2many lowers to SMT-LIB2 for a solver such as z3. The cases have no
``__main__``, produce no stdout to diff, and fail on every other language, so
they live under ``tests/smt/`` (their own ``cases``/``expected`` dirs) rather
than the shared ``tests/cases`` matrix, and are exercised here instead.

Each case is transpiled to ``.smt`` and compared against its committed expected
output. When z3 is available the generated file is additionally fed to it to
confirm it is well-formed SMT-LIB2 (the solver returns sat/unsat/unknown rather
than a parse error).
"""

import os
from pathlib import Path
from unittest.mock import Mock

import pytest

import py2many.cli
from py2many.cli import _create_cmd, _get_all_settings, main
from py2many.cli import _run as run
from py2many.process_helpers import find_executable
from py2many.pysmt.inference import SMT_CONTAINER_TYPE_MAP

TESTS_DIR = Path(__file__).parent.absolute()
SMT_DIR = TESTS_DIR / "smt"
CASES_DIR = SMT_DIR / "cases"
EXPECTED_DIR = SMT_DIR / "expected"
BUILD_DIR = TESTS_DIR / "build"
GENERATED_DIR = BUILD_DIR

KEEP_GENERATED = os.environ.get("KEEP_GENERATED", False)
UPDATE_EXPECTED = os.environ.get("UPDATE_EXPECTED", False)

# The SMT cases are exactly those with a committed ``.smt`` expected output.
SMT_CASES = sorted(p.stem for p in EXPECTED_DIR.glob("*.smt"))


class TestSMT:
    UPDATE_EXPECTED = UPDATE_EXPECTED
    KEEP_GENERATED = KEEP_GENERATED

    @classmethod
    def setup_class(cls):
        os.makedirs(BUILD_DIR, exist_ok=True)
        os.chdir(BUILD_DIR)
        py2many.cli.CWD = BUILD_DIR

    @pytest.mark.parametrize("case", SMT_CASES)
    def test_generated(self, case):
        settings = _get_all_settings(Mock(indent=4))["smt"]
        ext = settings.ext
        expected_filename = EXPECTED_DIR / f"{case}{ext}"
        case_filename = CASES_DIR / f"{case}.py"
        case_output = GENERATED_DIR / f"{case}{ext}"

        if settings.formatter and not find_executable(settings.formatter[0]):
            pytest.skip(f"{settings.formatter[0]} not available")

        try:
            rv = main(
                args=[
                    "--smt",
                    "--comment-unsupported",
                    str(case_filename),
                    "--outdir",
                    str(GENERATED_DIR),
                ]
            )
            generated = case_output.read_text()

            if self.UPDATE_EXPECTED:
                expected_filename.write_text(generated)
            else:
                assert expected_filename.read_text() == generated

            assert rv == 0, "formatting failed"

            # SMT is declarative -- there is nothing to run, but z3 can confirm
            # the output parses as well-formed SMT-LIB2 (sat/unsat/unknown, not a
            # parse error). Skip cleanly when z3 isn't installed.
            if find_executable("z3"):
                cmd = _create_cmd(
                    ["z3", "-smt2"], filename=case_output, exe=case_output
                )
                proc = run(cmd, check=False, capture_output=True)
                out = (proc.stdout or b"").decode("utf-8", "replace")
                err = (proc.stderr or b"").decode("utf-8", "replace")
                assert proc.returncode == 0, (
                    f"z3 rejected {case}{ext} (exit={proc.returncode})\n{out}{err}"
                )
        finally:
            if not self.KEEP_GENERATED:
                case_output.unlink(missing_ok=True)
