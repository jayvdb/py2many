import ast

from .analysis import get_id
from .ast_helpers import create_ast_node, create_noop_node, unparse
from .clike import CLikeTranspiler

from py2rb import convert_py2rb

TYPING_IMPORTS = ["ctypes", "typing"]


class DowngradeAnnAssignRewriter(ast.NodeTransformer):

    def visit_Import(self, node):
        names = [self.visit(n) for n in node.names]
        print(names)
        print(names[0].__dict__)
        names = [
            i
            for i in names
            if get_id(i) not in TYPING_IMPORTS
        ]
        if not names:
            return create_noop_node(at_node=node)
        node.names = names
        return node

    def visit_ImportFrom(self, node):
        if node.module in TYPING_IMPORTS:
            return create_noop_node(at_node=node)
        return node

    def visit_AnnAssign(self, node):
        col_offset = getattr(node, "col_offset", None)
        assert node.target
        #assert node.value

        node = ast.Assign(
            targets=[node.target],
            value=node.value or ast.Name(id="None"),
            lineno=node.lineno,
            col_offset=col_offset,
        )
        return node


class RubyTranspiler(CLikeTranspiler):
    NAME = "ruby"

    def visit(self, node):
        source_data = unparse(node)
        print(source_data)
        dir_path = node.__file__.parent

        _, header, data = convert_py2rb(unparse(node), dir_path)
        print(header, data)
        return f"{header}\n{data}"

    def usings(self):
        return ""
