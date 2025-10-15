# User Documentation Specification

## ADDED Requirements

### Requirement: Installation Instructions
The README SHALL provide complete installation instructions for all required dependencies.

#### Scenario: New user installation
- **GIVEN** a user with no prior setup
- **WHEN** they follow the installation instructions
- **THEN** they can successfully install Python 3, yt-dlp, and ffmpeg
- **AND** they understand the purpose of each dependency

#### Scenario: Dependency verification
- **GIVEN** a user has completed installation
- **WHEN** they verify their setup
- **THEN** the README provides commands to check installed versions

### Requirement: Configuration Documentation
The README SHALL document all configuration options with clear explanations and examples.

#### Scenario: Environment variable configuration
- **GIVEN** a user wants to customize behavior
- **WHEN** they review the configuration section
- **THEN** they can see all available environment variables (WATCHLATER_URL, OUTPUT_DIR, ARCHIVE_JSON, COOKIES_FILE)
- **AND** they understand the purpose and default value of each

#### Scenario: Cookie file setup
- **GIVEN** a user needs to access private Watch Later playlist
- **WHEN** they follow the cookie setup instructions
- **THEN** they can successfully export cookies from their browser
- **AND** they know how to specify the cookie file path

### Requirement: Usage Examples
The README SHALL provide clear usage examples for common workflows.

#### Scenario: Basic usage
- **GIVEN** a new user wants to download their Watch Later playlist
- **WHEN** they read the basic usage example
- **THEN** they can execute the script with default settings
- **AND** they understand where downloaded files will be saved

#### Scenario: Custom configuration
- **GIVEN** a user wants to customize output location
- **WHEN** they review the examples
- **THEN** they can see how to set environment variables
- **AND** they can run the script with custom settings

#### Scenario: Resume interrupted downloads
- **GIVEN** a user's download was interrupted
- **WHEN** they run the script again
- **THEN** the README explains that already-downloaded videos will be skipped
- **AND** they understand how the archive.json prevents duplicates

### Requirement: Troubleshooting Guide
The README SHALL include a troubleshooting section for common issues.

#### Scenario: Missing ffmpeg error
- **GIVEN** a user encounters an ffmpeg-related error
- **WHEN** they check the troubleshooting section
- **THEN** they find instructions to install or verify ffmpeg

#### Scenario: Authentication failure
- **GIVEN** a user cannot access their Watch Later playlist
- **WHEN** they review troubleshooting
- **THEN** they find guidance on cookie authentication issues
- **AND** they can verify their cookie file is valid

#### Scenario: Permission errors
- **GIVEN** a user encounters file permission issues
- **WHEN** they check troubleshooting
- **THEN** they find guidance on output directory permissions

### Requirement: Output Structure Documentation
The README SHALL explain the file naming convention and archive structure.

#### Scenario: Understanding output files
- **GIVEN** a user has downloaded videos
- **WHEN** they review the output structure documentation
- **THEN** they understand the file naming format (YYYYMMDD Title [video_id].ext)
- **AND** they know why files are named this way (chronological sorting)

#### Scenario: Archive JSON understanding
- **GIVEN** a user sees the archive JSON file
- **WHEN** they review the documentation
- **THEN** they understand its purpose (deduplication)
- **AND** they know what metadata is stored (title, upload_date, download_date, filepath)

### Requirement: Legal and Policy Disclaimer
The README SHALL include a clear legal disclaimer about usage restrictions and terms of service compliance.

#### Scenario: Understanding legal restrictions
- **GIVEN** a user is considering using the tool
- **WHEN** they read the legal disclaimer section
- **THEN** they are informed that downloading videos may violate YouTube's Terms of Service
- **AND** they understand they are responsible for compliance with applicable laws and policies

#### Scenario: Intended use clarification
- **GIVEN** a user reads the documentation
- **WHEN** they review the legal section
- **THEN** they understand the tool is intended for personal archival of their own Watch Later content
- **AND** they are warned against redistributing or commercial use of downloaded content

#### Scenario: Privacy and responsible use
- **GIVEN** a user wants to use the tool responsibly
- **WHEN** they review the privacy and usage guidelines
- **THEN** they understand to only download content they have the right to access
- **AND** they are aware of potential copyright and intellectual property considerations
- **AND** they know the tool stores authentication cookies locally

### Requirement: Terms of Service Reference
The README SHALL reference YouTube's Terms of Service and user responsibilities.

#### Scenario: YouTube ToS awareness
- **GIVEN** a new user reads the README
- **WHEN** they encounter the Terms of Service section
- **THEN** they are directed to YouTube's official Terms of Service
- **AND** they understand that use of this tool is at their own risk
- **AND** they acknowledge their responsibility to comply with YouTube's policies

