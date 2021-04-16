// cargo-deps: strum, strum_macros
use strum::IntoEnumIterator;
use strum_macros::Display;
use strum_macros::EnumIter;

#[derive(Debug, Display, EnumIter, PartialEq)]
enum Colors {
    RED,
    GREEN,
    BLUE,
}

fn show() {
    for color in Colors::iter() {
        println!("{}", color);
    }
}

fn main() {
    show();
}
