from .analysis import add_imports
from .annotation_transformer import add_annotation_flags

from .context import add_variable_context, add_list_calls
from .inference import infer_types
from .language import LanguageSettings
from .mutability_transformer import detect_mutable_vars
from .nesting_transformer import detect_nesting_levels
from .scope import add_scope_context

from .rewriters import (
    ComplexDestructuringRewriter,
    FStringJoinRewriter,
    PythonMainRewriter,
    DocStringToCommentRewriter,
    PrintBoolRewriter,
    StrStrRewriter,
    WithToBlockTransformer,
    IgnoredAssignRewriter,
    UnpackScopeRewriter,
)


def core_transformers(tree, trees):
    add_variable_context(tree, trees)
    add_scope_context(tree)
    add_list_calls(tree)
    detect_mutable_vars(tree)
    detect_nesting_levels(tree)
    add_annotation_flags(tree)
    infer_meta = infer_types(tree)
    add_imports(tree)
    return tree, infer_meta


def language_tree_processors(settings: LanguageSettings):
    transpiler = settings.transpiler
    rewriters = settings.rewriters
    transformers = settings.transformers
    post_rewriters = settings.post_rewriters
    language = transpiler.NAME
    generic_rewriters = [
        ComplexDestructuringRewriter(language),
        PythonMainRewriter(settings.transpiler._main_signature_arg_names),
        FStringJoinRewriter(language),
        DocStringToCommentRewriter(language),
        WithToBlockTransformer(language),
        IgnoredAssignRewriter(language),
    ]
    # Language independent rewriters that run after type inference
    generic_post_rewriters = [
        PrintBoolRewriter(language),
        StrStrRewriter(language),
        UnpackScopeRewriter(language),
    ]
    rewriters = generic_rewriters + rewriters
    post_rewriters = generic_post_rewriters + post_rewriters
    return rewriters, transformers, post_rewriters


def transpile_one(trees, tree, transpiler, settings):
    rewriters, transformers, post_rewriters = language_tree_processors(settings)
    # This is very basic and needs to be run before and after
    # rewrites. Revisit if running it twice becomes a perf issue
    add_scope_context(tree)
    # Language specific rewriters
    for rewriter in rewriters:
        tree = rewriter.visit(tree)
    # Language independent core transformers
    tree, infer_meta = core_transformers(tree, trees)
    # Language specific transformers
    for tx in transformers:
        tx(tree)
    # Language specific rewriters that depend on previous steps
    for rewriter in post_rewriters:
        tree = rewriter.visit(tree)
    # Rerun core transformers
    tree, infer_meta = core_transformers(tree, trees)
    out = []
    code = transpiler.visit(tree) + "\n"
    headers = transpiler.headers(infer_meta)
    features = transpiler.features()
    if features:
        out.append(features)
    if headers:
        out.append(headers)
    usings = transpiler.usings()
    if usings:
        out.append(usings)
    out.append(code)
    if transpiler.extension:
        out.append(transpiler.extension_module(tree))
    return "\n".join(out)
