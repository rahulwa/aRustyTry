# SSH Login Counter Agent

It is uses `pam_exec` library to evoke below script to send ssh login attempt to server (PAM is an API that takes care of authenticating a user to a service.):

```sh
if [[ $PAM_TYPE == open_session ]]; then
    curl -X POST $SSH_LOGGER_SERVER_URL \
        -d '{"login_IP":'"$PAM_RHOST"', "login_user":'"$PAM_USER"'}' \
        -H "Content-Type: application/json"
fi
```

### Running the script

```sh
# Assuming root

cat > /root/ssh_logger_agent.sh <<EOF
#!/bin/bash

# Put SERVER and PORT
SSH_LOGGER_SERVER_URL=http://<SERVER:PORT>/ssh/log/attempt
if [[ $PAM_TYPE == open_session ]]; then
    curl -X POST $SSH_LOGGER_SERVER_URL \
        -d '{"login_IP":'"$PAM_RHOST"', "login_user":'"$PAM_USER"'}' \
        -H "Content-Type: application/json"
fi
EOF
chmod u+x /root/ssh_logger_agent.sh
echo 'session    optional    pam_exec.so /root/ssh_logger_agent.sh' >> /etc/pam.d/sshd
```

### Deployment

Deployment is written in Ansible.

- Ansible needs to be installed on the system.
- destinations (where to deploy) need to be entered on `deployment/hosts` file
- Deployment can be done using:

```sh
ansible-playbook -i hosts deploy.yml
````