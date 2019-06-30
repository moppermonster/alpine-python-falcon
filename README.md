# alpine-python-falcon
Alpine based Falcon and friends image

## About
[Alpine based docker image with Python3](https://github.com/nielsds/alpine-python) including [Falcon](https://falconframework.org/), [NGINX](https://www.nginx.com/), [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) and [Supervisord](http://supervisord.org/).

## Docker Hub
```
dutchsecniels/alpine-python-falcon
```
[Docker Hub](https://cloud.docker.com/repository/docker/dutchsecniels/alpine-python-falcon)

## Usage

### Build your own image
```Dockerfile
FROM dutchsecniels/alpine-python-falcon

COPY app.py /app.py

CMD ["/usr/bin/supervisord"]
```

### Mount your own files
An alternative to building your own container is mounting files over existing locations in the container.

Interesting files and their locations (in the container):

| File                                     | Description                                                                                   |
| :---                                     | :---                                                                                          |
| /app.py                                  | Main app, an example is provided with this repository                                         |
| /middleware.py                           | Falcon middleware, this image comes with json middleware by default                           |
| /static/                                 | Static directory, by default NGINX is configured to deliver static content from this location |
| /etc/nginx/nginx.conf                    | NGINX config file                                                                             |
| /etc/nginx/conf.d/falcon-site-nginx.conf | NGINX config extension, static can be configured from here                                    |
| /etc/uwsgi/uwsgi.ini                     | UWSGI config file                                                                             |
| /etc/supervisord.conf                    | Supervisord config file                                                                       |

#### docker-compose
Mounting files is considerably easier using docker-compose. This repository contains some [examples](#examples).

### Examples
This repository contains some [examples](https://github.com/nielsds/alpine-python-falcon-examples) using the image.

## Dockerfile
```Dockerfile
# Install friends
RUN apk add --no-cache nginx uwsgi uwsgi-python3 supervisor

# Install Falcon
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Clean up
RUN rm /etc/nginx/conf.d/default.conf
RUN rm -r /root/.cache

# Config files
COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/supervisord.conf

# Falcon json middleware
COPY middleware.py /middleware.py

# Prepare static directory
RUN mkdir /static

# Copy default app.py
COPY app.py /app.py

CMD ["/usr/bin/supervisord"]
```

## Building

### rebuild.sh
Simply use `rebuild.sh`
```bash
sh rebuild.sh
```
Default port: `http://localhost:5678`

### Manually
#### Build
```bash
docker build -t alpine-python-falcon .
```

#### Run
```
docker run -p 5678:80 alpine-python-falcon
```

## Credits, thanks and background

- [Inspiration](https://github.com/hellt/nginx-uwsgi-flask-alpine-docker/tree/master/python3) ([blog](https://netdevops.me/2017/flask-application-in-a-production-ready-container/))
- [Middleware](https://eshlox.net/2017/08/02/falcon-framework-json-middleware-loads-dumps/)
- [Falcon](https://falconframework.org/)
