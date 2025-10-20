# Storage Retention Proposal

## Why

Users downloading large Watch Later playlists can quickly fill up disk space with old archived videos. Without automatic cleanup, storage grows unbounded requiring manual intervention to delete old files and maintain the archive JSON.

## What Changes

- Add configurable time-based retention policy via `RETENTION_DAYS` environment variable
- Automatic cleanup runs at start of each download session
- Delete videos older than retention threshold based on `download_date` in archive
- Remove corresponding entries from archive JSON automatically
- Display cleanup summary in terminal UI with files removed and space freed
- Safe deletion with proper error handling (skip if file missing, log failures)

## Impact

- **Affected specs**:
  - `storage-management` (NEW capability)
  - `configuration-management` (MODIFIED - adds new env variable)
  - `terminal-ui` (MODIFIED - adds cleanup status messages)

- **Affected code**:
  - `download.py` - Add cleanup function, integrate with run_download flow
  - `.env.example` - Document new `RETENTION_DAYS` variable
  - `README.md` - Document retention feature in configuration section

- **User Impact**:
  - **Opt-in**: Retention is disabled by default (no breaking changes)
  - When enabled, automatically manages disk space
  - Archive JSON stays in sync with filesystem

