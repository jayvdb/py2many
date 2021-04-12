import os.path
import unittest
import sys
from distutils import spawn
from pathlib import Path
from subprocess import run
from unittest.mock import Mock

from unittest_expander import foreach, expand

from py2many.cli import main, _get_all_settings

KEEP_GENERATED = os.environ.get("KEEP_GENERATED", False)
UPDATE_EXPECTED = os.environ.get("UPDATE_EXPECTED", False)
COMPILERS = {
    # cpp is disabled due to https://github.com/adsharma/py2many/issues/24
    # "cpp": ["clang", "-std=c++14"],
    "dart": ["dart"],
    "go": ["go", "tool", "compile"],
    "julia": ["julia"],
    "kotlin": ["kotlinc"],
    "nim": ["nim", "compile", "--nimcache:."],
    "rust": ["cargo", "script", "--build-only", "--debug"],
}
INVOKER = {
    "rust": ["cargo", "script", "{case_output}"],
    "kotlin": ["kotlin", "{class_name}"],
}
EXPECTED_COMPILE_FAILURES = [
    "binit.go",  # https://github.com/adsharma/py2many/issues/23
    "binit.kt",  # https://github.com/adsharma/py2many/issues/28
    "binit.nim",  # https://github.com/adsharma/py2many/issues/19
    "binit.rs",  # https://github.com/adsharma/py2many/issues/19
    "infer.go",  # https://github.com/adsharma/py2many/issues/23
    "infer.kt",  # https://github.com/adsharma/py2many/issues/28
    "infer_ops.go",  # https://github.com/adsharma/py2many/issues/16
    "infer_ops.kt",  # https://github.com/adsharma/py2many/issues/28
    "infer_ops.nim",  # https://github.com/adsharma/py2many/issues/16
    "infer_ops.rs",  # https://github.com/adsharma/py2many/issues/16
    "int_enum.jl",  # https://github.com/adsharma/py2many/issues/26
    "int_enum.kt",  # https://github.com/adsharma/py2many/issues/28
    "lambda.dart",  # https://github.com/adsharma/py2many/issues/34
    "lambda.go",  # https://github.com/adsharma/py2many/issues/15
    "lambda.kt",  # https://github.com/adsharma/py2many/issues/28
    "lambda.nim",  # https://github.com/adsharma/py2many/issues/27
    "lambda.rs",  # https://github.com/adsharma/py2many/issues/15
    "str_enum.jl",  # https://github.com/adsharma/py2many/issues/26
]


def has_main(filename):
    with open(filename) as f:
        lines = f.readlines()
    return bool([line in line for line in lines if "def main" in line or "__main__" in line])


@expand
class CodeGeneratorTests(unittest.TestCase):
    TESTS_DIR = Path(__file__).parent
    TEST_CASES = [
        item.stem
        for item in (TESTS_DIR / "cases").glob("*.py")
        if not item.stem.startswith("test_")
    ]
    SETTINGS = _get_all_settings(Mock(indent=4))
    maxDiff = None

    def setUp(self):
        os.chdir(self.TESTS_DIR)

    @foreach(SETTINGS.keys())
    @foreach(TEST_CASES)
    def test_cli(self, case, lang):
        settings = self.SETTINGS[lang]
        ext = settings.ext
        if (
            not UPDATE_EXPECTED
            and not KEEP_GENERATED
            and not os.path.exists(f"expected/{case}{ext}")
        ):
            raise unittest.SkipTest(f"expected/{case}{ext} not found")
        if settings.formatter:
            if not spawn.find_executable(settings.formatter[0]):
                raise unittest.SkipTest(f"{settings.formatter[0]} not available")

        exe = self.TESTS_DIR / "cases" / f"{case}"
        if ext == ".kt":
            class_name = str(case.title()) + "Kt"
            compiled = self.TESTS_DIR / (class_name + ".class")
        else:
            class_name = None
            compiled = exe
        print(f"exe={exe}; compiled={compiled}")
        compiled.unlink(missing_ok=True)

        case_filename = self.TESTS_DIR / "cases" / f"{case}.py"
        case_output = self.TESTS_DIR / "cases" / f"{case}{ext}"
        is_script = has_main(case_filename)
        print(f"is_script: {is_script}")
        sys.argv = ["test", f"--{lang}=1", str(case_filename)]

        try:
            main()
            with open(f"cases/{case}{ext}") as actual:
                generated = actual.read()
                if os.path.exists(f"expected/{case}{ext}") and not UPDATE_EXPECTED:
                    with open(f"expected/{case}{ext}") as f2:
                        self.assertEqual(f2.read(), generated)

            if ext == ".dart" and not is_script:
                # See https://github.com/adsharma/py2many/issues/25
                raise unittest.SkipTest(f"{case}{ext} doesnt have a main")

            expect_failure = f"{case}{ext}" in EXPECTED_COMPILE_FAILURES
            compiler = COMPILERS.get(lang)
            if ext == ".rs" and not is_script:
                compiler = ["rust-script"]
            if compiler and spawn.find_executable(compiler[0]):
                proc = run([*compiler, f"cases/{case}{ext}"], check=not expect_failure)

                assert not expect_failure or proc.returncode != 0
                if proc.returncode:
                    raise unittest.SkipTest(f"{case}{ext} doesnt compile")

                if UPDATE_EXPECTED or not os.path.exists(f"expected/{case}{ext}"):
                    with open(f"expected/{case}{ext}", "w") as f:
                        f.write(generated)
                if exe.exists():
                    run([exe], check=True)
                elif ext in [".rs", ".kt"] and not is_script:
                    pass
                elif INVOKER.get(lang):
                    invoker = INVOKER.get(lang)
                    invoker = [item.format(exe=exe, case_output=case_output, compiled=compiled, class_name=class_name) for item in invoker]
                    print('running', invoker)
                    run([*invoker], check=True)
        finally:
            try:
                if not KEEP_GENERATED:
                    os.unlink(f"cases/{case}{ext}")
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    unittest.main()
