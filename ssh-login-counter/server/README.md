# SSH Login Counter Server

A server daemon written in Rust using Rocket. It provide a way to store and view the number of ssh login attempts happened on client. It provide below routes:
- `POST /ssh/log/attempt` will increment the counter (contains information about how many ssh login attempts happened) corresponding to sender'IP.
- `GET /ssh/logs` will display statics containing login attempts against each clients.

### Running the server

```sh
# Install Rust
curl https://sh.rustup.rs -sSf | sh

# Switch to Nightly
rustup default nightly

# Clone this repo
git clone https://github.com/rahulwa/aRustyTry.git
cd aRustyTry/ssh-login-counter/server

# Run the server (Access on port 8000)
cargo run
```

### Deployment

Deployment is written in Ansible.

- Ansible needs to be installed on the system.
- destinations (where to deploy) need to be entered on `deployment/hosts` file
- Change any variable in `deployment/vars/main.yml` if needed.
- Deployment can be done using:

```sh
cd deployment; ansible-playbook -i hosts deploy.yml
````