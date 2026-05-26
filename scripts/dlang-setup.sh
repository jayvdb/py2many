#!/usr/bin/env bash
set -euo pipefail

# Pre-fetch and build dfmt once so the parallel `dub run dfmt` invocations from
# the test suite (pytest-xdist) don't race to populate and compile the shared
# ~/.dub cache.
dub run --yes dfmt -- --version
