#!/bin/bash

# SSH_LOGGER_SERVER_URL=http://<server:port>/ssh/log/attempt
if [[ $PAM_TYPE == open_session ]]; then
    curl -X POST $SSH_LOGGER_SERVER_URL \
        -d '{"login_IP":'"$PAM_RHOST"', "login_user":'"$PAM_USER"'}' \
        -H "Content-Type: application/json"
fi