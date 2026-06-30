FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --target=/install \
    -r requirements.txt


FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/install

RUN groupadd -g 10003 workeruser && \
    useradd -u 10003 -g workeruser -m -s /usr/sbin/nologin workeruser

COPY --from=builder /install /install

COPY --chown=workeruser:workeruser app ./app
# COPY --chown=workeruser:workeruser main.py .
# COPY --chown=workeruser:workeruser wallet .

USER workeruser

ENTRYPOINT ["python -m ", "app.infrastructure.api.main.py"]