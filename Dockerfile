# Base image with CUDA and PyTorch
FROM pytorch/pytorch:2.2.0-cuda11.8-cudnn8-runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy your code
COPY . /app

# Install any system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Default command (can be overridden)
ENTRYPOINT ["python", "scenesage.py"]