import argparse
import ast
import functools
import os
import pathlib
import sys

from dataclasses import dataclass, field
from distutils import spawn
from functools import lru_cache
from subprocess import run
from typing import Callable, List, Optional

from .analysis import add_imports
from .clike import CLikeTranspiler
from .scope import add_scope_context
from .annotation_transformer import add_annotation_flags
from .mutability_transformer import detect_mutable_vars
from .nesting_transformer import detect_nesting_levels
from .context import add_variable_context, add_list_calls
from .inference import infer_types

from pycpp.transpiler import CppTranspiler, CppListComparisonRewriter
from pyrs.inference import infer_rust_types
from pyrs.transpiler import (
    RustTranspiler,
    RustLoopIndexRewriter,
    RustNoneCompareRewriter,
    RustStringJoinRewriter,
)
from pyjl.transpiler import JuliaTranspiler, JuliaMethodCallRewriter
from pykt.inference import infer_kotlin_types
from pykt.transpiler import KotlinTranspiler, KotlinPrintRewriter, KotlinBitOpRewriter
from pynim.inference import infer_nim_types
from pynim.transpiler import NimTranspiler, NimNoneCompareRewriter
from pydart.transpiler import DartTranspiler, DartIntegerDivRewriter
from pygo.inference import infer_go_types
from pygo.transpiler import (
    GoTranspiler,
    GoMethodCallRewriter,
    GoNoneCompareRewriter,
    GoPropagateTypeAnnotation,
    GoVisibilityRewriter,
    GoIfExpRewriter,
)

from py2many.rewriters import (
    ComplexDestructuringRewriter,
    FStringJoinRewriter,
    PythonMainRewriter,
    DocStringToCommentRewriter,
    PrintBoolRewriter,
    StrStrRewriter,
    WithToBlockTransformer,
)

PY2MANY_DIR = pathlib.Path(__file__).parent
ROOT_DIR = PY2MANY_DIR.parent


def core_transformers(tree):
    add_variable_context(tree)
    add_scope_context(tree)
    add_list_calls(tree)
    detect_mutable_vars(tree)
    detect_nesting_levels(tree)
    add_annotation_flags(tree)
    infer_meta = infer_types(tree)
    add_imports(tree)
    return tree, infer_meta


def transpile(
    filename,
    source,
    transpiler,
    rewriters,
    transformers,
    post_rewriters,
    temp_counter_start=0,
):
    """
    Transpile a single python translation unit (a python script) into
    Rust code.
    """
    if isinstance(source, ast.Module):
        tree = source
    else:
        tree = ast.parse(source)
    tree.__file__ = filename
    language = transpiler.NAME
    generic_rewriters = [
        ComplexDestructuringRewriter(language),
        PythonMainRewriter(language),
        FStringJoinRewriter(language),
        DocStringToCommentRewriter(language),
        WithToBlockTransformer(language),
    ]
    # This is very basic and needs to be run before and after
    # rewrites. Revisit if running it twice becomes a perf issue
    add_scope_context(tree)
    # First run Language independent rewriters
    running_temp_var = temp_counter_start
    for rewriter in generic_rewriters:
        setattr(rewriter, "_temp", running_temp_var)
        tree = rewriter.visit(tree)
        running_temp_var = getattr(rewriter, "_temp")
    # Language specific rewriters
    for rewriter in rewriters:
        setattr(rewriter, "_temp", running_temp_var)
        tree = rewriter.visit(tree)
        running_temp_var = getattr(rewriter, "_temp")
    # Language independent core transformers
    tree, infer_meta = core_transformers(tree)
    # Language specific transformers
    for rewriter in transformers:
        setattr(rewriter, "_temp", running_temp_var)
        rewriter(tree)
        running_temp_var = getattr(rewriter, "_temp")
    # Language independent rewriters that run after type inference
    generic_post_rewriters = [PrintBoolRewriter(language), StrStrRewriter(language)]
    for rewriter in generic_post_rewriters:
        setattr(rewriter, "_temp", running_temp_var)
        tree = rewriter.visit(tree)
        running_temp_var = getattr(rewriter, "_temp")
    # Language specific rewriters that depend on previous steps
    for rewriter in post_rewriters:
        setattr(rewriter, "_temp", running_temp_var)
        tree = rewriter.visit(tree)
        running_temp_var = getattr(rewriter, "_temp")
    # Rerun core transformers
    tree, infer_meta = core_transformers(tree)
    out = []
    setattr(transpiler, "_temp", running_temp_var)
    code = transpiler.visit(tree) + "\n"
    headers = transpiler.headers(infer_meta)
    features = transpiler.features()
    if features:
        out.append(features)
    if headers:
        out.append(headers)
    usings = transpiler.usings()
    if usings:
        out.append(usings)
    out.append(code)
    if transpiler.extension:
        out.append(transpiler.extension_module(tree))
    return "\n".join(out)


