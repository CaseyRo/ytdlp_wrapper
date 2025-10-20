# configuration-management Specification Deltas

## ADDED Requirements

### Requirement: Storage Retention Configuration

The application SHALL support configurable storage retention via the `RETENTION_DAYS` environment variable.

#### Scenario: Retention days in .env file
- **GIVEN** a user sets `RETENTION_DAYS=30` in their .env file
- **WHEN** they run the script
- **THEN** the application loads the retention policy
- **AND** files older than 30 days are automatically deleted

#### Scenario: Retention disabled by default
- **GIVEN** `RETENTION_DAYS` is not set
- **WHEN** the user runs the script
- **THEN** no automatic cleanup occurs
- **AND** all downloaded files are retained indefinitely

#### Scenario: Retention override via environment variable
- **GIVEN** .env has `RETENTION_DAYS=30`
- **AND** user runs with `RETENTION_DAYS=7 uv run python download.py`
- **WHEN** the script starts
- **THEN** the 7-day retention policy is used (environment variable takes precedence)
- **AND** this allows temporary testing of different retention periods

#### Scenario: Retention documented in .env.example
- **GIVEN** a user opens .env.example
- **WHEN** they review configuration options
- **THEN** they see `RETENTION_DAYS` with explanation
- **AND** they understand it's optional and defaults to disabled
- **AND** they see example values (e.g., "30" for 30 days)

