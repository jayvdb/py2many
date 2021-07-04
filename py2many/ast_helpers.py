import ast

try:
    from ast import unparse
except ImportError:
    from astor import to_source as unparse

    # Note ast-compat and astunparse packages fail internally with:
    # AttributeError: 'Constant' object has no attribute 'kind'

    # https://github.com/isidentical/backports.ast_unparse/commit/e7b1aea is broken

unparse  # ignore pyflakes


def create_ast_node(code, at_node=None):
    new_node = ast.parse(code).body[0]
    if at_node:
        new_node.lineno = at_node.lineno
        new_node.col_offset = at_node.col_offset
    return new_node


def create_ast_block(body, at_node=None):
    block = ast.If(test=ast.Constant(value=True), body=body, orelse=[])
    block.rewritten = True
    if at_node:
        block.lineno = at_node.lineno
    ast.fix_missing_locations(block)
    return block


def create_noop_node(at_node=None, noop_type="pass"):
    return create_ast_node(noop_type or "pass", at_node=None)
