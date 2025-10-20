# Storage Management Specification

## ADDED Requirements

### Requirement: Time-Based Retention Configuration

The system SHALL support configurable time-based retention via the `RETENTION_DAYS` environment variable.

#### Scenario: Retention disabled by default
- **WHEN** `RETENTION_DAYS` is not set or empty
- **THEN** no automatic cleanup occurs and all downloaded files are retained indefinitely

#### Scenario: Retention enabled with days threshold
- **WHEN** `RETENTION_DAYS` is set to a positive integer (e.g., "30")
- **THEN** the system interprets this as the maximum age in days for downloaded files

#### Scenario: Invalid retention value
- **WHEN** `RETENTION_DAYS` is set to a non-numeric or negative value
- **THEN** the system treats it as disabled and logs a warning

### Requirement: Automatic Cleanup Execution

The system SHALL execute cleanup at the start of each download session when retention is enabled.

#### Scenario: Cleanup runs before downloads
- **WHEN** the download script starts and retention is configured
- **THEN** cleanup executes before fetching the playlist or downloading videos

#### Scenario: No cleanup when disabled
- **WHEN** retention is not configured
- **THEN** the cleanup phase is skipped entirely with no performance impact

### Requirement: Age-Based File Deletion

The system SHALL delete files older than the retention threshold based on the `download_date` timestamp in the archive JSON.

#### Scenario: File within retention period
- **WHEN** a file's download_date is less than RETENTION_DAYS old
- **THEN** the file is retained and its archive entry remains

#### Scenario: File exceeds retention period
- **WHEN** a file's download_date is RETENTION_DAYS or more days old
- **THEN** the file is deleted from the filesystem and its entry is removed from archive JSON

#### Scenario: Missing download_date in archive
- **WHEN** an archive entry lacks a download_date field
- **THEN** the entry is skipped and a warning is logged (file is retained)

### Requirement: Safe Deletion with Error Handling

The system SHALL handle file deletion failures gracefully without interrupting the download process.

#### Scenario: File already deleted manually
- **WHEN** a file marked for cleanup does not exist on filesystem
- **THEN** the system removes the archive entry and logs a warning (not an error)

#### Scenario: File deletion permission error
- **WHEN** a file cannot be deleted due to permissions or locks
- **THEN** the system logs the error, retains the archive entry, and continues cleanup

#### Scenario: Archive JSON corruption
- **WHEN** cleanup encounters invalid JSON or missing fields
- **THEN** the system logs errors and proceeds with download without cleanup

### Requirement: Archive Synchronization

The system SHALL keep the archive JSON synchronized with the filesystem after cleanup operations.

#### Scenario: Successful cleanup updates archive
- **WHEN** files are successfully deleted during cleanup
- **THEN** their corresponding entries are atomically removed from archive JSON

#### Scenario: Partial cleanup completion
- **WHEN** some files are deleted but others fail
- **THEN** only successfully deleted files have their archive entries removed

### Requirement: Cleanup Status Reporting

The system SHALL report cleanup results in the terminal UI with Rich formatting.

#### Scenario: Cleanup with deleted files
- **WHEN** cleanup deletes one or more files
- **THEN** a summary message displays the count of deleted files and space freed

#### Scenario: Cleanup with no files to delete
- **WHEN** all files are within retention period
- **THEN** a brief status message confirms cleanup ran but found nothing to delete

#### Scenario: Retention disabled message
- **WHEN** retention is not configured
- **THEN** the configuration summary shows "Retention: ✗ Disabled"

### Requirement: Storage Calculation

The system SHALL calculate and display storage space freed during cleanup.

#### Scenario: Calculate space freed
- **WHEN** files are deleted during cleanup
- **THEN** the system sums file sizes and displays in human-readable format (MB/GB)

#### Scenario: Failed size calculation
- **WHEN** file size cannot be determined before deletion
- **THEN** the system reports count of files deleted without size information