@lru_cache(maxsize=100)
def process_once_data(source_data, filename, settings, temp_counter_start=0):
    return transpile(
        filename,
        source_data,
        settings.transpiler,
        settings.rewriters,
        settings.transformers,
        settings.post_rewriters,
        temp_counter_start=temp_counter_start,
    )


def _create_cmd(parts, filename, **kw):
    cmd = [arg.format(filename=filename, **kw) for arg in parts]
    if cmd != parts:
        return cmd
    return [*parts, str(filename)]


@dataclass
class LanguageSettings:
    transpiler: CLikeTranspiler
    ext: str
    display_name: str
    formatter: Optional[List[str]] = None
    indent: Optional[int] = None
    rewriters: List[ast.NodeVisitor] = field(default_factory=list)
    transformers: List[Callable] = field(default_factory=list)
    post_rewriters: List[ast.NodeVisitor] = field(default_factory=list)
    linter: Optional[List[str]] = None

    def __hash__(self):
        f = tuple(self.formatter) if self.formatter is not None else ()
        l = tuple(self.linter) if self.linter is not None else ()
        return hash((self.transpiler, f, l))


def cpp_settings(args, env=os.environ):
    clang_format_style = env.get("CLANG_FORMAT_STYLE")
    cxx = env.get("CXX")
    default_cxx = ["clang++", "g++-11", "g++"]
    if cxx:
        if not spawn.find_executable(cxx):
            print(f"Warning: CXX({cxx}) not found")
            cxx = None
    if not cxx:
        for exe in default_cxx:
            if spawn.find_executable(exe):
                cxx = exe
                break
        else:
            cxx = default_cxx[0]
    cxx_flags = env.get("CXXFLAGS")
    if cxx_flags:
        cxx_flags = cxx_flags.split()
    else:
        cxx_flags = ["-std=c++14", "-Wall", "-Werror"]
    cxx_flags = ["-I", str(ROOT_DIR)] + cxx_flags
    if cxx.startswith("clang++") and not sys.platform == "win32":
        cxx_flags += ["-stdlib=libc++"]

    if clang_format_style:
        clang_format_cmd = ["clang-format", f"-style={clang_format_style}", "-i"]
    else:
        clang_format_cmd = ["clang-format", "-i"]

    return LanguageSettings(
        CppTranspiler(args.extension, args.no_prologue),
        ".cpp",
        "C++",
        clang_format_cmd,
        None,
        [CppListComparisonRewriter()],
        linter=[cxx, *cxx_flags],
    )


def rust_settings(args, env=os.environ):
    return LanguageSettings(
        RustTranspiler(args.extension, args.no_prologue),
        ".rs",
        "Rust",
        ["rustfmt", "--edition=2018"],
        None,
        [RustNoneCompareRewriter()],
        [functools.partial(infer_rust_types, extension=args.extension)],
        [RustLoopIndexRewriter(), RustStringJoinRewriter()],
    )


def julia_settings(args, env=os.environ):
    format_jl = spawn.find_executable("format.jl")
    if format_jl:
        format_jl = ["julia", "-O0", "--compile=min", "--startup=no", format_jl, "-v"]
    else:
        format_jl = ["format.jl", "-v"]
    return LanguageSettings(
        JuliaTranspiler(),
        ".jl",
        "Julia",
        format_jl,
        None,
        [],
        [],
        [JuliaMethodCallRewriter()],
    )


