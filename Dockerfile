FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    curl \
    ca-certificates \
    libx11-dev \
    libxcomposite-dev \
    libxrandr-dev \
    libxtst-dev \
    libnss3-dev \
    libgdk-pixbuf2.0-0 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libappindicator3-1 \
    libasound2 \
    libpangocairo-1.0-0

RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/trusted.gpg.d/google.asc
RUN sh -c 'echo "deb [signed-by=/etc/apt/trusted.gpg.d/google.asc] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get update && apt-get install -y google-chrome-stable

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5000
CMD ["python", "app.py"]