FROM alpine

LABEL description "Dockerfile based on this repo: https://github.com/hellt/nginx-uwsgi-flask-alpine-docker. Thanks, Roman Dodin <dodin.roman@gmail.com> !!"

# Copy python requirements file
COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache \
    python3 \
    build-base \
    python3-dev \
    py-pip \
    jpeg-dev \
    zlib-dev \
    bash \
    nginx \
    uwsgi \
    uwsgi-python3 \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r /tmp/requirements.txt && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache

# Copy the Nginx global conf
COPY nginx.conf /etc/nginx/
# Copy the Flask Nginx site conf
COPY site-nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Add demo app
#COPY ./app /app
WORKDIR /wedding-gallery

CMD ["/usr/bin/supervisord"]