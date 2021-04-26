// cargo-deps: flagset
extern crate flagset;
use flagset::flags;
use flagset::FlagSet;
use std::collections::HashMap;
use std::os::raw::c_int;

#[derive(Clone, Eq, Hash, PartialEq)]
enum Colors {
    RED,
    GREEN,
    BLUE,
}

flags! {
    enum Permissions: c_int {
        R = 1,
        W = 2,
        X = 16,
    }
}
struct PermissionsContainer(FlagSet<Permissions>);
impl PermissionsContainer {
    fn new(flags: impl Into<FlagSet<Permissions>>) -> PermissionsContainer {
        PermissionsContainer(flags.into())
    }
}

fn show() {
    let color_map: _ = [
        (Colors::RED, "red"),
        (Colors::GREEN, "green"),
        (Colors::BLUE, "blue"),
    ]
    .iter()
    .cloned()
    .collect::<HashMap<_, _>>();
    let a: _ = Colors::GREEN;
    if a == Colors::GREEN {
        println!("{}", "green");
    } else {
        println!("{}", "Not green");
    }
    let b: PermissionsContainer = PermissionsContainer::new(Permissions::R | Permissions::W);
    if (b.0 & Permissions::R).bits() != 0b0 {
        println!("{}", "R");
    } else {
        println!("{}", "Not R");
    }
    if (b.0 & Permissions::W).bits() != 0b0 {
        println!("{}", "W");
    } else {
        println!("{}", "Not W");
    }
    if (b.0 & Permissions::X).bits() != 0b0 {
        println!("{}", "X");
    } else {
        println!("{}", "Not X");
    }
}

fn main() {
    show();
}
