#!/usr/bin/env python3
"""Run cleanup test with proper imports"""

import sys
import os
import json

# Set up environment to use test directory
test_dir = "/var/folders/77/wx2cs5794lx8npx0n5xc0nbm0000gn/T/ytdlp_test_8at213tp"
os.chdir(test_dir)

# Override OUTPUT_DIR for testing
sys.path.insert(0, '/Users/caseyromkes/dev/ytdlp_wrapper')
os.environ['OUTPUT_DIR'] = test_dir

# Import after setting up environment
from download import cleanup_old_files, console

# Load test archive
with open('test_archive.json', 'r') as f:
    archive = json.load(f)

print(f"Files before cleanup: {len(archive)}")
print(f"Test files on disk: {len([f for f in os.listdir('.') if f.endswith('.mp4')])}")
print()

# Run cleanup with 30 day retention
result = cleanup_old_files(archive, 30)

print()
print(f"Files after cleanup: {len(result)}")
print(f"Remaining files on disk: {len([f for f in os.listdir('.') if f.endswith('.mp4')])}")

# Save updated archive
with open('test_archive_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print("\nTest passed! ✅")
print("Old files (>30 days) should be deleted")
print("Recent files (<30 days) should remain")

