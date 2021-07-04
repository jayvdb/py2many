import os.path
import glob
import unittest

from pathlib import Path
from unittest.mock import Mock

from unittest_expander import foreach, expand

try:
    import test
except ImportError:
    raise unittest.SkipTest("CPython 'test' not installed")

from py2many.cli import _get_all_settings, _transpile
from py2many.exceptions import AstNotImplementedError

SHOW_ERRORS = os.environ.get("SHOW_ERRORS", False)

TESTS_DIR = Path(__file__).parent
ROOT_DIR = TESTS_DIR.parent
OUT_DIR = TESTS_DIR / "output"
CYTHON_TEST_DIR = Path(test.__file__).parent
dunder_init_dot_py = "__init__.py"

CYTHON_TEST_FILES = [
    str(Path(f).relative_to(CYTHON_TEST_DIR))[:-3]
    for f in glob.iglob(str(CYTHON_TEST_DIR) + "**/*.py")
]


@expand
class CPythonTests(unittest.TestCase):
    SETTINGS = _get_all_settings(Mock(indent=4, extension=False))

    @foreach(CYTHON_TEST_FILES)
    def test_cpython_test(self, filename):

        settings = self.SETTINGS["python"]
        filename += ".py"
        filename = CYTHON_TEST_DIR.joinpath(filename)
        with open(filename) as f:
            try:
                source_data = f.read()
            except UnicodeDecodeError as e:
                raise unittest.SkipTest(e)
        try:
            output_list, successful = _transpile(
                [filename], [source_data], settings, _suppress_exceptions=None
            )
        except (AstNotImplementedError, SyntaxError) as e:
            raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
        assert output_list
        assert successful
        assert len(output_list) == 1
        assert output_list[0] != "FAILED"
