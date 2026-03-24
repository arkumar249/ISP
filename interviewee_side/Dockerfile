# ============================================================
# AI Hiring Assistant – Interviewee Side
# PyQt6 GUI app with webcam, OpenCV, MediaPipe
# ============================================================
FROM python:3.11-slim

# System dependencies for Qt6, OpenCV, and MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    # OpenCV / video
    libgl1 libglib2.0-0 \
    # Qt6 / XCB platform plugin
    libxkbcommon0 libdbus-1-3 \
    libxcb-xinerama0 libxcb-cursor0 libxcb-shape0 \
    libegl1 libfontconfig1 libx11-xcb1 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-randr0 libxcb-render-util0 libxcb-shm0 \
    libxcb1 libx11-6 libxext6 libxrender1 \
    # Multimedia backend
    libgstreamer1.0-0 gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    # Webcam
    libv4l-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure user_data directory exists
RUN mkdir -p /app/user_data

# Set Qt to use xcb platform (X11 forwarding)
ENV QT_QPA_PLATFORM=xcb

CMD ["python", "main.py"]
