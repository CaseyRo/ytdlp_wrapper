# package-management Specification

## Purpose
TBD - created by archiving change add-uv-setup. Update Purpose after archive.
## Requirements
### Requirement: Project Dependency Declaration
The project SHALL define dependencies in a pyproject.toml file following Python packaging standards.

#### Scenario: Dependency file exists
- **GIVEN** a user clones or downloads the project
- **WHEN** they review the project root
- **THEN** they find a pyproject.toml file
- **AND** it contains all required dependencies (yt-dlp, python-dotenv)

#### Scenario: Python version specified
- **GIVEN** a user wants to know Python requirements
- **WHEN** they check pyproject.toml
- **THEN** they see the minimum Python version requirement
- **AND** they can verify their Python version is compatible

### Requirement: UV Installation Instructions
The README SHALL provide clear instructions for installing dependencies using UV as the primary method.

#### Scenario: UV installation method documented
- **GIVEN** a user wants to use UV for setup
- **WHEN** they read the installation section
- **THEN** they find instructions to install UV prominently featured first
- **AND** they see platform-specific installation commands (macOS, Linux, Windows)

#### Scenario: UV dependency installation
- **GIVEN** a user has UV installed
- **WHEN** they follow the UV setup instructions
- **THEN** they can install all Python dependencies with a single command
- **AND** the process is faster than traditional pip installation

#### Scenario: UV quick-start workflow
- **GIVEN** a new user wants the fastest setup
- **WHEN** they follow the UV quick-start guide
- **THEN** they can go from zero to running in minimal steps (3-4 commands max)
- **AND** the workflow is clearly documented with example commands

### Requirement: Simplified Documentation
The README SHALL be reorganized to reduce complexity and prioritize the UV workflow.

#### Scenario: Prerequisites simplified
- **GIVEN** a user reads the prerequisites section
- **WHEN** they review what they need to install
- **THEN** they see UV and ffmpeg as primary requirements
- **AND** individual Python packages (yt-dlp, python-dotenv) are not listed separately
- **AND** they understand UV handles Python dependency management

#### Scenario: Installation section streamlined
- **GIVEN** a user follows installation instructions
- **WHEN** they read the installation section
- **THEN** they see UV method first and most prominently
- **AND** alternative pip method is available but clearly marked as alternative
- **AND** the overall documentation flow is simpler than before

#### Scenario: Usage examples with UV
- **GIVEN** a user wants to run the script
- **WHEN** they review usage examples
- **THEN** they see UV run commands as the primary examples
- **AND** they understand the UV workflow (uv sync, uv run)

### Requirement: Backward Compatibility
The project SHALL maintain support for traditional pip-based installation.

#### Scenario: Pip installation still works
- **GIVEN** a user prefers pip over UV
- **WHEN** they follow the pip installation instructions
- **THEN** they can successfully install dependencies
- **AND** the script functions identically to UV-installed version

#### Scenario: Multiple installation methods documented
- **GIVEN** a user reads the README
- **WHEN** they review installation options
- **THEN** they see both UV (recommended) and pip methods
- **AND** they can choose the method that suits their workflow

### Requirement: UV Run Commands
The documentation SHALL show how to use UV for running the script directly.

#### Scenario: Running script with UV
- **GIVEN** a user has installed dependencies via UV
- **WHEN** they want to run the download script
- **THEN** they can use UV run commands
- **AND** they understand the benefits (automatic environment management)

#### Scenario: UV sync for dependency updates
- **GIVEN** dependencies are updated in pyproject.toml
- **WHEN** a user runs UV sync
- **THEN** their local environment updates to match
- **AND** they understand this keeps dependencies in sync

