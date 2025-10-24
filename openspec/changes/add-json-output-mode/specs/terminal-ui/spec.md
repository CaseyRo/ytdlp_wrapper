## ADDED Requirements

### Requirement: JSON Output Mode
The application SHALL provide a JSON output mode that suppresses all Rich terminal formatting and outputs only structured JSON data.

#### Scenario: JSON mode via command-line flag
- **GIVEN** a user runs the application with --json-output flag
- **WHEN** the application executes
- **THEN** all Rich formatting is suppressed
- **AND** only raw JSON is output to stdout
- **AND** no progress bars, panels, or colored text is displayed

#### Scenario: JSON mode via environment variable
- **GIVEN** JSON_OUTPUT environment variable is set to "true"
- **WHEN** the application executes
- **THEN** JSON output mode is enabled
- **AND** behavior is identical to --json-output flag

#### Scenario: JSON output structure
- **GIVEN** JSON output mode is enabled
- **WHEN** the application completes
- **THEN** JSON contains: downloaded, skipped, errors, summary statistics
- **AND** JSON is valid and parseable
- **AND** JSON includes metadata for each video (id, title, upload_date, etc.)

#### Scenario: JSON output with successful downloads
- **GIVEN** JSON mode is enabled and videos are downloaded
- **WHEN** the application completes
- **THEN** JSON includes downloaded array with video metadata
- **AND** each downloaded video includes: video_id, title, upload_date, download_date, filepath
- **AND** summary includes count of downloaded videos

#### Scenario: JSON output with skipped videos
- **GIVEN** JSON mode is enabled and some videos are already downloaded
- **WHEN** the application completes
- **THEN** JSON includes skipped array with video metadata
- **AND** each skipped video includes: video_id, title, reason
- **AND** summary includes count of skipped videos

#### Scenario: JSON output with download errors
- **GIVEN** JSON mode is enabled and some downloads fail
- **WHEN** the application completes
- **THEN** JSON includes errors array with error details
- **AND** each error includes: video_id, title, error message
- **AND** summary includes count of errors

#### Scenario: JSON output with cleanup operations
- **GIVEN** JSON mode is enabled and retention cleanup occurs
- **WHEN** the application completes
- **THEN** JSON includes cleanup statistics
- **AND** cleanup stats include: files_deleted, space_freed_bytes
- **AND** summary includes cleanup information

## MODIFIED Requirements

### Requirement: Rich Library Integration
The application SHALL use the Rich library for enhanced terminal output and formatting, except when JSON output mode is enabled.

#### Scenario: Rich console initialization with JSON mode
- **GIVEN** JSON output mode is enabled
- **WHEN** Rich console is initialized
- **THEN** console is configured to suppress all formatting
- **AND** no Rich components are used for output

#### Scenario: Rich console initialization without JSON mode
- **GIVEN** JSON output mode is disabled
- **WHEN** Rich console is initialized
- **THEN** console works normally with full Rich formatting
- **AND** all existing Rich features remain available

### Requirement: Configuration Summary Display
The application SHALL display configuration settings in a formatted panel at startup, except when JSON output mode is enabled.

#### Scenario: Configuration display in JSON mode
- **GIVEN** JSON output mode is enabled
- **WHEN** the application starts
- **THEN** no configuration panel is displayed
- **AND** configuration information is included in final JSON output

#### Scenario: Configuration display in normal mode
- **GIVEN** JSON output mode is disabled
- **WHEN** the application starts
- **THEN** configuration panel is displayed normally
- **AND** existing Rich formatting is preserved

### Requirement: Summary Statistics
The application SHALL display summary statistics after completion, except when JSON output mode is enabled.

#### Scenario: Summary display in JSON mode
- **GIVEN** JSON output mode is enabled
- **WHEN** the application completes
- **THEN** no Rich summary panel is displayed
- **AND** summary statistics are included in JSON output
- **AND** JSON includes: total_videos, downloaded_count, skipped_count, error_count, duration_seconds

#### Scenario: Summary display in normal mode
- **GIVEN** JSON output mode is disabled
- **WHEN** the application completes
- **THEN** Rich summary panel is displayed normally
- **AND** existing Rich formatting is preserved
