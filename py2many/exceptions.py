import ast

from .ast_helpers import get_id


class AstErrorBase:
    def __init__(self, msg: str, node: ast.AST):
        self.lineno = node.lineno
        self.col_offset = node.col_offset
        super().__init__(msg)


class AstNotImplementedError(AstErrorBase, NotImplementedError):
    """Node is not supported by the transpiler"""


class AstUnrecognisedBinOp(AstNotImplementedError):
    """BinOp using unrecognised combination"""

    def __init__(self, left_id: str, right_id: str, node: ast.AST):
        self.lineno = node.lineno
        self.col_offset = node.col_offset
        super().__init__(f"{left_id} {type(node.op)} {right_id}", node)


class AstMissingChild(AstNotImplementedError):
    """Node contains missing child"""

    def __init__(self, node: ast.AST):
        self.lineno = node.lineno
        self.col_offset = node.col_offset
        super().__init__(f"{get_id(node) or 'function'} has an empty child", node)


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
