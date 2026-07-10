FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install your dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools==69.5.1 && \
    pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY LaredoMLModel.py .

# Expose KServe's default HTTP port
EXPOSE 8080

# Run your script using python directly
ENTRYPOINT ["python", "-m", "LaredoMLModel"]