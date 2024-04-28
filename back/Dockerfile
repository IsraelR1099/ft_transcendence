FROM python:3.12-alpine

WORKDIR /srv

COPY requirements.txt .

RUN apk update && \
    apk add --no-cache gcc \
	libffi-dev \
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

RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/wait-for-it.sh

ENTRYPOINT ["/bin/sh", "/usr/local/bin/entrypoint.sh"]
