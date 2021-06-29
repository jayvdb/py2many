import ast

from .ast_helpers import create_ast_node, unparse
from .clike import CLikeTranspiler

from pygo.transpiler import GoTranspiler


class HaxeTranspiler(CLikeTranspiler):
    NAME = "haxe"
    BASE = GoTranspiler

    def __init__(self, settings):
        self.settings = settings
        self._extension = False
        self._temp = 0

    def visit(self, tree):
        intermediate_path = tree.__file__.with_suffix(".go")
        intermediate_source = process_once_data(
            tree,
            tree.__file__,
            self.settings,
            temp_counter_start=self._temp,
        )
        with open(intermediate_path, "w") as f:
            f.write(intermediate_source)
        final_file = intermediate_path.with_suffix(".js")
        proc = run(["go2hx", str(intermediate_path), "-o", str(final_file)])
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

