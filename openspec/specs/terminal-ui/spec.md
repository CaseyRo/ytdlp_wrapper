# terminal-ui Specification

## Purpose
TBD - created by archiving change add-rich-terminal-output. Update Purpose after archive.
## Requirements
### Requirement: Rich Library Integration
The application SHALL use the Rich library for enhanced terminal output and formatting.

#### Scenario: Rich dependency installed
- **GIVEN** a user installs the application
- **WHEN** they run uv sync
- **THEN** the rich library is installed automatically
- **AND** the application can import Rich components

#### Scenario: Rich console initialization
- **GIVEN** the application starts
- **WHEN** Rich console is initialized
- **THEN** a global console instance is available for all output
- **AND** the console respects terminal capabilities (color support, width)

### Requirement: Color-Coded Status Messages
The application SHALL use color-coding to indicate message types and status.

#### Scenario: Success messages in green
- **GIVEN** a video is successfully downloaded
- **WHEN** the completion message is displayed
- **THEN** the message appears in green color
- **AND** includes a success icon (✓ or ✅)

#### Scenario: Warning messages in yellow
- **GIVEN** a webhook fails or non-critical issue occurs
- **WHEN** the warning is displayed
- **THEN** the message appears in yellow/orange color
- **AND** includes a warning icon (⚠)

#### Scenario: Error messages in red
- **GIVEN** a critical error occurs
- **WHEN** the error is displayed
- **THEN** the message appears in red color
- **AND** includes an error icon (✗ or ❌)
- **AND** the message is clearly distinguishable from other output

#### Scenario: Info messages in blue/cyan
- **GIVEN** general information is displayed
- **WHEN** the info message appears
- **THEN** it uses blue or cyan color
- **AND** maintains good readability

### Requirement: Progress Tracking
The application SHALL display progress bars and live updates during operations.

#### Scenario: Playlist extraction progress
- **GIVEN** the application is fetching playlist information
- **WHEN** extraction is in progress
- **THEN** a progress indicator or spinner is displayed
- **AND** the user knows the application is working

#### Scenario: Download progress bar
- **GIVEN** a video is being downloaded
- **WHEN** download is in progress
- **THEN** a progress bar shows percentage complete
- **AND** download speed and ETA are displayed
- **AND** the progress bar updates in real-time

#### Scenario: Multiple downloads tracking
- **GIVEN** multiple videos are queued for download
- **WHEN** downloads are processing
- **THEN** the current video and total progress are visible
- **AND** skipped videos are clearly indicated

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

### Requirement: Summary Statistics
The application SHALL display summary statistics after completion.

#### Scenario: Completion summary panel
- **GIVEN** the download process completes
- **WHEN** the final summary is displayed
- **THEN** a formatted panel shows statistics
- **AND** statistics include: total videos processed, new downloads, skipped videos, failed downloads
- **AND** total time elapsed is shown

#### Scenario: Downloaded videos table
- **GIVEN** videos were downloaded in this session
- **WHEN** the summary is displayed
- **THEN** a formatted table lists downloaded videos
- **AND** table includes: video ID, title, upload date, file size (if available)

### Requirement: Visual Hierarchy
The application SHALL use Rich formatting to create clear visual hierarchy and organization.

#### Scenario: Panel usage for sections
- **GIVEN** the application displays different types of information
- **WHEN** output is rendered
- **THEN** panels are used to group related information
- **AND** panels have clear titles and borders
- **AND** panels improve readability and scannability

#### Scenario: Table formatting for lists
- **GIVEN** multiple items need to be displayed (videos, errors, etc.)
- **WHEN** a list is shown
- **THEN** Rich tables are used with proper columns
- **AND** tables have headers and alignment
- **AND** tables adapt to terminal width

#### Scenario: Emoji and icon usage
- **GIVEN** status messages are displayed
- **WHEN** icons enhance clarity
- **THEN** appropriate emoji/icons are used (✓ ✗ ⚠ 📹 📁 🔗)
- **AND** icons are consistent throughout the application
- **AND** fallback text exists for terminals without emoji support

### Requirement: Webhook Status Display
The application SHALL format webhook-related messages with Rich styling.

#### Scenario: Webhook success indication
- **GIVEN** a webhook notification is sent successfully
- **WHEN** the success message is displayed
- **THEN** it uses green color with success icon
- **AND** includes the video title in the message

#### Scenario: Webhook failure indication
- **GIVEN** a webhook fails to send
- **WHEN** the error is displayed
- **THEN** it uses yellow/orange warning color
- **AND** clearly indicates the failure won't stop downloads
- **AND** provides brief error description

### Requirement: Terminal Compatibility
The application SHALL work correctly across different terminal environments.

#### Scenario: Color support detection
- **GIVEN** the application runs in a terminal
- **WHEN** Rich initializes
- **THEN** terminal color capabilities are detected
- **AND** output degrades gracefully on terminals without color support

#### Scenario: Width adaptation
- **GIVEN** the terminal has a specific width
- **WHEN** Rich content is displayed
- **THEN** panels and tables adapt to terminal width
- **AND** content remains readable in narrow terminals (80 chars)

#### Scenario: Non-TTY environments
- **GIVEN** the application runs in a non-interactive environment (cron, CI/CD)
- **WHEN** output is generated
- **THEN** Rich detects non-TTY and adjusts output appropriately
- **AND** ANSI codes are stripped if output is redirected to a file

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

