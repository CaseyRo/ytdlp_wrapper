#!/usr/bin/env python3
"""
Simple test script to verify retention cleanup logic without downloading videos.
"""

import json
import os
import datetime
import tempfile
import shutil

# Create test directory
test_dir = tempfile.mkdtemp(prefix="ytdlp_test_")
print(f"Test directory: {test_dir}")

# Create test archive with old and new files
archive = {
    "old_video_1": {
        "title": "Old Video 1",
        "upload_date": "20240915",
        "download_date": (datetime.datetime.utcnow() - datetime.timedelta(days=45)).isoformat() + "Z",
        "filepath": os.path.join(test_dir, "old_video_1.mp4")
    },
    "old_video_2": {
        "title": "Old Video 2",
        "upload_date": "20240916",
        "download_date": (datetime.datetime.utcnow() - datetime.timedelta(days=35)).isoformat() + "Z",
        "filepath": os.path.join(test_dir, "old_video_2.mp4")
    },
    "recent_video_1": {
        "title": "Recent Video 1",
        "upload_date": "20241015",
        "download_date": (datetime.datetime.utcnow() - datetime.timedelta(days=10)).isoformat() + "Z",
        "filepath": os.path.join(test_dir, "recent_video_1.mp4")
    },
    "recent_video_2": {
        "title": "Recent Video 2",
        "upload_date": "20241016",
        "download_date": (datetime.datetime.utcnow() - datetime.timedelta(days=5)).isoformat() + "Z",
        "filepath": os.path.join(test_dir, "recent_video_2.mp4")
    }
}

# Create dummy video files
print("\nCreating test files...")
for video_id, metadata in archive.items():
    filepath = metadata["filepath"]
    with open(filepath, "wb") as f:
        # Write dummy data (1 MB per file)
        f.write(b"0" * (1024 * 1024))
    print(f"  Created: {os.path.basename(filepath)}")

print(f"\nTotal files created: {len(archive)}")
print(f"Old files (>30 days): 2")
print(f"Recent files (<30 days): 2")

# Save archive
archive_path = os.path.join(test_dir, "test_archive.json")
with open(archive_path, "w") as f:
    json.dump(archive, f, indent=2)

print(f"\nArchive saved to: {archive_path}")
print("\nTo test cleanup, run:")
print(f"  cd {test_dir}")
print(f"  python3 -c \"import sys; sys.path.insert(0, '{os.getcwd()}'); from download import cleanup_old_files; import json; archive = json.load(open('test_archive.json')); result = cleanup_old_files(archive, 30); json.dump(result, open('test_archive.json', 'w'), indent=2)\"")
print(f"\nOr test the logic manually with retention_days=30")
print(f"\nCleanup test directory when done:")
print(f"  rm -rf {test_dir}")

