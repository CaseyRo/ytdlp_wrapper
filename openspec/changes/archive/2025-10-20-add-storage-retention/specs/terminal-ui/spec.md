# terminal-ui Specification Deltas

## MODIFIED Requirements

### Requirement: Configuration Summary Display

The application SHALL display configuration settings in a formatted panel at startup.

#### Scenario: Startup configuration panel
- **GIVEN** the application starts
- **WHEN** initial output is displayed
- **THEN** a formatted panel shows active configuration
- **AND** the panel includes: playlist URL, output directory, archive file, cookie file status
- **AND** webhook configuration is shown if enabled
- **AND** retention policy is shown if configured (e.g., "Retention: 30 days")

#### Scenario: Configuration visibility
- **GIVEN** a user runs the script
- **WHEN** they view the startup output
- **THEN** they can quickly verify their settings are correct
- **AND** they can see which optional features are enabled (webhooks, retention, etc.)

#### Scenario: Retention status display
- **GIVEN** `RETENTION_DAYS` is set
- **WHEN** the configuration panel is displayed
- **THEN** it shows "Retention: ✓ X days" where X is the configured value
- **AND** when not set, it shows "Retention: ✗ Disabled"

## ADDED Requirements

### Requirement: Cleanup Status Messages

The application SHALL display cleanup operation status with Rich formatting.

#### Scenario: Cleanup with deleted files
- **GIVEN** cleanup deletes one or more files
- **WHEN** cleanup completes
- **THEN** a message displays count of deleted files
- **AND** the message uses yellow/orange color (informational)
- **AND** includes space freed in human-readable format (e.g., "Freed 2.3 GB")
- **AND** includes appropriate icon (🗑️ or 📦)

#### Scenario: Cleanup with no deletions
- **GIVEN** all files are within retention period
- **WHEN** cleanup runs
- **THEN** a brief message confirms "No files to clean up"
- **AND** uses dim/muted styling (not a warning)

#### Scenario: Cleanup disabled
- **GIVEN** retention is not configured
- **WHEN** the script runs
- **THEN** no cleanup status messages are displayed
- **AND** the download process starts immediately

#### Scenario: Cleanup errors displayed
- **GIVEN** some files fail to delete due to permissions
- **WHEN** cleanup encounters errors
- **THEN** warning messages in yellow show failed deletions
- **AND** errors include file path and reason
- **AND** messages clarify that downloads will continue

### Requirement: Cleanup Statistics in Summary

The application SHALL include cleanup statistics in the completion summary.

#### Scenario: Summary includes cleanup stats
- **GIVEN** cleanup deleted files during the session
- **WHEN** the completion summary is displayed
- **THEN** summary panel includes cleanup statistics
- **AND** shows count of files cleaned and space freed
- **AND** cleanup stats appear before download stats in summary

#### Scenario: Summary without cleanup
- **GIVEN** no cleanup occurred (disabled or nothing to delete)
- **WHEN** the completion summary is displayed
- **THEN** cleanup statistics are omitted
- **AND** summary shows only download statistics

