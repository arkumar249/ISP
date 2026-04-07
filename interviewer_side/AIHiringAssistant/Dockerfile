# ============================================================
# AI Hiring Assistant – Interviewer Side
# ============================================================
FROM python:3.10-slim

# System dependencies for Qt6, OpenCV, and X11
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 \
    libxkbcommon0 libdbus-1-3 \
    libxcb-xinerama0 libxcb-cursor0 libxcb-shape0 \
    libegl1 libfontconfig1 libx11-xcb1 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-randr0 libxcb-render-util0 libxcb-shm0 \
    libxcb1 libx11-6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure data directory exists
RUN mkdir -p /app/user_data

ENV QT_QPA_PLATFORM=xcb

CMD ["python", "main.py"]
