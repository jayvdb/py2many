import os

from py2many.language import LanguageSettings

from .inference import infer_kotlin_types
from .transpiler import KotlinBitOpRewriter, KotlinPrintRewriter, KotlinTranspiler


def settings(args, env=os.environ):
    return LanguageSettings(
        KotlinTranspiler(),
        ".kt",
        "Kotlin",
        ["jgo", "--add-opens", "java.base/java.lang=ALL-UNNAMED", "com.pinterest:ktlint", "-F"],
        rewriters=[KotlinBitOpRewriter()],
        transformers=[infer_kotlin_types],
        post_rewriters=[KotlinPrintRewriter()],
        linter=["jgo", "com.pinterest:ktlint"],
    )
