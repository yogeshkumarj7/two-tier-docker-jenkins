FROM python:3.10-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Force IPv4 + retry for apt
RUN echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4 \
    && apt-get update -o Acquire::Retries=5 \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --default-timeout=100 --retries 10 -r requirements.txt

COPY app/ .
COPY templates/ templates/
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

