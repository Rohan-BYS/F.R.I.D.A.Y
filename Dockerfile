# F.R.I.D.A.Y. Isolated Execution Sandbox (OpenHands standard)
FROM python:3.13-slim

WORKDIR /workspace

# Install system dependencies (including Audio and GUI capabilities)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    portaudio19-dev \
    alsa-utils \
    libdbus-1-3 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Set default virtual display
ENV DISPLAY=:99

# Install F.R.I.D.A.Y. dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright
RUN playwright install --with-deps chromium

# Copy core engine
COPY . .

# Run the API Nexus or Voice loop by default wrapped in Xvfb
CMD ["xvfb-run", "-a", "python", "friday_voice_listener.py"]
