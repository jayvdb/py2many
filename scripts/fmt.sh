#!/usr/bin/env bash
set -exuo pipefail

# Write counterpart of lint.sh: apply isort + black in place. flake8/cpplint are
# lint-only (no autofix), so they aren't run here.

isort \
    --skip tests/expected \
    --skip-glob 'tests/dir_cases/test1-*-expected/*' \
    */ *.py

black \
    --extend-exclude 'tests/(expected|dir_cases/test1-[^/]+-expected)/' \
    */ *.py
