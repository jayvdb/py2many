import ast

from .ast_helpers import get_id


class _InternalErrorBase(Exception):
    """Errors occurring when a node with lineno is not available"""


class TypeNotSupported(_InternalErrorBase):
    def __init__(self, typename):
        super().__init__(f"{typename} not supported")

class AstErrorBase:
    def __init__(self, msg: str, node: ast.AST):
        self.lineno = node.lineno
        self.col_offset = node.col_offset
        super().__init__(msg)  # noqa: other mechanisms of subclassing Exception


class AstNotImplementedError(AstErrorBase, NotImplementedError):
    """Node is not supported by the transpiler"""


class AstUnrecognisedBinOp(AstNotImplementedError):
    """BinOp using unrecognised combination"""

    def __init__(self, left_id: str, right_id: str, node: ast.AST):
        self.lineno = node.lineno
        self.col_offset = node.col_offset
        super().__init__(f"{left_id} {type(node.op)} {right_id}", node)


class AstClassUsedBeforeDeclaration(AstNotImplementedError):
    """Class usage found before prior to its declaration"""
    def __init__(self, fndef, node: ast.AST):
        super().__init__(f"Declaration of {get_id(fndef)} not yet parsed", node)

    def __init__(self, fndef, node: ast.AST):
        super().__init__(f"Declaration of {get_id(fndef)} not yet parsed", node)


class AstCouldNotInfer(AstNotImplementedError):
    """Unable to infer type"""

    def __init__(self, type_node, node: ast.AST):
        super().__init__(f"Could not infer: {type_node}", node)


class AstTypeNotSupported(AstNotImplementedError):
    """Unable to infer type"""
    def __init__(self, msg, node: ast.AST):
        super().__init__(msg, node)

class AstIncompatibleAssign(AstErrorBase, TypeError):
    """Assignment target has type annotation that is incompatible with expression"""


class IncompatibleLifetime(_InternalErrorBase, AssertionError):
    """Type is not supported in this context due to incompatible lifetime"""


class AstIncompatibleLifetime(AstNotImplementedError, IncompatibleLifetime):
    """Type is not supported in this context due to incompatible lifetime"""


class AstMissingChild(AstNotImplementedError):
    """Node contains missing child"""

    def __init__(self, node: ast.AST):
        self.lineno = node.lineno
        self.col_offset = node.col_offset
        super().__init__(f"{get_id(node) or 'function'} has an empty child", node)


class AstEmptyNodeFound(_InternalErrorBase, TypeError):
    def __init__(self, msg=None):
        super().__init__(msg)