def kotlin_settings(args, env=os.environ):
    return LanguageSettings(
        KotlinTranspiler(),
        ".kt",
        "Kotlin",
        ["ktlint", "-F"],
        rewriters=[KotlinBitOpRewriter()],
        transformers=[infer_kotlin_types],
        post_rewriters=[KotlinPrintRewriter()],
        linter=["ktlint"],
    )


def nim_settings(args, env=os.environ):
    nim_args = {}
    nimpretty_args = []
    if args.indent is not None:
        nim_args["indent"] = args.indent
        nimpretty_args.append(f"--indent:{args.indent}")
    return LanguageSettings(
        NimTranspiler(**nim_args),
        ".nim",
        "Nim",
        ["nimpretty", *nimpretty_args],
        None,
        [NimNoneCompareRewriter()],
        [infer_nim_types],
    )


def dart_settings(args, env=os.environ):
    return LanguageSettings(
        DartTranspiler(),
        ".dart",
        "Dart",
        ["dart", "format"],
        post_rewriters=[DartIntegerDivRewriter()],
    )


class JavascriptTranspiler(CLikeTranspiler):
    NAME = "JavaScript"
    BASE = DartTranspiler

    def __init__(self, settings):
        self.settings = settings
        self._extension = False
        self._temp = 0

    def visit(self, tree):
        intermediate_path = tree.__file__.with_suffix(".dart")
        intermediate_source = process_once_data(
            tree,
            tree.__file__,
            self.settings,
            temp_counter_start=self._temp,
        )
        with open(intermediate_path, "w") as f:
            f.write(intermediate_source)
        js_file = intermediate_path.with_suffix(".js")
        proc = run(["dart2js", str(intermediate_path), "-o", str(js_file)])
        if proc.returncode:
            print(proc.stdout)
            print(proc.stderr)
            raise NotImplementedError(f"dart2js exit {proc.returncode}")
        with open(js_file) as f:
            generated_by = f.readline()
            if not generated_by:
                raise NotImplementedError("dart2js did not generate output")
            version_start = generated_by.find(" version")
            assert version_start != -1
            generated_by = generated_by[:version_start] + "\n"
            lines = f.readlines()
            assert lines
            result = "\n".join(line.rstrip() for line in lines)
            return generated_by + result


def javascript_settings(args, env=os.environ):
    return LanguageSettings(
        JavascriptTranspiler(dart_settings(args, env=env)),
        ".js",
        "JavaScript",
    )


def go_settings(args, env=os.environ):
    return LanguageSettings(
        GoTranspiler(),
        ".go",
        "Go",
        ["gofmt", "-w"],
        None,
        [GoNoneCompareRewriter(), GoVisibilityRewriter(), GoIfExpRewriter()],
        [infer_go_types],
        [GoMethodCallRewriter(), GoPropagateTypeAnnotation()],
        linter=["golint", "-set_exit_status", "-min_confidence", "1.0"],
    )


def _get_all_settings(args, env=os.environ):
    return {
        "cpp": cpp_settings(args, env=env),
        "rust": rust_settings(args, env=env),
        "julia": julia_settings(args, env=env),
        "kotlin": kotlin_settings(args, env=env),
        "nim": nim_settings(args, env=env),
        "dart": dart_settings(args, env=env),
        "go": go_settings(args, env=env),
        "javascript": javascript_settings(args, env=env),
    }


