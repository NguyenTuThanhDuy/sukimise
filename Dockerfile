FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && rm -rf /tmp/* /var/cache/*

COPY requirements.lock /
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r requirements.lock

COPY . /webapps

WORKDIR /webapps

ENV PYTHONPATH=/webapps

ENTRYPOINT ["./entry_point.sh"]
