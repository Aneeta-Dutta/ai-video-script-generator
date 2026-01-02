FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY production_references/ ./production_references/
COPY run_e2e_sequential.py .
COPY server.py .

# Create output directories
RUN mkdir -p outputs/research_reports outputs/production_scripts outputs/sessions logs/metrics

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    GOOGLE_GENAI_USE_VERTEXAI=true

# Cloud Run will provide service account automatically
# No need to copy credentials file

# Health check endpoint (if needed for Cloud Run)
EXPOSE 8080

# Run the web server
CMD ["python", "server.py"]
