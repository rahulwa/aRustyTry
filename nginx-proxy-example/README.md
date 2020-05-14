# Nginx as Reverse and Forward Proxy

It contains following setup -
1. Web server exposing API over HTTPS
2. App server exposing API over HTTP
3. Use nginx as reverse as well as forward proxy
4. Use any minimal framework for creating APIs
5. App server should return latest NYT Best Sellers Names
6. The latest NYT Best Sellers Names should be fetched directly from NYT dev APIs -
    https://developer.nytimes.com/docs/books-product/1/overview
7. App server should use nginx running on web server as a forward proxy

**We are using Flask for application and Nginx for reverse webserver/fordward proxy server.**

## Setting up python environment
We are using [pipenv](https://github.com/pypa/pipenv) as development workflow for Python.
- Installing pipenv

```sh
# For Ubuntu 18.04
echo 'export PATH="${HOME}/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
sudo apt install python3-pip
python3 -m pip install --user pipenv
# https://gist.github.com/planetceres/8adb62494717c71e93c96d8adad26f5c#troubleshooting-and-removal
# For Ubuntu 20.04
sudo apt install pipenv
#For Mac
brew install pipenv
```

## Setting Nginx
We need to use an out-of-tree module for connect requests needed for tunning HTTPS while in acting as forward proxy mode.
So we will need to compile nginx from source with [ngx_http_proxy_connect_module](https://github.com/chobits/ngx_http_proxy_connect_module):

```sh
## This instructions follow and tested in Ubuntu 18.04

# Installing dependencies
sudo apt install -y build-essential git libfontconfig1 libpcre3 libpcre3-dev git dpkg-dev libpng-dev perl libperl-dev libgd3 libgd-dev libgeoip1 libgeoip-dev geoip-bin libxml2 libxml2-dev libxslt1.1 libxslt1-dev
# OpenSSL version 1.1.0h Source
wget https://www.openssl.org/source/openssl-1.1.0h.tar.gz && tar -xzvf openssl-1.1.0h.tar.gz
# ngx_http_proxy_connect_module Source
git clone https://github.com/chobits/ngx_http_proxy_connect_module
# Nginx Source
wget http://nginx.org/download/nginx-1.18.0.tar.gz && tar -xzvf nginx-1.18.0.tar.gz
# Compiling Nginx and Installing it
cd nginx-1.18.0
patch -p1 < ../ngx_http_proxy_connect_module/patch/proxy_connect_rewrite_101504.patch
./configure --add-module=../ngx_http_proxy_connect_module \
    --with-http_ssl_module \
    --with-openssl=../openssl-1.1.0h
sudo make
sudo make install
# This is installed at /usr/local/nginx/sbin/nginx
# You can verify it via
/usr/local/nginx/sbin/nginx -V
> nginx version: nginx/1.18.0
> built by gcc 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04) 
> built with OpenSSL 1.1.0h  27 Mar 2018
> TLS SNI support enabled
> configure arguments: --add-module=../ngx_http_proxy_connect_module --with-http_ssl_module --with-openssl=../openssl-1.1.0h
# Now downloaded sources can be cleaned up
rm -rf nginx-* ngx_http_proxy_connect_module openssl-*
```

## Usage

- Setting up venv (by Pipenev) and starting flask server
```sh
cd nginx-proxy-example
pipenv install --three
# Should install flask and other dependencies also as it reads Pipfile automatically
export NYTIMES_API_KEY=<API_KEY OBTAINED FROM https://developer.nytimes.com/>
pipenv run python app.py
```
- Creating ssl self signed certs for local development (On prod, use letsencrypt)
```sh
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
```
- Starting nginx server with forward and reverse proxy mode
```sh
sudo cp cd nginx-proxy-example/nginx.conf /usr/local/nginx/conf/nginx.conf
sudo /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
# You can check that nginx is running on
# Port 80 for HTTP endpoint for application
# Port 443 for HTTPS endpoint for application
# Port 8081 for forward proxy server
sudo netstat -tunapl | grep nginx
> tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      11768/nginx: master 
> tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      11768/nginx: master 
> tcp        0      0 0.0.0.0:8081            0.0.0.0:*               LISTEN      11768/nginx: master 
> tcp6       0      0 :::443                  :::*                    LISTEN      11768/nginx: master 
> tcp6       0      0 :::80                   :::*                    LISTEN      11768/nginx: master 
```
- Now we can test our APIs
```sh
# Testing out HTTP endpoint
curl -i http://localhost/nytimes/books/bestsellers.json
# Testing out HTTPS endpoint
# -k for supprssing self signed error
curl -k -i https://localhost/nytimes/books/bestsellers.json
# Our application allows almost all api for nytimes books
# https://developer.nytimes.com/docs/books-product/1/overview
# as appended on `/nytimes/books/`
# Let's test some (like `/lists/current/hardcover-fiction.json`)
curl -i http://localhost/nytimes/books/lists/current/hardcover-fiction.json
# like `/reviews.json?author=Michelle+Obama`
curl -i http://localhost/nytimes/books//reviews.json?author=Michelle+Obama
```