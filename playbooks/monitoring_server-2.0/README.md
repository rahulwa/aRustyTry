monitoring_server-2.0
=========

An Ansible role to install and configure [Prometheus](http://prometheus.io) monitoring server and [Grafana](http://grafana.org).


Requirements
------------

- Ubuntu 16.04


vars
------------

Change variables in vars/main.yml for latest software version.

```
# vars file for prometheus
aws_access_key: ""
aws_secret_key: ""
grafana_proxy_port: 80
server_dns_name: "monitor.example.com"
smtp_auth_username: ""
smtp_auth_password: ""
slack_api_url: ""
prometheus_node_exporter_version: "0.12.0"
prometheus_version: "1.1.2"
prometheus_alertmanager_version: "0.4.2"
```

Features
------------

 - Monitoring AWS Servers based on `monitoring` tag is `enabled` or not.
 - send notifications to slack
 - Also Configure `node_exporter`, `alertmanager` and `Grafana`
