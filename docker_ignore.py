# Create .dockerignore file
dockerignore_content = '''# Git files
.git
.gitignore

# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Documentation
*.md
!README.md

# Test files
test_*
*_test.py
tests/

# Build artifacts
build/
dist/
*.egg-info/

# Local directories that shouldn't be in container
input/
output/
examples/
'''

with open('.dockerignore', 'w') as f:
    f.write(dockerignore_content)

print("Created .dockerignore")

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

# Create a run script
run_script = '''#!/bin/bash
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
docker run --rm \\
    -v $(pwd)/input:/app/input \\
    -v $(pwd)/output:/app/output \\
    --network none \\
    pdf-outline-extractor:latest

echo ""
echo "Processing completed! Check the 'output' directory for results."
echo "Output files:"
ls -la output/
'''

with open('run.sh', 'w') as f:
    f.write(run_script)

print("Created run.sh")

# Make scripts executable (on Unix systems)
import stat
try:
    os.chmod('build.sh', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    os.chmod('run.sh', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    os.chmod('test_extractor.py', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    os.chmod('pdf_extractor.py', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    print("Made scripts executable")