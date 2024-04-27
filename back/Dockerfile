FROM python:3.12-alpine

WORKDIR /srv

COPY requirements.txt .

RUN apk update && \
    apk add --no-cache vim \
	gcc \
	python3-dev \
	musl-dev \
	libpq \
	libpq-dev \
	bash \
    netcat-openbsd && \
    pip install -r requirements.txt

COPY src /srv
COPY ./tools/wait-for-it.sh /usr/local/bin/wait-for-it.sh
COPY ./tools/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY ./tools/reset_migrations.sh /usr/local/bin/reset_migrations.sh

RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/wait-for-it.sh /usr/local/bin/reset_migrations.sh

ENTRYPOINT ["/bin/sh", "/usr/local/bin/entrypoint.sh"]
