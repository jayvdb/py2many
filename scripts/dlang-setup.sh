#!/usr/bin/env bash
set -euo pipefail

# Build dfmt once (version-pinned). `dub run dfmt` rebuilds/relinks on every
# call (https://github.com/dlang-community/dfmt/issues/407) and dub can't build
# a package safely from concurrent processes
# (https://github.com/dlang/dub/issues/1113), so the test suite (pytest-xdist)
# calls the prebuilt binary directly via PATH instead (see .mise.toml _.path
# and pyd/__init__.py). The dfmt version here must match the path in .mise.toml.
dub run --yes dfmt@0.15.2 -- --version
