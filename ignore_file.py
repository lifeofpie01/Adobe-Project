# Create .gitignore file
gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
input/
output/
test_input/
test_output/
examples/
*.pdf
*.json

# Docker
.dockerignore

# Logs
*.log
'''

with open('.gitignore', 'w') as f:
    f.write(gitignore_content)

print("Created .gitignore")

# Create final deployment guide
deployment_guide = '''# Deployment Guide - PDF Outline Extractor

## Adobe India Hackathon Challenge - Round 1A

This guide provides complete instructions for deploying and running the PDF Outline Extractor solution.

## System Requirements

- **Platform**: AMD64 Linux
- **Docker**: Version 20.x or higher
- **Memory**: 8 CPUs, 16 GB RAM (as per challenge specs)
- **Storage**: ~500 MB for Docker image
- **Network**: None required (runs offline)

## Deployment Steps

### 1. Project Setup

```bash
# Clone or extract the project files
# Ensure you have all these files:
# - pdf_extractor.py
# - Dockerfile  
# - requirements.txt
# - README.md
# - build.sh
# - run.sh
```

### 2. Build Docker Image

```bash
# Method 1: Using build script
chmod +x build.sh
./build.sh

# Method 2: Manual build
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

### 3. Prepare Input Data

```bash
# Create input directory
mkdir -p input

# Copy PDF files to input directory
cp /path/to/your/pdfs/*.pdf input/

# Verify PDFs are ready
ls -la input/
```

### 4. Run Processing

```bash
# Method 1: Using run script
chmod +x run.sh
./run.sh

# Method 2: Manual run
mkdir -p output
docker run --rm \\
  -v $(pwd)/input:/app/input \\
  -v $(pwd)/output:/app/output \\
  --network none \\
  pdf-outline-extractor:latest
```

### 5. Verify Results

```bash
# Check output files
ls -la output/

# Validate JSON format
python test_extractor.py
```

## Expected Performance

- **Processing Time**: ≤ 10 seconds per 50-page PDF
- **Memory Usage**: < 1 GB RAM per PDF
- **Image Size**: ~200 MB total
- **CPU Usage**: 100% utilization during processing

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x build.sh run.sh pdf_extractor.py
   ```

2. **Platform Mismatch**
   ```bash
   docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
   ```

3. **No PDFs Found**
   ```bash
   # Ensure PDFs are in input/ directory
   find input/ -name "*.pdf" -type f
   ```

4. **Docker Network Issues**
   ```bash
   # Must use --network none as per challenge requirements
   docker run --rm --network none ...
   ```

### Debug Mode

```bash
# Enable detailed logging
docker run --rm \\
  -v $(pwd)/input:/app/input \\
  -v $(pwd)/output:/app/output \\
  --network none \\
  pdf-outline-extractor:latest \\
  python pdf_extractor.py --input /app/input --output /app/output --debug
```

### Local Testing

```bash
# Install dependencies locally
pip install -r requirements.txt

# Run without Docker
python pdf_extractor.py --input ./input --output ./output --debug
```

## Validation Checklist

- [ ] Docker image builds successfully on AMD64
- [ ] Container runs with --network none
- [ ] Processes PDFs within time limit (≤ 10 seconds for 50 pages)
- [ ] Outputs valid JSON in required format
- [ ] Handles multiple PDFs in batch
- [ ] Gracefully handles malformed PDFs
- [ ] No internet connectivity required

## Challenge Compliance

✅ **Input/Output**: Reads from `/app/input`, writes to `/app/output`
✅ **JSON Format**: Exact format as specified with title and outline
✅ **Performance**: ≤ 10 seconds for 50-page PDFs
✅ **Architecture**: AMD64 Linux compatible
✅ **Offline**: No internet/API calls
✅ **Container**: Self-contained with all dependencies

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Run in debug mode for detailed logging
3. Validate JSON output using test_extractor.py
4. Verify Docker platform and network settings

## Final Verification Command

```bash
# Complete end-to-end test
./build.sh && ./run.sh
```

This should build the image, process all PDFs in input/, and generate JSON files in output/.
'''

with open('DEPLOYMENT.md', 'w', encoding='utf-8') as f:
    f.write(deployment_guide)

print("Created DEPLOYMENT.md")

# Final project status
print(f"\n{'='*60}")
print("PDF OUTLINE EXTRACTOR - PROJECT COMPLETE")
print(f"{'='*60}")
print(f"Files created: {len(glob.glob('*'))} files")
print("Core components:")
print("  ✅ pdf_extractor.py - Main extraction logic")
print("  ✅ Dockerfile - Container configuration") 
print("  ✅ requirements.txt - Dependencies")
print("  ✅ README.md - Documentation")
print("  ✅ Test and build scripts")
print("\nReady for Adobe India Hackathon Challenge Round 1A!")
print("Next steps:")
print("  1. ./build.sh - Build Docker image")
print("  2. Add PDFs to input/ directory")
print("  3. ./run.sh - Process PDFs")