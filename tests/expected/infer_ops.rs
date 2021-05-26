//! ```cargo
//! [package]
//! edition = "2018"
//! [dependencies]
//! anyhow = "*"
//! ```

#![allow(clippy::collapsible_else_if)]
#![allow(clippy::double_parens)] // https://github.com/adsharma/py2many/issues/17
#![allow(clippy::map_identity)]
#![allow(clippy::needless_return)]
#![allow(clippy::print_literal)]
#![allow(clippy::ptr_arg)]
#![allow(clippy::redundant_static_lifetimes)] // https://github.com/adsharma/py2many/issues/266
#![allow(clippy::unnecessary_cast)]
#![allow(clippy::upper_case_acronyms)]
#![allow(clippy::useless_vec)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(non_upper_case_globals)]
#![allow(unused_imports)]
#![allow(unused_mut)]
#![allow(unused_parens)]

extern crate anyhow;
use anyhow::Result;

pub fn foo() {
    let a: i32 = 10;
    let b: i32 = 20;
    let c1: i32 = (a + b);
    assert!(c1 == 30);
    let c2: i32 = (a - b);
    assert!(c2 == -10);
    let c3: i32 = (a * b);
    assert!(c3 == 200);
    let c4: f64 = ((a as f64) / (b as f64));
    assert!(c4 == 0.5);
    let c5: i32 = -(a);
    assert!(c5 == -10);
    let d: f64 = 2.0;
    let e1: f64 = ((a as f64) + d);
    assert!(e1 == 12.0);
    let e2: f64 = ((a as f64) - d);
    assert!(e2 == 8.0);
    let e3: f64 = ((a as f64) * d);
    assert!(e3 == 20.0);
    let e4: f64 = ((a as f64) / d);
    assert!(e4 == 5.0);
    let f: f64 = -3.0;
    assert!(f < -2.9);
}

pub fn add1(x: i8, y: i8) -> i16 {
    return ((x as i16) + (y as i16)) as i16;
}

pub fn add2(x: i16, y: i16) -> i32 {
    return ((x as i32) + (y as i32)) as i32;
}

pub fn add3(x: i32, y: i32) -> i64 {
    return ((x as i64) + (y as i64)) as i64;
}

pub fn add4(x: i64, y: i64) -> i64 {
    return (x + y);
}

pub fn add5(x: u8, y: u8) -> u16 {
    return ((x as u16) + (y as u16)) as u16;
}

pub fn add6(x: u16, y: u16) -> u32 {
    return ((x as u32) + (y as u32)) as u32;
}

pub fn add7(x: u32, y: u32) -> u64 {
    return ((x as u64) + (y as u64)) as u64;
}

pub fn add8(x: u64, y: u64) -> u64 {
    return (x + y);
}

pub fn add9(x: i8, y: u16) -> u32 {
    return ((x as u32) + (y as u32)) as u32;
}

pub fn sub(x: i8, y: i8) -> i8 {
    return (x - y);
}

pub fn mul(x: i8, y: i8) -> i16 {
    return ((x as i16) * (y as i16)) as i16;
}

pub fn fadd1(x: i8, y: f64) -> f64 {
    return ((x as f64) + y);
}

pub fn show() {
    foo();
    assert!(fadd1(6, 6.0) == (12 as f64));
    println!("{}", "OK");
}

pub fn main() -> Result<()> {
    foo();
    show();
    Ok(())
}
