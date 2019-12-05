#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] extern crate rocket;
extern crate serde;
extern crate serde_json;

use rocket::{State, StaticFiles};
use serde::{Deserialize, Serialize};

// extern crate sysfs_gpio;

use std::sync::atomic::{AtomicUsize, Ordering};

#[derive(Debug, Serialize, Deserialize)]
struct PingPongState {
    firing_speed: AtomicUsize,
    oscillation_frequency: AtomicUsize,
    backspin: AtomicUsize,
    topspin: AtomicUsize,
}

impl PingPongState {
    fn update(&self) {
        //
    }
}

// Expects an int between 5 and 70. 
#[get("/set-firing-speed/<speed>")]
fn set_firing_speed(speed: usize, state: State<PingPongState>) -> String {
    state.firing_speed.swap(speed, Ordering::Relaxed);
    state.update();
    serde_json::to_string(state.inner()).unwrap()
}

// Expects int between 0 and 50
#[get("/set-oscillation-frequency/<frequency>")]
fn set_oscillation_frequency(frequency: usize, state: State<PingPongState>) -> String {
    state.oscillation_frequency.swap(frequency, Ordering::Relaxed);
    state.update();
    serde_json::to_string(state.inner()).unwrap()
}

// Expects int between 0 and 100
#[get("/set-backspin/<frequency>")]
fn set_backspin(frequency: usize, state: State<PingPongState>) -> String {
    state.backspin.swap(frequency, Ordering::Relaxed);
    state.update();
    serde_json::to_string(state.inner()).unwrap()
}

// Expects int between 0 and 100
#[get("/set-topspin/<frequency>")]
fn set_topspin(frequency: usize, state: State<PingPongState>) -> String {
    state.topspin.swap(frequency, Ordering::Relaxed);
    state.update();
    serde_json::to_string(state.inner()).unwrap()
}

fn main() {
    let machine_state = PingPongState {
        firing_speed: AtomicUsize::new(0),
        oscillation_frequency: AtomicUsize::new(0),
        backspin: AtomicUsize::new(0),
        topspin: AtomicUsize::new(0)
    };

    rocket::ignite()
        .mount("/", StaticFiles::from(concat!(env!("CARGO_MANIFEST_DIR"), "/frontend")))
        .mount("/api/v1/", routes![set_firing_speed])
        .mount("/api/v1/", routes![set_oscillation_frequency])
        .mount("/api/v1/", routes![set_backspin])
        .mount("/api/v1/", routes![set_topspin])
        .manage(machine_state)
        .launch();
}