FROM python:3.9-slim

WORKDIR /app

# Create a non-root user
ARG PUID=1000
ARG PGID=1000
RUN groupadd -g ${PGID} appgroup && \
    useradd -u ${PUID} -g appgroup -s /bin/sh -m appuser

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .
RUN chown -R appuser:appgroup /app

USER appuser
EXPOSE 8000

# Run with Gunicorn (Production Server)
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "app:app"]