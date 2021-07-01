import pathlib
from subprocess import run

from .clike import CLikeTranspiler
from .transpile import transpile_one


class HaxeTranspiler(CLikeTranspiler):
    NAME = "haxe"
    _target_extension = ".hx"
    _cmd = ["lix", "run", "go2hx"]

    def __init__(self, intermediate_settings):
        self._intermediate_settings = intermediate_settings
        self._extension = False
        self._temp = 0
        self._main_signature_arg_names = set()

    def _get_generated_filename(self, intermediate_path):
        CWD = pathlib.Path.cwd()
        return CWD / "golibs" / "command_line_arguments" / (str.title(intermediate_path.stem) + self._target_extension)

    def visit(self, tree):
        intermediate_path = tree.__file__.with_suffix(self._intermediate_settings.ext)
        print(intermediate_path)
        print(self._intermediate_settings)
        intermediate_source = transpile_one(
            [tree],
            tree,
            self._intermediate_settings.transpiler,
            self._intermediate_settings,
        )
        with open(intermediate_path, "w") as f:
            f.write(intermediate_source)
        assert "?" not in intermediate_source, "? found"
        generated_file = self._get_generated_filename(intermediate_path)
        # Use _create_cmd
        cmd = [*self._cmd, str(intermediate_path)]
        print(cmd)
        proc = run(cmd)
        if proc.returncode:
            print(proc.stdout)
            print(proc.stderr)
            raise NotImplementedError(f"{self._cmd[0]} exit {proc.returncode}")
        with open(generated_file) as f:
            lines = f.readlines()
            assert lines
            return "\n".join(line.rstrip() for line in lines)
