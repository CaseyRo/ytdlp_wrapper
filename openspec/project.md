# Project Context

## Purpose
A lightweight Python wrapper around yt-dlp for downloading YouTube Watch Later playlists with intelligent archiving and deduplication. The tool maintains a JSON archive to prevent re-downloading videos, organizes files by upload date, and handles missing metadata gracefully.

## Tech Stack
- **Python 3** - Primary language
- **yt-dlp** - Core video download library
- **JSON** - State/archive management
- No frameworks - intentionally simple single-file design

## Project Conventions

### Code Style
- **Naming**: Snake_case for variables/functions (Python PEP 8 standard)
- **Constants**: SCREAMING_SNAKE_CASE for environment-configurable values
- **Functions**: Descriptive verb-led names (`load_archive`, `save_archive`, `run_download`)
- **Comments**: Inline comments for non-obvious logic, docstrings for complex functions
- **Encoding**: UTF-8 with `ensure_ascii=False` for international characters in video titles
- **Line length**: Reasonable limit (~100 chars), prioritize readability

### Architecture Patterns
- **Simplicity First**: Single-file script until proven insufficient
- **Atomic Operations**: Use temp files + `os.replace()` for safe archive updates
- **State Management**: JSON-based archive (`video_id` -> metadata) separate from yt-dlp's built-in archive
- **Configuration**: Environment variables with sensible defaults
- **Error Handling**: Graceful fallbacks (e.g., missing upload dates → download timestamp)
- **Hooks**: yt-dlp progress hooks for custom archive tracking
- **Idempotency**: Skip already-downloaded videos by checking JSON archive before download

### Testing Strategy
- Manual testing initially (script is simple enough)
- If complexity grows: pytest for unit tests on archive logic
- Test with small playlists first
- Verify: deduplication, fallback renaming, archive integrity after interruptions

### Git Workflow
- **Branching**: Feature branches for new capabilities (`feature/add-quality-selection`)
- **Commits**: Descriptive messages following conventional commits where useful
- **Main branch**: Should always be runnable
- **No force pushes** to main

## Domain Context
- **YouTube Watch Later**: Special playlist (list=WL) requires authentication via cookies
- **Upload Date Fallback**: Some videos lack upload_date metadata; we use download timestamp as fallback
- **File Naming**: `YYYYMMDD Title [video_id].ext` for chronological sorting
- **Archive vs Download**: JSON archive tracks metadata; separate from yt-dlp's download archive
- **Merge Formats**: Best video + best audio merged to mp4 by default

## Important Constraints
- **YouTube API**: Not used (relies on yt-dlp's extraction)
- **Authentication**: Requires cookie file for private Watch Later playlists
- **Disk Space**: No automatic cleanup; user manages storage
- **Rate Limiting**: Respect YouTube's limits (yt-dlp handles this)
- **Network**: Downloads can be large; no built-in retry logic beyond yt-dlp's defaults

## External Dependencies
- **yt-dlp**: Core dependency (pip install yt-dlp)
- **ffmpeg**: Required by yt-dlp for video+audio merging
- **YouTube**: External service (availability dependent on YouTube)
