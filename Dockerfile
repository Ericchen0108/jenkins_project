FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome for AMD64 or Chromium for ARM64
RUN dpkg --print-architecture > /tmp/arch \
    && if [ "$(cat /tmp/arch)" = "amd64" ]; then \
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
        && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
        && apt-get update \
        && apt-get install -y google-chrome-stable; \
    else \
        apt-get update \
        && apt-get install -y chromium chromium-driver; \
    fi \
    && rm -rf /var/lib/apt/lists/*

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create reports and screenshots directories
RUN mkdir -p reports/screenshots

# Set environment variables
ENV HEADLESS=true
ENV BROWSER=chrome
ENV DISPLAY=:99

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Start Xvfb for headless browser support\n\
Xvfb :99 -screen 0 1920x1080x24 &\n\
export DISPLAY=:99\n\
\n\
# Wait for Xvfb to start\n\
sleep 2\n\
\n\
# Execute the command\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["pytest", "--html=reports/report.html", "--self-contained-html", "-v"]