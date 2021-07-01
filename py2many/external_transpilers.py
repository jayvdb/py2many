import ast

from .ast_helpers import create_ast_node, unparse
from .clike import CLikeTranspiler

from py2rb import convert_py2rb


class RubyTranspiler(CLikeTranspiler):
    NAME = "ruby"

    def visit(self, node):
        dir_path = node.__file__.parent

        _, header, data = convert_py2rb(unparse(node), dir_path)
        print(header, data)
        return f"{header}\n{data}"

    def usings(self):
        return ""
