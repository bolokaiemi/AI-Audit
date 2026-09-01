
# ============================================================
# AI AUDITOR V0.1
# Dockerfile
# ============================================================

# ------------------------------------------------------------
# 1. Use Python 3.9 Slim as the base image
# ------------------------------------------------------------
FROM python:3.9-slim

# ------------------------------------------------------------
# 2. Prevent Python from creating .pyc files
#    and make Python output appear immediately in Docker logs
# ------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------------------
# 3. Update Linux package list and install eSpeak
#    eSpeak is required by pyttsx3 for Linux TTS
# ------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        espeak \
        espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# 4. Set the application working directory
# ------------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------------
# 5. Copy requirements.txt first
#    This allows Docker to cache dependency installation
# ------------------------------------------------------------
COPY requirements.txt .

# ------------------------------------------------------------
# 6. Upgrade pip and install Python dependencies
# ------------------------------------------------------------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------
# 7. Copy the complete application into /app
# ------------------------------------------------------------
COPY . .

# ------------------------------------------------------------
# 8. Expose the Gunicorn application port
# ------------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------------
# 9. Start Flask application with Gunicorn
#
#    app:app means:
#       app.py       -> Python module
#       app           -> Flask application object
# ------------------------------------------------------------
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "app:app"]
