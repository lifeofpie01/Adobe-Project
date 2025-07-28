# Create Dockerfile
dockerfile_content = '''# Use official Python slim image for AMD64 architecture
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PyMuPDF
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    libmupdf-dev \\
    libfreetype6-dev \\
    libjpeg-dev \\
    libopenjp2-7-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY pdf_extractor.py .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set permissions
RUN chmod +x pdf_extractor.py

# Default command - process all PDFs in /app/input and output to /app/output
CMD ["python", "pdf_extractor.py", "--input", "/app/input", "--output", "/app/output"]
'''

with open('Dockerfile', 'w') as f:
    f.write(dockerfile_content)

print("Created Dockerfile")