from .clike import CLikeTranspiler
from .transpile import transpile_one

from pygo.transpiler import GoTranspiler


class HaxeTranspiler(CLikeTranspiler):
    NAME = "haxe"
    BASE = GoTranspiler
    _target_extension = ".hx"
    _cmd = ["lix", "run", "go2hx"]

    def __init__(self, intermediate_settings):
        self._intermediate_settings = intermediate_settings
        self._extension = False
        self._temp = 0

    def visit(self, tree):
        intermediate_path = tree.__file__.with_suffix(self._intermediate_settings)
        intermediate_source = transpile_one(
            [tree],
            tree,
            self._intermediate_settings,
        )
        with open(intermediate_path, "w") as f:
            f.write(intermediate_source)
        final_file = intermediate_path.with_suffix(self._target_extension)
        # Use _create_cmd
        proc = run([*self._cmd])
        if proc.returncode:
            print(proc.stdout)
            print(proc.stderr)
            raise NotImplementedError(f"dart2js exit {proc.returncode}")
        with open(final_file) as f:
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
