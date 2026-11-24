
# AFTER image - small, multi-stage, non-root

# Stage 1: Build dependencies
FROM python:3.12-alpine AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Final lightweight image
FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy Flask application
COPY app/app.py .

# Copy frontend HTML templates
COPY app/templates ./templates

# Copy frontend CSS and static files
COPY app/static ./static

# Create a non-root user for security
RUN adduser -D -u 10001 appuser

USER 10001

# Flask application port
EXPOSE 5000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
