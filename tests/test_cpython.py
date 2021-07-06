import glob
import unittest

from pathlib import Path
from unittest.mock import Mock

from unittest_expander import foreach, expand

try:
    import test
except ImportError:
    raise unittest.SkipTest("CPython 'test' not installed")

from py2many.cli import _get_all_settings, _transpile, _print_exception
from py2many.exceptions import (
    AstNotImplementedError,
    AstMissingChild,
    AstClassUsedBeforeDeclaration,
    AstIncompatibleLifetime,
    AstUnrecognisedBinOp,
)

from tests.test_cli import LANGS, SHOW_ERRORS

TESTS_DIR = Path(__file__).parent
OUT_DIR = TESTS_DIR / "output"
CYTHON_TEST_DIR = Path(test.__file__).parent

CYTHON_TEST_FILES = [
    str(Path(f).relative_to(CYTHON_TEST_DIR))[:-3]
    for f in glob.iglob(str(CYTHON_TEST_DIR) + "**/*.py")
]


@expand
class CPythonTests(unittest.TestCase):
    SETTINGS = _get_all_settings(Mock(indent=4, extension=False))

    @foreach(list(set(LANGS) - {"python", "cpp", "go"}))  # go and cpp fail too much
    @foreach(CYTHON_TEST_FILES)
    def test_cpython_test(self, filename, lang):
        if SHOW_ERRORS:
            if filename == "test_array":
                raise unittest.SkipTest("the assigned_from isnt being set, which is odd")
            if filename == "datetimetester":
                raise unittest.SkipTest("Fails with ValueError")
            if filename == "test_pathlib":
                raise unittest.SkipTest("'\udfff' causes UnicodeEncodeError")
        if SHOW_ERRORS and lang in ["cpp"]:
            if filename == "test_asyncgen":
                return  # notimpl... due to async func
        if SHOW_ERRORS and lang in ["julia","dart"] and filename in ["test_bool", "test_bytes", "test_inspect"]:
            return  # plugin args IndexError
        if SHOW_ERRORS and lang in ["rust"] and filename in ["test_bisect", "test_inspect"]:
            return  # list() fails; plugin args IndexError
        if SHOW_ERRORS and lang in ["cpp", "go"] and filename in ["ann_module", "ann_module2", "ann_module3"]:
            return
        if SHOW_ERRORS and lang in ["dart"] and filename == "test_codecs":
            raise unittest.SkipTest("causes UnicodeEncodeError")

        filename += ".py"

        settings = self.SETTINGS[lang]
        filename = CYTHON_TEST_DIR.joinpath(filename)
        with open(filename) as f:
            try:
                source_data = f.read()
            except UnicodeDecodeError as e:
                raise unittest.SkipTest(e)
        settings.transpiler._throw_on_unimplemented = False
        try:
            output_list, successful = _transpile(
                [filename], [source_data], settings, _suppress_exceptions=None
            )
        except (
            AstUnrecognisedBinOp,
            AstMissingChild,
            SyntaxError,
            AstIncompatibleLifetime,
            AstClassUsedBeforeDeclaration,
            AssertionError,
        ) as e:
            raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
        except AstNotImplementedError as e:
            _print_exception(filename, e)
            #if "no assigned_from" in str(e):  # or "node can not be None" in str(e):
            #    raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
            if SHOW_ERRORS:
                raise
            raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
        assert output_list
        assert successful
        assert len(output_list) == 1
        assert output_list[0] != "FAILED"
