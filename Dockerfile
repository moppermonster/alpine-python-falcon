# https://github.com/nielsds/alpine-python-falcon

FROM dutchsecniels/alpine-python

MAINTAINER niels@dutchsec.com

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
COPY falcon-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/supervisord.conf

# Falcon json middleware
COPY middleware.py /middleware.py

# Prepare static directory
RUN mkdir /static

# Copy default app.py
COPY app.py /app.py

CMD ["/usr/bin/supervisord"]
