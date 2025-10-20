# Implementation Tasks

## 1. Configuration
- [x] 1.1 Add `RETENTION_DAYS` environment variable to download.py (default: None/disabled)
- [x] 1.2 Update `.env.example` with `RETENTION_DAYS` documentation
- [x] 1.3 Add retention configuration to show_config_summary() output

## 2. Core Cleanup Logic
- [x] 2.1 Create `cleanup_old_files()` function that accepts archive and retention days
- [x] 2.2 Calculate cutoff date based on current time and retention days
- [x] 2.3 Filter archive entries by download_date vs cutoff
- [x] 2.4 Delete files from filesystem (skip if missing, log errors)
- [x] 2.5 Remove entries from archive JSON
- [x] 2.6 Track cleanup statistics (files deleted, space freed)

## 3. Integration
- [x] 3.1 Call cleanup function at start of run_download() (before downloading)
- [x] 3.2 Pass retention configuration to cleanup function
- [x] 3.3 Update archive after cleanup

## 4. Terminal UI
- [x] 4.1 Display cleanup status message when retention is enabled
- [x] 4.2 Show count of files deleted and space freed (if any)
- [x] 4.3 Add cleanup stats to completion summary

## 5. Documentation
- [x] 5.1 Update README.md Configuration Options table with RETENTION_DAYS
- [x] 5.2 Add "Storage Management" section to README explaining retention
- [x] 5.3 Add FAQ entry about retention behavior
- [x] 5.4 Document what happens to archive when files are deleted

## 6. Testing
- [x] 6.1 Test with RETENTION_DAYS unset (cleanup disabled)
- [x] 6.2 Test with RETENTION_DAYS=7 (cleanup old files)
- [x] 6.3 Test with missing files (already deleted manually)
- [x] 6.4 Test archive JSON stays consistent after cleanup
- [x] 6.5 Verify download_date parsing handles ISO format correctly

