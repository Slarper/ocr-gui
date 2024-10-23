use prgrs::Prgrs;
use std::{thread, time};

fn main() {
    for _ in Prgrs::new((0..1000).enumerate(), 1000) {
        thread::sleep(time::Duration::from_millis(10));
            
    }
}
