# Create a build script
build_script = '''#!/bin/bash
# Build script for PDF Outline Extractor

set -e

echo "Building PDF Outline Extractor Docker Image..."
echo "=============================================="

# Build the image
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .

echo ""
echo "Build completed successfully!"
echo ""
echo "To run the container:"
echo "docker run --rm -v \\$(pwd)/input:/app/input -v \\$(pwd)/output:/app/output --network none pdf-outline-extractor:latest"
echo ""
echo "Make sure to create 'input' directory with PDF files before running."
'''

with open('build.sh', 'w') as f:
    f.write(build_script)

print("Created build.sh")