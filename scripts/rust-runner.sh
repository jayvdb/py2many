#!/usr/bin/env bash

MODE=$1
shift


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
bin_name=$(basename -s .rs $1)
DIR="common-rust-proj-${bin_name}"

# Share the build cache across cases so cargo doesn't recompile structopt
# (etc.) once per directory.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$(pwd)/common-rust-target}"

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    # If the directory doesn't exist, create a new Cargo binary project
    cargo new --bin "$DIR"

    echo "Created new Cargo binary project in $DIR"
fi

# Extract the embedded Cargo.toml content
# Look for lines between ```cargo and ```
# Remove the first 4 characters (e.g., "//! ") from each line
$SED -n '/```cargo/,/```/p' "$1" | $SED '1d;$d' | $SED 's#^//!##' | $SED 's/^ //' > $DIR/Cargo.toml
$SED -i "s/^.package.\$/[package]\nname=\"$bin_name\"/" $DIR/Cargo.toml

# Now copy the argument to the target dir
cp $1 $DIR/src/main.rs
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
