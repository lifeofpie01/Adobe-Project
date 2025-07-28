# Create a test script to validate the solution
test_script = '''#!/usr/bin/env python3
"""
Test script for PDF Outline Extractor
This script validates the functionality and creates sample test cases
"""

import json
import os
import sys
import tempfile
from pathlib import Path

def create_sample_json_output():
    """Create sample expected JSON output for testing"""
    sample_output = {
        "title": "Understanding Artificial Intelligence",
        "outline": [
            {"level": "H1", "text": "Introduction", "page": 1},
            {"level": "H2", "text": "What is AI?", "page": 2},
            {"level": "H3", "text": "Machine Learning", "page": 3},
            {"level": "H3", "text": "Deep Learning", "page": 4},
            {"level": "H2", "text": "AI Applications", "page": 5},
            {"level": "H3", "text": "Natural Language Processing", "page": 6},
            {"level": "H3", "text": "Computer Vision", "page": 7},
            {"level": "H1", "text": "Future of AI", "page": 8},
            {"level": "H2", "text": "Challenges", "page": 9},
            {"level": "H2", "text": "Opportunities", "page": 10}
        ]
    }
    
    with open('sample_output.json', 'w', encoding='utf-8') as f:
        json.dump(sample_output, f, indent=2, ensure_ascii=False)
    
    print("Created sample_output.json")

def validate_json_format(json_file):
    """Validate that the JSON output follows the required format"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required fields
        if 'title' not in data:
            return False, "Missing 'title' field"
        
        if 'outline' not in data:
            return False, "Missing 'outline' field"
        
        if not isinstance(data['outline'], list):
            return False, "'outline' must be a list"
        
        # Validate outline entries
        for i, entry in enumerate(data['outline']):
            if not isinstance(entry, dict):
                return False, f"Outline entry {i} must be a dictionary"
            
            required_fields = ['level', 'text', 'page']
            for field in required_fields:
                if field not in entry:
                    return False, f"Outline entry {i} missing '{field}' field"
            
            # Validate level values
            if entry['level'] not in ['H1', 'H2', 'H3']:
                return False, f"Invalid level '{entry['level']}' in entry {i}"
            
            # Validate page number
            if not isinstance(entry['page'], int) or entry['page'] < 1:
                return False, f"Invalid page number in entry {i}"
        
        return True, "Valid JSON format"
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error validating JSON: {e}"

def run_integration_test():
    """Run a simple integration test"""
    print("Running integration test...")
    
    # Create test directories
    os.makedirs('test_input', exist_ok=True)
    os.makedirs('test_output', exist_ok=True)
    
    # Note: In a real test, we would put actual PDF files in test_input
    print("Test directories created")
    print("To run full test:")
    print("1. Place PDF files in test_input/")
    print("2. Run: python pdf_extractor.py --input test_input --output test_output")
    print("3. Check test_output/ for JSON files")

def main():
    print("PDF Outline Extractor - Test Suite")
    print("=" * 50)
    
    create_sample_json_output()
    
    # Validate sample output
    is_valid, message = validate_json_format('sample_output.json')
    print(f"Sample JSON validation: {message}")
    
    run_integration_test()
    
    print("\\nTest suite completed!")

if __name__ == "__main__":
    main()
'''

with open('test_extractor.py', 'w', encoding='utf-8') as f:
    f.write(test_script)

print("Created test_extractor.py")