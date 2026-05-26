#!/usr/bin/env bash
set -exuo pipefail

isort --check --diff \
    --skip tests/expected \
    --skip-glob 'tests/dir_cases/test1-*-expected/*' \
    */ *.py

black --check \
    --extend-exclude 'tests/(expected|dir_cases/test1-[^/]+-expected)/' \
    */ *.py

flake8 .

cpplint \
    --filter=-legal/copyright,-whitespace/semicolon,-runtime/reference \
    tests/expected/*.cpp
