import argparse
import ast
import os
import pathlib

from functools import lru_cache
from subprocess import run
from typing import List, Set, Tuple

from .exceptions import AstErrorBase
from .language import LanguageSettings
from .registry import _get_all_settings, ALL_SETTINGS, FAKE_ARGS
from .toposort_modules import toposort
from .transpile import transpile_one

CWD = pathlib.Path.cwd()


def _transpile(
    filenames: List[pathlib.Path], sources: List[str], settings: LanguageSettings
):
    """
    Transpile a single python translation unit (a python script) into
    target language
    """
    transpiler = settings.transpiler
    tree_list = []
    for filename, source in zip(filenames, sources):
        tree = ast.parse(source)
        tree.__file__ = filename
        tree_list.append(tree)
    trees = toposort(tree_list)
    topo_filenames = [t.__file__ for t in trees]
    outputs = {}
    successful = []
    for filename, tree in zip(topo_filenames, trees):
        try:
            output = transpile_one(trees, tree, settings.transpiler, settings)
            successful.append(filename)
            outputs[filename] = output
        except Exception as e:
            raise
            import traceback

            formatted_lines = traceback.format_exc().splitlines()
            if isinstance(e, AstErrorBase):
                print(f"{filename}:{e.lineno}:{e.col_offset}: {formatted_lines[-1]}")
            else:
                print(f"{filename}: {formatted_lines[-1]}")
            outputs[filename] = "FAILED"
    # return output in the same order as input
    output_list = [outputs[f] for f in filenames]
    return output_list, successful


@lru_cache(maxsize=100)
def _process_one_data(source_data, filename, settings):
    return _transpile([filename], [source_data], settings,)[
        0
    ][0]


def _create_cmd(parts, filename, **kw):
    cmd = [arg.format(filename=filename, **kw) for arg in parts]
    if cmd != parts:
        return cmd
    return [*parts, str(filename)]


def _relative_to_cwd(absolute_path):
    return pathlib.Path(os.path.relpath(absolute_path, CWD))


def _get_output_path(filename, ext, outdir):
    output_path = outdir / (filename.stem + ext)
    if ext == ".kt" and output_path.is_absolute():
        # KtLint does not support absolute path in globs
        output_path = _relative_to_cwd(output_path)
    return output_path


def _process_one(
    settings: LanguageSettings, filename: pathlib.Path, outdir: str, env=None
):
    """Transpile and reformat.

    Returns False if reformatter failed.
    """
    output_path = _get_output_path(filename, settings.ext, outdir)
    print(f"{filename} ... {output_path}")
    with open(filename) as f:
        source_data = f.read()
    dunder_init = filename.stem == "__init__"
    if dunder_init and not source_data:
        print("Detected empty __init__; skipping")
        return True
    with open(output_path, "w") as f:
        f.write(
            _transpile([filename], [source_data], settings,)[
                0
            ][0]
        )

    if settings.formatter:
        return _format_one(settings, output_path, env)

    return True


def _format_one(settings, output_path, env=None):
    try:
        restore_cwd = False
        if settings.ext == ".kt" and output_path.parts[0] == "..":
            # ktlint can not handle relative paths starting with ..
            restore_cwd = CWD

            os.chdir(output_path.parent)
            output_path = output_path.name
        cmd = _create_cmd(settings.formatter, filename=output_path)
        proc = run(cmd, env=env, capture_output=True)
        if proc.returncode:
            # format.jl exit code is unreliable
            if settings.ext == ".jl":
                if proc.stderr is not None:
                    print(
                        f"{cmd} (code: {proc.returncode}):\n{proc.stderr}{proc.stdout}"
                    )
                    if b"ERROR: " in proc.stderr:
                        return False
                return True
            print(
                f"Error: {cmd} (code: {proc.returncode}):\n{proc.stderr}{proc.stdout}"
            )
            if restore_cwd:
                os.chdir(restore_cwd)
            return False
        if settings.ext == ".kt":
            # ktlint formatter needs to be invoked twice before output is lint free
            if run(cmd, env=env).returncode:
                print(f"Error: Could not reformat: {cmd}")
                if restore_cwd:
                    os.chdir(restore_cwd)
                return False

        if restore_cwd:
            os.chdir(restore_cwd)
    except Exception as e:
        print(f"Error: Could not format: {output_path}")
        print(f"Due to: {e.__class__.__name__} {e}")
        return False

    return True


FileSet = Set[pathlib.Path]


def _process_many(
    settings, basedir, filenames, outdir, env=None
) -> Tuple[FileSet, FileSet]:
    """Transpile and reformat many files."""

    # Try to flush out as many errors as possible
    settings.transpiler.set_continue_on_unimplemented()

    source_data = []
    for filename in filenames:
        with open(basedir / filename) as f:
            source_data.append(f.read())

    outputs, successful = _transpile(
        filenames,
        source_data,
        settings,
    )

    output_paths = [
        _get_output_path(basedir / filename, settings.ext, outdir)
        for filename in filenames
    ]
    for filename, output, output_path in zip(filenames, outputs, output_paths):
        with open(output_path, "w") as f:
            f.write(output)

    successful = set(successful)
    format_errors = set()
    if settings.formatter:
        # TODO: Optimize to a single invocation
        for filename, output_path in zip(filenames, output_paths):
            if filename in successful and not _format_one(settings, output_path, env):
                format_errors.add(pathlib.Path(filename))

    return (successful, format_errors)


def _process_dir(settings, source, outdir, env=None, _suppress_exceptions=True):
    print(f"Transpiling whole directory to {outdir}:")
    successful = []
    failures = []
    input_paths = []
    for path in source.rglob("*.py"):
        if path.suffix != ".py":
            continue
        if path.parent.name == "__pycache__":
            continue

        relative_path = path.relative_to(source)
        target_path = outdir / relative_path
        target_dir = target_path.parent
        os.makedirs(target_dir, exist_ok=True)
        input_paths.append(relative_path)

    successful, format_errors = _process_many(
        settings, source, input_paths, outdir, env=env
    )
    failures = set(input_paths) - set(successful)

    print("\nFinished!")
    print(f"Successful: {len(successful)}")
    if format_errors:
        print(f"Failed to reformat: {len(format_errors)}")
    print(f"Failed to convert: {len(failures)}")
    print()
    return (successful, format_errors, failures)


def main(args=None, env=os.environ):
    parser = argparse.ArgumentParser()
    LANGS = _get_all_settings(FAKE_ARGS)
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

    settings_func = ALL_SETTINGS["cpp"]
    for lang, func in ALL_SETTINGS.items():
        arg = getattr(args, lang)
        if arg:
            print(f"{lang} enabled")
            settings_func = func
            break
    settings = settings_func(args, env=env)

    for filename in rest:
        source = pathlib.Path(filename)
        if args.outdir is None:
            outdir = source.parent
        else:
            outdir = pathlib.Path(args.outdir)

        if source.is_file():
            print(f"Writing to: {outdir}")
            try:
                rv = _process_one(settings, source, outdir, env=env)
            except Exception as e:
                raise
                import traceback

                formatted_lines = traceback.format_exc().splitlines()
                if isinstance(e, AstErrorBase):
                    print(f"{source}:{e.lineno}:{e.col_offset}: {formatted_lines[-1]}")
                else:
                    print(f"{source}: {formatted_lines[-1]}")
                rv = False
        else:
            if args.outdir is None:
                outdir = source.parent / f"{source.name}-py2many"

            successful, format_errors, failures = _process_dir(
                settings, source, outdir, env=env
            )
            rv = not (failures or format_errors)
        rv = 0 if rv is True else 1
        return rv
