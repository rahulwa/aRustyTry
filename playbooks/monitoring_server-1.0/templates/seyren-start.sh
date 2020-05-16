#!/bin/bash

export SEYREN_LOG_PATH="/var/log/";
export GRAPHITE_URL="http://localhost:{{graphite_port}}";
#export SMTP_HOST="aspmx.l.google.com"
#export SMTP_PORT="25"
export SMTP_HOST="{{seyren_SMTP_HOST}}";
export SMTP_PORT="{{seyren_SMTP_PORT}}";
export SMTP_FROM="{{seyren_SMTP_FROM}}";
export SMTP_USERNAME="{{seyren_SMTP_USERNAME}}";
export SMTP_PASSWORD="{{seyren_SMTP_PASSWORD}}";
# export SMTP_PROTOCOL="smtp"
export SLACK_TOKEN="{{seyren_SLACK_TOKEN}}";
export SLACK_USERNAME="{{seyren_SLACK_USERNAME}}";



/usr/bin/java -jar /opt/seyren-1.3.0.jar &
