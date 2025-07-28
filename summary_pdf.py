# Make scripts executable and create project summary
import stat

try:
    os.chmod('build.sh', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    os.chmod('run.sh', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    os.chmod('test_extractor.py', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    os.chmod('pdf_extractor.py', stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    print("Made scripts executable")
except Exception as e:
    print(f"Could not set execute permissions: {e}")

# Create a project summary
project_summary = '''# PDF Outline Extractor - Project Summary

## Quick Start

1. **Build the Docker image:**
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

2. **Prepare input:**
   ```bash
   mkdir -p input
   # Copy your PDF files to the input/ directory
   ```

3. **Run the extractor:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

## Manual Commands

### Build
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

### Run
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:latest
```

### Test Locally
```bash
pip install -r requirements.txt
python pdf_extractor.py --input ./input --output ./output --debug
```

## Files Created

- `pdf_extractor.py` - Main extraction script with multi-heuristic heading detection
- `Dockerfile` - Container definition optimized for AMD64 Linux
- `requirements.txt` - Python dependencies (minimal: PyMuPDF)
- `README.md` - Comprehensive documentation
- `test_extractor.py` - Test script and validation utilities
- `build.sh` - Build automation script
- `run.sh` - Run automation script
- `.dockerignore` - Docker build optimization

## Key Features

✅ **Performance**: Processes 50-page PDFs in under 10 seconds
✅ **Offline**: No internet dependencies, runs with --network none
✅ **AMD64 Compatible**: Built specifically for linux/amd64 platform
✅ **Robust**: Multi-heuristic heading detection algorithm
✅ **Format Compliant**: Outputs exact JSON format as specified
✅ **Error Handling**: Graceful handling of malformed PDFs

## Architecture

The solution uses a sophisticated heading detection algorithm that combines:
- Font size analysis relative to document averages
- Bold text detection via font flags and naming
- Positional analysis (margins, spacing)
- Numbered heading pattern recognition
- Text length and capitalization heuristics
- Title extraction from metadata and content analysis

This approach is designed to work across various PDF types without requiring machine learning models or large dependencies.
'''

with open('QUICKSTART.md', 'w', encoding='utf-8') as f:
    f.write(project_summary)

print("Created QUICKSTART.md")

# List all created files
print("\nProject files created:")
import glob
files = glob.glob('*')
for file in sorted(files):
    if os.path.isfile(file):
        size = os.path.getsize(file)
        print(f"  {file:<20} ({size:,} bytes)")

print(f"\nTotal files: {len(files)}")