import ast
import io

from .analysis import get_id
from .ast_helpers import create_ast_node, create_noop_node, unparse
from .clike import CLikeTranspiler

from py2rb import convert_py2rb
from voc.transpiler import Transpiler as VOCTranspiler
import transpyle
from sherlock.codelib.generator import CodeGenerator

TYPING_IMPORTS = ["ctypes", "typing"]


# https://github.com/Escape-Technologies/pyuntype
class RemoveTypingImportRewriter(ast.NodeTransformer):

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

class DowngradeAnnAssignRewriter(ast.NodeTransformer):

    def visit_AnnAssign(self, node):
        col_offset = getattr(node, "col_offset", None)

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

        dir_path = node.__file__.parent
        _, header, data = convert_py2rb(unparse(node), dir_path)
        return f"{header}\n{data}"

    def usings(self):
        return ""


class JavaClassTranspiler(CLikeTranspiler):
    NAME = "javaclass"

    def visit(self, node):
        source_data = unparse(node)
        t = VOCTranspiler(namespace="build")  # to match the tests
        dir_path = node.__file__.parent
        t.transpile_string(node.__file__.stem, node)
        assert t.classfiles
        print(t.classfiles)
        _, _, out = t.classfiles[0]
        print(out.__class__, out.__class__.__module__)
        buf = io.BytesIO()
        writer = io.BufferedWriter(buf)
        out.write(buf)
        #raise Exception
        return buf.getvalue()


class JavaTranspiler(CLikeTranspiler):
    NAME = "java"

    def visit(self, node):
        out = JavaClassTranspiler().visit(node)
        # use javap -c? nope
        # python https://github.com/Storyyeller/Krakatau/pull/157
        # https://github.com/drstrng/Krakatau-noff
        return out


class FortranTranspiler(CLikeTranspiler):
    NAME = "fortran"

    def visit(self, node):
        code = unparse(node)

        from_language = transpyle.Language.find('Python 3.6')
        to_language = transpyle.Language.find('Fortran 95')
        assert to_language
        translator = transpyle.AutoTranslator(from_language, to_language)
        return translator.translate(code)



class CTranspiler(CLikeTranspiler):
    NAME = "clang"

    def visit(self, node):
        code = unparse(node)

        from_language = transpyle.Language.find('Python 3.6')
        to_language = transpyle.Language.find('C99')
        assert to_language
        translator = transpyle.AutoTranslator(from_language, to_language)
        # Python to C is not supported
        return translator.translate(code)



class ShellTranspiler(CLikeTranspiler):
    NAME = "shell"

    def visit(self, node):
        code = unparse(node)

        generator = CodeGenerator(code)
        return generator.generate()



class SchemeTranspiler(CLikeTranspiler):
    NAME = "scheme"

    def visit(self, node):
        from PySchemeTranspiler.converter import Converter
        code = unparse(node)
        buf = io.StringIO(code)
        buf.name = str(node.__file__)

        out = Converter.transpile(buf)
        return out