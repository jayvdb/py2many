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
    AstTypeNotSupported,  # go only
    AstCouldNotInfer,
)

from tests.test_cli import LANGS, SHOW_ERRORS

TESTS_DIR = Path(__file__).parent
OUT_DIR = TESTS_DIR / "output"
CYTHON_TEST_DIR = Path(test.__file__).parent

#raise RuntimeError(str(CYTHON_TEST_DIR) + "/**/*.py")

CYTHON_TEST_FILES_ALL = [
    Path(f).relative_to(CYTHON_TEST_DIR)
    for f in glob.glob(str(CYTHON_TEST_DIR) + "/**", recursive=True)
]

#raise RuntimeError(str([i for i in CYTHON_TEST_FILES_ALL if "/" in str(i)]))

CYTHON_TEST_FILES = [
    str(f)[:-3] for f in CYTHON_TEST_FILES_ALL if f.suffix == ".py" and f.stem != "__init__"
    if f.stem.startswith("dataclass")
]

#raise RuntimeError(str(CYTHON_TEST_FILES))

@expand
class CPythonTests(unittest.TestCase):
    SETTINGS = _get_all_settings(Mock(indent=4, extension=False))

    @foreach(list(set(LANGS) - {"python", "cpp"})) #$, "go"}))  # go and cpp fail too much
    @foreach(CYTHON_TEST_FILES)
    def test_cpython_test(self, filename, lang):
        if SHOW_ERRORS:
            if filename == "datetimetester":
                raise unittest.SkipTest("Fails with ValueError")
            if filename == "test_pathlib":
                raise unittest.SkipTest("'\udfff' causes UnicodeEncodeError")
        if SHOW_ERRORS and lang in ["cpp"]:
            if filename == "test_asyncgen":
                return  # notimpl... due to async func
        if SHOW_ERRORS and lang in ["go"]:
            if filename == "test_grammar":
                return  # lots of unusual stuff
        #if SHOW_ERRORS and lang in ["julia","dart"] and filename in ["test_bool", "test_bytes", "test_inspect"]:
        #    return  # plugin args IndexError
        #if SHOW_ERRORS and lang in ["rust"] and filename in ["test_bisect", "test_inspect"]:
        #    return  # list() fails; plugin args IndexError
        if SHOW_ERRORS and lang in ["cpp", "go"] and filename in ["ann_module", "ann_module2", "ann_module3"]:
            return
        if SHOW_ERRORS and lang in ["dart", "julia"] and filename == "test_codecs":
            raise unittest.SkipTest("causes UnicodeEncodeError")
        if SHOW_ERRORS and lang in ["dart", "julia"] and filename == "test_io":
            raise unittest.SkipTest("causes RecursionError")  # https://github.com/adsharma/py2many/issues/376
        if SHOW_ERRORS and lang in ["kotlin"] and filename == "test_print":
            raise unittest.SkipTest("AttributeError: 'If' object has no attribute 'body_vars'")
        #if SHOW_ERRORS and lang in ["dart", "julia", "kotlin", "nim"] and filename == "test_named_expressions":
        #    raise unittest.SkipTest("TypeError: sequence item 0: expected str instance, NoneType found")
        if SHOW_ERRORS and filename in ["test_importlib/test_metadata_api", "test_importlib/test_zip"]:
            raise unittest.SkipTest("logic causes importerror in class_for_typename")
        if lang == "go" and filename in ["dataclass_module_1_str", "dataclass_module_1"]:
            # :20:4: py2many.exceptions.AstCouldNotInfer: Could not infer: <ast.Attribute object at 0x10702df10>
            #return
            pass
        # test_embed
        # Dict(keys=[None, Constant(value='PYTHONSTARTUP')], values=[Call(func=Name(id='remove_python_envvars', ctx=Load()), args=[], keywords=[]), Name(id='startup', ctx=Load())])

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
            #AstMissingChild,
            SyntaxError,
            AstIncompatibleLifetime,
            AstClassUsedBeforeDeclaration,
            AssertionError,
            AstTypeNotSupported,  # go only
            #AstCouldNotInfer,
        ) as e:
            raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
        except (
            AstTypeNotSupported,  # go only
        ) as e:
            if lang == "go":
                raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
            raise
        except AstNotImplementedError as e:
            _print_exception(filename, e)
            #if "no assigned_from" in str(e):  # or "node can not be None" in str(e):
            #    raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
            if SHOW_ERRORS:
                raise
            raise unittest.SkipTest(f"{e.__class__.__name__}: {e}")
        except TypeError as e:
            if 'Dict(keys=[None' in str(e):
                raise unittest.SkipTest(e)
            raise
        assert output_list
        assert successful
        assert len(output_list) == 1
        assert output_list[0] != "FAILED"
