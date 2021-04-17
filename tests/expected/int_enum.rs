#[derive(PartialEq)]
enum Colors {
    RED,
    GREEN,
    BLUE,
}

fn show() {
    if Colors::RED == Colors::RED {
        println!("{}", "OK");
    }
    println!("{}", "OK");
}

fn main() {
    show();
}
