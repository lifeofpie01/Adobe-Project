#!/bin/bash
# Run script for PDF Outline Extractor

set -e

# Create directories if they don't exist
mkdir -p input output

echo "Running PDF Outline Extractor..."
echo "================================"
echo "Input directory: $(pwd)/input"
echo "Output directory: $(pwd)/output"
echo ""

# Check if input directory has PDF files
if [ -z "$(ls -A input/*.pdf 2>/dev/null)" ]; then
    echo "Warning: No PDF files found in input directory"
    echo "Please place PDF files in the 'input' directory before running."
    exit 1
fi

echo "Found PDF files:"
ls -la input/*.pdf

echo ""
echo "Starting processing..."

# Run the container
docker run --rm \
    -v $(pwd)/input:/app/input \
    -v $(pwd)/output:/app/output \
    --network none \
    pdf-outline-extractor:latest

echo ""
echo "Processing completed! Check the 'output' directory for results."
echo "Output files:"
ls -la output/
