#!/usr/bin/env bash

MODE=$1
shift

# Under git-bash on Windows the test passes a native path (D:\...\foo.rs), where
# coreutils treat '\' as an ordinary char (only '/' separates) -- so basename,
# sed and cp all mis-parse it. Normalise backslashes to forward slashes; this is
# a no-op on Linux/macOS where paths contain no backslashes.
TEST_FILE="${1//\\//}"

# Determine the correct sed command
if [[ "$(uname)" == "Darwin" ]]; then
    # macOS: Use gsed
    SED="gsed"
else
    # Linux/Other: Use sed
    SED="sed"
fi

# Per-case project dir so parallel runs (pytest-xdist) don't clobber a shared
# common-rust-proj/src/main.rs and end up executing the wrong case's binary.
bin_name=$(basename -s .rs "$TEST_FILE")
DIR="common-rust-proj-${bin_name}"

# Share the build cache across cases so cargo doesn't recompile structopt
# (etc.) once per directory. Use the Windows-form cwd on git-bash (pwd -W) so the
# native cargo.exe understands the absolute path; plain pwd elsewhere.
WORKDIR="$(pwd -W 2>/dev/null || pwd)"
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$WORKDIR/common-rust-target}"

# Debug (surfaced via the test's captured skip message on failure).
echo "[rust-runner] MODE=$MODE arg1=$1" >&2
echo "[rust-runner] TEST_FILE=$TEST_FILE" >&2
echo "[rust-runner] bin_name=$bin_name DIR=$DIR" >&2
echo "[rust-runner] uname=$(uname) pwd=$(pwd) WORKDIR=$WORKDIR" >&2
echo "[rust-runner] CARGO_TARGET_DIR=$CARGO_TARGET_DIR cargo=$(command -v cargo)" >&2

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    # If the directory doesn't exist, create a new Cargo binary project
    cargo new --bin "$DIR"

    echo "Created new Cargo binary project in $DIR"
fi

# Extract the embedded Cargo.toml content
# Look for lines between ```cargo and ```
# Remove the first 4 characters (e.g., "//! ") from each line
$SED -n '/```cargo/,/```/p' "$TEST_FILE" | $SED '1d;$d' | $SED 's#^//!##' | $SED 's/^ //' > $DIR/Cargo.toml
$SED -i "s/^.package.\$/[package]\nname=\"$bin_name\"/" $DIR/Cargo.toml

# Now copy the argument to the target dir
cp "$TEST_FILE" $DIR/src/main.rs
shift;

if [ "$MODE" = "lint" ]; then
    cd $DIR
    # uncomment if there are lint errors py2many didn't fix or was asked not to fix
    #cargo clippy --fix --allow-dirty
    cargo clippy
elif [ "$MODE" = "compile" ]; then
    cargo build --manifest-path $DIR/Cargo.toml
else
    cargo run --manifest-path $DIR/Cargo.toml $*
fi
