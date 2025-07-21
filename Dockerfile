FROM alpine

RUN apk add --update --no-cache \
    gcc \
    python3-dev \
    py3-pip \
    musl-dev \
    libffi-dev \
    openssl-dev \
    linux-headers \
    libffi \
    openssl

WORKDIR /app

COPY ./app.py /app

COPY ./requirements.txt /app

COPY ./telemetry.py /app

RUN pip install --no-cache-dir --break-system-packages --upgrade -r /app/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5003", "--proxy-headers"]
