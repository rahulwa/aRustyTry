#![feature(proc_macro_hygiene, decl_macro)]

use concurrent_hashmap::*;
use std::net::SocketAddr;
use rocket::State;
#[macro_use] extern crate rocket;

// To Hold SSH Login attempts
struct LoginCounter {
    // For now using hash data type, but a persistent data-store (Like any sql databases) should be use
    store: ConcHashMap<String, u32>
}

// Implementing needed methods for LoginCounter
//TODO, for now just added new method
impl LoginCounter {
    fn new() -> LoginCounter {
        let map = ConcHashMap::<String, u32>::new();
        LoginCounter { store: map }
    }
}

// Using post verb as it is changing state of system although there is no requirement of body
#[post("/ssh/log/attempt")]
fn update_ssh_counter(counter: State<LoginCounter>, remote_addr: SocketAddr) -> &'static str {
    let addr = remote_addr.ip().to_string();
    counter.store.upsert(addr, 1, &|count| *count += 1);
    return "Logged Entry"
}

#[get("/ssh/logs")]
fn getall_ssh_counters(counter: State<LoginCounter>) -> String {
    let mut values = String::from("Metrics for ssh log-in attempts");
    for (client, &count) in counter.store.iter() {
        values.push_str(&format!("\n{} ssh log-in attempts were made at {}", count, client));
    }
    values
}

fn main() {
    let ssh_login_counter = LoginCounter::new();
    rocket::ignite()
        .manage(ssh_login_counter)
        .mount("/", routes![update_ssh_counter, getall_ssh_counters])
        .launch();
}