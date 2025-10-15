# Configuration Management Specification

## ADDED Requirements

### Requirement: .env File Loading
The application SHALL support loading configuration from a .env file in the project root.

#### Scenario: .env file present
- **GIVEN** a user creates a .env file with configuration values
- **WHEN** they run the script
- **THEN** the application loads configuration from the .env file
- **AND** they don't need to set environment variables manually

#### Scenario: .env file missing
- **GIVEN** no .env file exists
- **WHEN** the user runs the script
- **THEN** the application falls back to reading environment variables
- **AND** the application functions normally with defaults

#### Scenario: Environment variables override .env
- **GIVEN** a user has both .env file and environment variables set
- **WHEN** they run the script
- **THEN** environment variables take precedence over .env file values
- **AND** this allows temporary overrides without modifying .env

### Requirement: Example Configuration File
The project SHALL provide a .env.example file as a template.

#### Scenario: New user setup
- **GIVEN** a new user wants to configure the application
- **WHEN** they review the project files
- **THEN** they find a .env.example file with all configuration options
- **AND** each option has a helpful comment explaining its purpose

#### Scenario: Creating user configuration
- **GIVEN** a user has .env.example file
- **WHEN** they copy it to .env and fill in their values
- **THEN** the application uses their configuration
- **AND** they understand what each setting does

### Requirement: Credential Security
The project SHALL prevent accidental commits of .env files containing credentials.

#### Scenario: Git ignore configuration
- **GIVEN** the project uses git
- **WHEN** a user creates a .env file
- **THEN** the .gitignore file prevents .env from being committed
- **AND** credentials remain secure

#### Scenario: Template file safety
- **GIVEN** the .env.example file exists
- **WHEN** users commit changes
- **THEN** .env.example is committed (no secrets)
- **AND** .env with actual secrets is ignored

### Requirement: Configuration Documentation
The README SHALL document both environment variable and .env file configuration methods.

#### Scenario: Understanding configuration options
- **GIVEN** a user reads the README
- **WHEN** they review the configuration section
- **THEN** they see instructions for both environment variables and .env files
- **AND** they understand .env is the recommended method for persistent config

#### Scenario: python-dotenv installation
- **GIVEN** a user wants to use .env files
- **WHEN** they follow the installation instructions
- **THEN** they can install python-dotenv
- **AND** they understand it's required for .env file support

