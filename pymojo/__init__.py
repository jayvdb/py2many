import os

from py2many.language import LanguageSettings

from .inference import infer_mojo_types
from .rewriters import (
    MojoDictKeysInElider,
    MojoImplicitConstructor,
    MojoInferMoveSemantics,
)
from .transpiler import MojoTranspiler


def settings(args, env=os.environ):
    mojo_args = {}
    return LanguageSettings(
        MojoTranspiler(**mojo_args),
        ".mojo",
        "Mojo",
        ["mojo", "format"],
        None,
        [MojoInferMoveSemantics()],
        [infer_mojo_types],
        post_rewriters=[
            # Runs after type inference so it can check the receiver is a Dict.
            MojoDictKeysInElider(),
            MojoImplicitConstructor(),
        ],
    )
