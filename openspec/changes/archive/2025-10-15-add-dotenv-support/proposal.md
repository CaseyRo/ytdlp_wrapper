# Add .env File Support

## Why
Currently, users must set environment variables manually each time they run the script, which is cumbersome and error-prone. Adding support for a `.env` file will improve user experience by allowing persistent configuration storage in a single file.

## What Changes
- Add python-dotenv dependency for .env file loading
- Modify download.py to automatically load configuration from .env file if present
- Create .env.example template file with all configuration options documented
- Update README.md to document .env file usage
- Add .env to .gitignore (if not present) to prevent accidental credential commits

## Impact
- **Affected specs**: configuration-management (new capability)
- **Affected code**: download.py (add dotenv loading before config reading)
- **User benefit**: Easier configuration management, no need to set env vars manually
- **Breaking changes**: None (falls back to environment variables if .env not present)

