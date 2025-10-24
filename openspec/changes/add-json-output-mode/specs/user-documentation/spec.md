## ADDED Requirements

### Requirement: JSON Output Documentation
The application SHALL provide documentation for JSON output mode including usage examples.

#### Scenario: README JSON output section
- **GIVEN** a user wants to use JSON output mode
- **WHEN** they read the README.md
- **THEN** they find a dedicated "JSON Output Mode" section
- **AND** the section includes command-line usage examples
- **AND** the section includes environment variable examples
- **AND** the section shows sample JSON output format

#### Scenario: JSON output format documentation
- **GIVEN** a user needs to parse JSON output programmatically
- **WHEN** they read the documentation
- **THEN** they find JSON schema documentation
- **AND** documentation includes field descriptions and data types
- **AND** documentation includes example responses for different scenarios

#### Scenario: Command-line usage examples
- **GIVEN** a user wants to use the command-line interface
- **WHEN** they read the documentation
- **THEN** they find examples for the --json-output flag
- **AND** examples show both normal and JSON output modes
- **AND** examples include environment variable usage

## MODIFIED Requirements

### Requirement: README Structure
The application SHALL maintain a comprehensive README.md with clear sections and examples.

#### Scenario: README includes JSON output section
- **GIVEN** a user opens the README.md
- **WHEN** they look for output mode information
- **THEN** they find a dedicated "JSON Output Mode" section
- **AND** the section is clearly marked and easy to find
- **AND** the section includes practical examples