def _process_once(settings, filename, outdir, env=None):
    """Transpile and reformat.

    Returns False if reformatter failed.
    """
    output_path = outdir / (filename.stem + settings.ext)
    if settings.ext == ".kt" and output_path.is_absolute():
        # KtLint does not support absolute path in globs
        output_path = output_path.relative_to(pathlib.Path.cwd())
    print(f"{filename}...{output_path}")
    with open(filename) as f:
        source_data = f.read()
    new_source = process_once_data(source_data, filename, settings)
    with open(output_path, "w") as f:
        f.write(new_source)

    if settings.formatter:
        cmd = _create_cmd(settings.formatter, filename=output_path)
        proc = run(cmd, env=env)
        if proc.returncode:
            # format.jl exit code is unreliable
            if settings.ext == ".jl":
                if proc.stderr is not None:
                    print(
                        f"Error: {cmd} (code: {proc.returncode}):\n{proc.stderr}{proc.stdout}"
                    )
                return True
            print(
                f"Error: {cmd} (code: {proc.returncode}):\n{proc.stderr}{proc.stdout}"
            )
            return False
        if settings.ext == ".kt":
            # ktlint formatter needs to be invoked twice before output is lint free
            if run(cmd, env=env).returncode:
                print(f"Error: Could not reformat: {cmd}")
                return False
    return True


def _process_dir(settings, source, outdir, env=None, _suppress_exceptions=True):
    print(f"Transpiling whole directory to {outdir}:")
    successful = []
    failures = []
    format_errors = []
    for path in source.rglob("*.py"):
        if path.suffix != ".py":
            continue
        if path.parent.name == "__pycache__":
            continue

        relative_path = path.relative_to(source)
        target_path = outdir / relative_path
        target_dir = target_path.parent
        os.makedirs(target_dir, exist_ok=True)

        try:
            if _process_once(settings, path, target_dir, env=env):
                successful.append(path)
            else:
                print(f"Error: Could not reformat: {path}")
                format_errors.append(path)
        except Exception as e:
            print(f"Error: Could not transpile: {path}")
            print(f"Due to: {e}")
            failures.append(path)
            if _suppress_exceptions:
                if _suppress_exceptions is not True:
                    if not isinstance(e, _suppress_exceptions):
                        raise e
            else:
                raise e

    print("\nFinished!")
    print(f"Successful: {len(successful)}")
    if format_errors:
        print(f"Failed to reformat: {len(format_errors)}")
    print(f"Failed to convert: {len(failures)}")
    print()
    return (successful, format_errors, failures)


from unittest.mock import Mock


def main(args=None, env=os.environ):
    parser = argparse.ArgumentParser()
    LANGS = _get_all_settings(Mock(indent=4))
    for lang, settings in LANGS.items():
        parser.add_argument(
            f"--{lang}",
            type=bool,
            default=False,
            help=f"Generate {settings.display_name} code",
        )
    parser.add_argument("--outdir", default=None, help="Output directory")
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=None,
        help="Indentation to use in languages that care",
    )
    parser.add_argument(
        "--extension", type=bool, default=False, help="Build a python extension"
    )
    parser.add_argument("--no-prologue", type=bool, default=False, help="")
    args, rest = parser.parse_known_args(args=args)

    # Validation of the args
    if args.extension and not args.rust:
        print("extension supported only with rust via pyo3")
        return -1

    for filename in rest:
        settings = cpp_settings(args, env=env)
        if args.cpp:
            pass
        if args.rust:
            settings = rust_settings(args, env=env)
        elif args.julia:
            settings = julia_settings(args, env=env)
        elif args.kotlin:
            settings = kotlin_settings(args, env=env)
        elif args.nim:
            settings = nim_settings(args, env=env)
        elif args.dart:
            settings = dart_settings(args, env=env)
        elif args.go:
            settings = go_settings(args, env=env)
        elif args.javascript:
            settings = javascript_settings(args, env=env)
        source = pathlib.Path(filename)
        if args.outdir is None:
            outdir = source.parent
        else:
            outdir = pathlib.Path(args.outdir)

        if source.is_file():
            print(f"Writing to: {outdir}")
            rv = _process_once(settings, source, outdir, env=env)
        else:
            if args.outdir is None:
                outdir = source.parent / f"{source.name}-py2many"

            successful, format_errors, failures = _process_dir(
                settings, source, outdir, env=env
            )
            rv = not (failures or format_errors)
        rv = 0 if rv is True else 1
        return rv
