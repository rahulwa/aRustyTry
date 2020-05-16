monitoring_server-1.0
=========

A Monitoring server that uses
 - [collectd](https://collectd.org) to collect hosts metrics
 - [graphite](https://graphiteapp.org) as time series database
 - [grafana](grafana.org) for visualizing metrics
 - finally uses [seyren](https://github.com/scobal/seyren) for alerting system.

Requirements
------------

- Ubuntu 16.04

Example Playbook
----------------
```yml
 - hosts: all
   become: yes
   gather_facts: no
 #to install python2 on ubuntu
 #run second with enable gather_facts to run roles


  pre_tasks:
    - name: 'install python2'
      raw: test -e /usr/bin/python || (apt -y update && apt install -y python-minimal)

  roles:
    - monitoring_server-1.0
```

# Inside of monitoring_server-1.0 Role

## Graphite
- ```sudo apt-get install graphite-web graphite-carbon```
- ```sudo apt-get install postgresql libpq-dev python-psycopg2```
- ```mkdir /data/postgresql```
- ```chown -R postgres:postgres /data/postgresql/```
- ```vim /etc/postgresql/9.5/main/postgresql.conf```

```
data_directory = '/data/postgresql'
```

- ```sudo su - postgres```
- ```cd /usr/lib/postgresql/9.5/bin/```
- ```./initdb -D /data/postgresql/```
- ```createuser graphite_user --pwprompt```
```
graphite_user123$
```

- ```createdb -O graphite_user graphite_db```
- ```createdb -O graphite_user grafana_db```
- ```logout```

```
# postgresql Troubleshooting
sudo -u postgres psql
ALTER USER graphite_user WITH PASSWORD 'graphite_user123$';
show data_directory;
show all;
\list
\dt
\q
```
- ```mkdir /data/graphite/whisper```
- ```chown -R _graphite:_graphite /data/graphite```
- ```sudo vim /etc/graphite/local_settings.py```

```
WHISPER_DIR = '/data/graphite/whisper'
```

```
DATABASES = {
'default': {
   'NAME': 'graphite_db',
   'ENGINE': 'django.db.backends.postgresql_psycopg2',
   'USER': 'graphite_user',
   'PASSWORD': 'graphite_user123$',
   'HOST': '127.0.0.1',
   'PORT': ''
   }
}
```

```
SECRET_KEY = 'kcbskhdw7ry27rwfslcs3653'
```

```
TIME_ZONE = 'Asia/Kolkata'
```

```
USE_REMOTE_USER_AUTHENTICATION = True
```

- ```vim /etc/carbon/carbon.conf```

```
STORAGE_DIR    = /data/graphite/
LOCAL_DATA_DIR = /data/graphite/whisper/
```

- ```cd /usr/lib/python2.7/dist-packages/graphite/```
- ```python manage.py migrate auth```
- ```python manage.py migrate```
- ```sudo graphite-manage syncdb```
```
SUPERUSER: synup
PASSWORD of SUPERUSER: synup123
```

- ```sudo cp /usr/share/doc/graphite-carbon/examples/storage-aggregation.conf.example  /etc/carbon/storage-aggregation.conf```
- ```sudo vim /etc/default/graphite-carbon```

```
CARBON_CACHE_ENABLED=true
```
- ```sudo service carbon-cache start```
- ```sudo apt-get install apache2 libapache2-mod-wsgi```
- ```sudo a2dissite 000-default```
- ```sudo cp /usr/share/graphite-web/apache2-graphite.conf /etc/apache2/sites-available```
- ```sudo a2ensite apache2-graphite```
- ```sudo service apache2 reload```

```
#Deleting Data in whisper, if neede
rm -rf /data/graphite/whisper/collectd/ip-12-12-0-250/
```

## Collectd
- ```sudo apt-get install collectd collectd-utils```
- ```sudo vim /etc/collectd/collectd.conf```

```
FQDNLookup false
LoadPlugin network
LoadPlugin cpu
LoadPlugin df
LoadPlugin interface
LoadPlugin load
LoadPlugin memory
LoadPlugin Disk

LoadPlugin ping
<Plugin ping>
       Host "127.0.0.1"
       Interval 1.0
       Timeout 0.9
       TTL 255
       MaxMissed -1
</Plugin>

<Plugin df>
        FSType tmpfs
        MountPoint "/dev"
        IgnoreSelected true
</Plugin>


# Server
<Plugin "network">
  Listen "0.0.0.0"
</Plugin>

# Client
# <Plugin "network">
#   Server "Server IP" "server port(default UDP port 25826, can be blank if this used)"
# </Plugin>

LoadPlugin syslog
<Plugin syslog>
       LogLevel info
</Plugin>

LoadPlugin write_graphite
<Plugin write_graphite>
        <Node "graphite">
                Host "127.0.0.1"
                Port "2003"
                Protocol "tcp"
                LogSendErrors true
                Prefix "collectd."
                StoreRates true
                AlwaysAppendDS false
                EscapeCharacter "_"
        </Node>
</Plugin>

```

- ```sudo vim /etc/carbon/storage-schemas.conf```
```
[collectd]
pattern = ^collectd.*
retentions = 10s:1d,1m:7d,5m:30d,10m:1y
```
- ```sudo service carbon-cache stop```
- ```sudo service carbon-cache start```
- ```sudo service collectd restart```

## Grafana
- ```wget https://grafanarel.s3.amazonaws.com/builds/grafana_3.1.1-1470047149_amd64.deb```
- ```sudo apt-get install -y adduser libfontconfig```
- ```sudo dpkg -i grafana_3.1.1-1470047149_amd64.deb```
- ```sudo vim /etc/grafana/grafana.ini```

```
[database]
type = postgres
host = 127.0.0.1:5432
name = grafana_db
user = graphite_user
password = graphite_user123$
```
- ```sudo systemctl start grafana-server```
- ```systemctl enable grafana-server```

## Seyren
- ```sudo su -```
- ```curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.0.12.tgz```
- ```tar -zxvf mongodb-linux-x86_64-3.0.12.tgz```
- ```mkdir -p /opt/mongodb```
- ```cp -R -n mongodb-linux-x86_64-3.0.12/ /opt/mongodb```
- ```rm -rf mongodb-linux-x86_64-3.0.12```
- ```mkdir -p /data/db```
- ```/opt/mongodb/mongodb-linux-x86_64-3.0.12/bin/mongod &```
- ```sudo apt-get install -q -y openjdk-8-jre-headless && apt-get clean```
- ```wget https://github.com/scobal/seyren/releases/download/1.3.0/seyren-1.3.0.jar```
- ```export SMTP_HOST="aspmx.l.google.com"```
- ```export SMTP_PORT="25"```
- ```export SMTP_FROM="alert@synup.com"```
- ```java -jar seyren-1.3.0.jar```
- ```vim /etc/systemd/system/mongodb.service```

```
[Unit]
Description=Mongo database
After=network.target

[Service]
ExecStart=/opt/mongodb/mongodb-linux-x86_64-3.0.12/bin/mongod


[Install]
WantedBy=default.target
```
- ```systemctl enable mongodb.service```
- ```vim /opt/seyren-start.sh```

```
#!/bin/bash

export SMTP_HOST="aspmx.l.google.com"
export SMTP_PORT="25"
export SMTP_FROM="alerts@example.com"

/usr/bin/java -jar /opt/seyren-1.3.0.jar &
```
- ```vim /opt/seyren-stop.sh```

```
#!/bin/bash
# Grabs and kill a process from the pidlist that has the word myapp

pid=`ps aux | grep seyren | awk '{print $2}'`
kill -9 $pid
```
- ```chmod 744 /opt/seyren-st*```
- ```vim /etc/init.d/seyren```

```
#!/bin/bash
# Seyren
#
# description: startup script for seyren

case $1 in
    start)
        /bin/bash /opt/seyren-start.sh
    ;;
    stop)
        /bin/bash /opt/seyren-stop.sh
    ;;
    restart)
        /bin/bash /opt/seyren-stop.sh
        /bin/bash /opt/seyren-start.sh
    ;;
esac
exit 0
```
- ```systemctl enable seyren```
- ```vim /etc/systemd/system/seyren.service```

```
# NOT WORKING (just fyi)
[Unit]
Description=Seyren Alerting system
After=network.target
After=syslog.target
#After=grafana-server.service
#Afetr=collectd.service
Requires=mongodb.service

[Service]

Environment=SMTP_FROM="alert@example.com"
Environment=SMTP_HOST="aspmx.l.google.com"
Environment=SMTP_PORT="25"
Environment=GRAPHITE_URL="http://localhost:80"
Environment=MONGO_URL="mongodb://localhost:27017/seyren"
Environment=SEYREN_URL="http://localhost:8080/seyren"


ExecStart=/usr/bin/java -jar /opt/seyren-1.3.0.jar
WorkingDirectory=/opt/

User=root

[Install]
WantedBy=default.target
```

## Nginx

- ```vim /etc/nginx/sites-enabled/grafana.conf```

```
server  {
        listen 80;
        #listen 443 ssl http2;
        #listen [::]:443 ssl http2;
        server_name monitor.example.com;

        root /usr/share/grafana/;

        location / {
                proxy_pass http://127.0.0.1:3000;
        }

        location ~ /.well-known {
                allow all;
        }
}
```
