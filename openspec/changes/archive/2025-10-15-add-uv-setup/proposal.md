# Add UV Setup Method

## Why
UV is a modern, extremely fast Python package installer and resolver that simplifies dependency management. Currently, users must manually install Python, pip, yt-dlp, python-dotenv, and ffmpeg separately. Adding UV support will provide a streamlined, one-command setup experience that's significantly faster than traditional pip installations.

## What Changes
- Create `pyproject.toml` with project metadata and dependencies (yt-dlp, python-dotenv)
- Reorganize and simplify README.md to prioritize UV as the primary installation method
- Replace multi-step pip installation with simple UV quick-start
- Move manual pip/dependency installation to "Alternative Installation" section
- Add UV run commands and workflow examples
- Streamline prerequisites section (UV handles Python dependencies automatically)
- Keep backward compatibility documentation for users who prefer pip

## Impact
- **Affected specs**: package-management (new capability)
- **Affected code**: No changes to download.py
- **User benefit**: Faster, simpler installation process (UV is 10-100x faster than pip)
- **Breaking changes**: None (pip installation still supported)

