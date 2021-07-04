import ast

from .ast_helpers import get_id


class AstErrorBase:
    def __init__(self, msg: str, node: ast.AST):
        self.lineno = node.lineno
        self.col_offset = node.col_offset
        super().__init__(msg)


class AstNotImplementedError(AstErrorBase, NotImplementedError):
    """Node is not supported by the transpiler"""


class AstIncompatibleAssign(AstErrorBase, TypeError):
    """Assignment target has type annotation that is incompatible with expression"""


class AstEmptyNodeFound(TypeError):
    def __init__(self):
        super().__init__("node can not be None")


def print_exception(filename, e):
    import traceback

    formatted_lines = traceback.format_exc().splitlines()
    if isinstance(e, AstErrorBase):
        print(f"{filename}:{e.lineno}:{e.col_offset}: {formatted_lines[-1]}")
    else:
        print(f"{filename}: {formatted_lines[-1]}")
