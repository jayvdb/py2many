import os.path
import unittest

from pathlib import Path
from shutil import which
from unittest.mock import Mock

from py2many.cli import _get_all_settings, _process_dir

SHOW_ERRORS = os.environ.get("SHOW_ERRORS", False)

TESTS_DIR = Path(__file__).parent
ROOT_DIR = TESTS_DIR.parent
OUT_DIR = TESTS_DIR / "output"
PY2MANY_MODULE = ROOT_DIR / "py2many"


class SelfTranspileTests(unittest.TestCase):
    SETTINGS = _get_all_settings(Mock(indent=4))

    def test_rust_recursive(self):
        settings = self.SETTINGS["rust"]

        transpiler_module = ROOT_DIR / "pyrs"
        successful, format_errors, failures = _process_dir(
            settings, transpiler_module, OUT_DIR, _suppress_exceptions=False
        )
        assert len(successful) == 2  # The two __init__.py

        successful, format_errors, failures = _process_dir(
            settings,
            PY2MANY_MODULE,
            OUT_DIR,
            _suppress_exceptions=False,
        )
        assert len(successful) == 4  # Four files transpile ok

    def test_dart_recursive(self):
        settings = self.SETTINGS["dart"]

        transpiler_module = ROOT_DIR / "pydart"
        successful, format_errors, failures = _process_dir(
            settings, transpiler_module, OUT_DIR, _suppress_exceptions=False
        )
        assert len(successful) == 4

        successful, format_errors, failures = _process_dir(
            settings,
            PY2MANY_MODULE,
            OUT_DIR,
            _suppress_exceptions=False,
        )
        assert len(successful) == 14

    def test_kotlin_recursive(self):
        settings = self.SETTINGS["kotlin"]

        formatter_available = which(settings.formatter[0])

        transpiler_module = ROOT_DIR / "pykt"
        successful, format_errors, failures = _process_dir(
            settings,
            transpiler_module,
            OUT_DIR,
            _suppress_exceptions=False,
        )
        if formatter_available:
            assert len(successful) == 1  # The __init__.py

        successful, format_errors, failures = _process_dir(
            settings,
            PY2MANY_MODULE,
            OUT_DIR,
            _suppress_exceptions=False,
        )
        if not formatter_available:
            raise unittest.SkipTest(f"{settings.formatter[0]} not available")

        assert len(successful) == 3

    def test_go_recursive(self):
        settings = self.SETTINGS["go"]

        transpiler_module = ROOT_DIR / "pygo"
        successful, format_errors, failures = _process_dir(
            settings,
            transpiler_module,
            OUT_DIR,
            _suppress_exceptions=NotImplementedError,
        )
        assert len(successful) == 1  # The __init__.py

        successful, format_errors, failures = _process_dir(
            settings,
            PY2MANY_MODULE,
            OUT_DIR,
            _suppress_exceptions=(NotImplementedError, IndexError),
        )
        assert len(successful) == 1  # The __init__.py

    def test_nim_recursive(self):
        settings = self.SETTINGS["nim"]

        transpiler_module = ROOT_DIR / "pynim"
        successful, format_errors, failures = _process_dir(
            settings,
            transpiler_module,
            OUT_DIR,
            _suppress_exceptions=AttributeError,
        )
        assert len(successful) == 1  # The __init__.py

        successful, format_errors, failures = _process_dir(
            settings,
            PY2MANY_MODULE,
            OUT_DIR,
            _suppress_exceptions=AttributeError,
        )
        assert len(successful) == 2

    def test_cpp_recursive(self):
        settings = self.SETTINGS["cpp"]

        transpiler_module = ROOT_DIR / "pycpp"
        successful, format_errors, failures = _process_dir(
            settings,
            transpiler_module,
            OUT_DIR,
            _suppress_exceptions=NotImplementedError,
        )
        assert len(successful) == 9  # The __init__.py

        successful, format_errors, failures = _process_dir(
            settings,
            PY2MANY_MODULE,
            OUT_DIR,
            _suppress_exceptions=(
                AttributeError,
                NotImplementedError,
                TypeError,
            ),
        )
        assert len(successful) == 5

    def test_julia_recursive(self):
        settings = self.SETTINGS["julia"]

        suppress_exceptions = (NotImplementedError,)
        formatter_available = which(settings.formatter[0])

        transpiler_module = ROOT_DIR / "pyjl"
        successful, format_errors, failures = _process_dir(
            settings,
            transpiler_module,
            OUT_DIR,
            _suppress_exceptions=suppress_exceptions,
        )
        if formatter_available:
            assert len(successful) == 1  # The __init__.py

        suppress_exceptions = suppress_exceptions + (ValueError, KeyError)
        successful, format_errors, failures = _process_dir(
            settings,
            PY2MANY_MODULE,
            OUT_DIR,
            _suppress_exceptions=suppress_exceptions,
        )
        if not formatter_available:
            raise unittest.SkipTest(f"{settings.formatter[0]} not available")

        assert len(successful) == 4
