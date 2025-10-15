# YouTube Watch Later Downloader

A lightweight Python wrapper around yt-dlp for downloading and archiving your YouTube Watch Later playlist with intelligent deduplication and metadata tracking.

## ⚠️ Legal Disclaimer & Terms of Service

**IMPORTANT: Please read before using this tool.**

This tool is provided for **educational and personal archival purposes only**. By using this tool, you acknowledge and agree that:

- Downloading videos from YouTube may violate [YouTube's Terms of Service](https://www.youtube.com/t/terms)
- You are solely responsible for ensuring your use complies with all applicable laws, regulations, and terms of service
- This tool is intended for **personal archival of your own Watch Later content only**
- You must have the legal right to download and store any content you access
- **Do not redistribute, share, or use downloaded content for commercial purposes**
- Respect copyright and intellectual property rights of content creators
- Use of this tool is **at your own risk** - the authors assume no liability for misuse

### Privacy Considerations

- This tool stores your YouTube authentication cookies **locally** on your computer
- No data is transmitted to third parties
- You are responsible for securing your cookie file and downloaded content
- Only download content you have the legal right to access

By proceeding, you accept full responsibility for compliance with YouTube's policies and all applicable laws.

---

## Features

- ✅ **Smart Deduplication** - Automatically skips already-downloaded videos
- 📁 **Organized Storage** - Files named by upload date for chronological sorting
- 📝 **JSON Archive** - Maintains metadata for all downloaded videos
- 🔄 **Resumable** - Interrupt and resume downloads without re-downloading
- 🎥 **High Quality** - Downloads best available video and audio, merged to MP4
- ⚙️ **Configurable** - Customize output directory, playlist URL, and more
- 🎨 **Beautiful Terminal UI** - Rich formatted output with progress bars and color-coded status

## Prerequisites

Before using this tool, you need to install:

1. **[UV](https://docs.astral.sh/uv/)** - Modern Python package installer (handles all Python dependencies)
2. **ffmpeg** - Required for merging video and audio streams

That's it! UV will automatically handle installing Python, yt-dlp, python-dotenv, rich, and all other dependencies.

## Quick Start (Recommended)

Get up and running in 3 simple steps:

### 1. Install UV

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or using package managers:**
```bash
# macOS
brew install uv

# Arch Linux
pacman -S uv

# Cargo
cargo install --git https://github.com/astral-sh/uv uv
```

### 2. Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use [Chocolatey](https://chocolatey.org/):
```bash
choco install ffmpeg
```

### 3. Clone and Setup

```bash
# Clone the repository (or download the files)
git clone https://github.com/CaseyRo/ytdlp_wrapper.git
cd ytdlp_wrapper

# Install all Python dependencies automatically
uv sync

# That's it! You're ready to use the tool.
```

## Configuration

### Quick Configuration with .env File

1. Copy the example configuration:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings:
   ```bash
   nano .env
   ```

3. Set your cookie file path (required for Watch Later):
   ```bash
   # In .env file
   COOKIES_FILE=youtube_cookies.txt
   ```

### Configuration Options

| Variable | Purpose | Default Value |
|----------|---------|---------------|
| `WATCHLATER_URL` | YouTube playlist URL to download | `https://www.youtube.com/playlist?list=WL` |
| `OUTPUT_DIR` | Directory where videos will be saved | `./yt_watchlater` |
| `ARCHIVE_JSON` | Path to JSON archive file | `./yt_watchlater_archive.json` |
| `COOKIES_FILE` | Path to browser cookies file | `None` (must be set for Watch Later) |
| `WEBHOOK_URL` | HTTP endpoint for download notifications | `None` (optional) |
| `WEBHOOK_PORT` | Port for webhook endpoint | `80` |
| `WEBHOOK_SECRET` | Bearer token for webhook authentication | `None` (optional) |

**Configuration priority:** Command-line environment variables > .env file > defaults

### Setting Up Cookies (Required for Watch Later)

Your Watch Later playlist is private and requires authentication. Export your YouTube cookies:

**Method 1: Using a Browser Extension (Recommended)**

1. Install a cookie export extension:
   - Chrome: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Navigate to [YouTube.com](https://www.youtube.com) while logged in
3. Click the extension icon and export cookies
4. Save the file as `youtube_cookies.txt` in the project directory

**Method 2: Using yt-dlp**

```bash
uv run yt-dlp --cookies-from-browser chrome --cookies youtube_cookies.txt --skip-download "https://www.youtube.com/"
```

**⚠️ Security Warning:** Your cookies file contains authentication credentials. Keep it secure and never share it.

### Webhook Notifications (Optional)

Get real-time notifications when videos are downloaded! The downloader can send HTTP POST requests with video metadata to any webhook endpoint.

**Use Cases:**
- Discord/Slack notifications
- Home automation triggers (Home Assistant, Node-RED)
- Custom logging and analytics
- Integration with Zapier, IFTTT, n8n

**Configuration:**

Edit your `.env` file:
```bash
# Basic webhook setup
WEBHOOK_URL=http://192.168.1.100/api/webhook
WEBHOOK_PORT=8080

# With authentication
WEBHOOK_SECRET=your-secret-token-here
```

**JSON Payload Structure:**

Each successful download sends a POST request with this payload:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Introduction to Python",
  "upload_date": "20241015",
  "download_date": "2024-10-15T14:30:00Z",
  "filepath": "./yt_watchlater/20241015 Introduction to Python [dQw4w9WgXcQ].mp4"
}
```

**Headers Sent:**
```
Content-Type: application/json
Authorization: Bearer YOUR_SECRET  (if WEBHOOK_SECRET is set)
```

**Integration Examples:**

**Discord Webhook:**
```bash
# Discord webhooks use HTTPS on port 443
WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN
WEBHOOK_PORT=443
```

Note: For Discord, you'll need a server to transform the payload into Discord's format, or use a service like Zapier.

**Slack Webhook:**
```bash
WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
WEBHOOK_PORT=443
```

**Home Assistant:**
```bash
WEBHOOK_URL=http://homeassistant.local:8123/api/webhook/ytdlp_download
WEBHOOK_PORT=8123
WEBHOOK_SECRET=your-webhook-id
```

**Custom Local Server:**
```bash
# Python Flask example listening on port 5000
WEBHOOK_URL=http://localhost/webhook
WEBHOOK_PORT=5000
```

**Error Handling:**

Webhook failures are logged but **do not interrupt downloads**:
- Network errors → Logged to stderr, download continues
- HTTP errors → Status code logged, download continues
- Timeouts (10s) → Logged, download continues
- If `WEBHOOK_URL` is not set → Webhooks disabled silently

**Testing Your Webhook:**

Use a service like [webhook.site](https://webhook.site) to test:

```bash
# Get a test URL from webhook.site
WEBHOOK_URL=https://webhook.site/your-unique-url
WEBHOOK_PORT=443

# Run a download and check webhook.site for the payload
uv run python download.py
```

## Usage

### Basic Usage

Download your Watch Later playlist:

```bash
# Run with UV (recommended)
uv run python download.py
```

**Terminal Output:**

The downloader features beautiful, color-coded terminal output:
- 📹 Welcome banner with configuration summary
- ✅ Green success messages for completed downloads
- ⏭️ Yellow indicators for skipped videos
- ⚠️ Warning messages for non-critical issues
- 📊 Summary statistics table at completion
- 🔗 Webhook status indicators

All output uses the Rich library for enhanced readability with progress tracking and visual hierarchy.

### Custom Configuration Examples

**Temporary override with environment variables:**
```bash
OUTPUT_DIR="~/Videos/YouTube" uv run python download.py
```

**Download a different playlist:**

Edit `.env`:
```bash
WATCHLATER_URL=https://www.youtube.com/playlist?list=PLxxxxxxx
```

Then run:
```bash
uv run python download.py
```

### Advanced UV Commands

```bash
# Update dependencies to latest versions
uv sync --upgrade

# Run with specific Python version
uv run --python 3.11 python download.py

# Add a new dependency
uv add package-name

# Remove a dependency
uv remove package-name
```

## Output Structure

### File Naming Convention

Downloaded videos are named using this format:

```
YYYYMMDD Title [video_id].ext
```

**Examples:**
- `20241015 Introduction to Python [dQw4w9WgXcQ].mp4`
- `20241014 Machine Learning Basics [abc123xyz].mp4`

**Why this format?**
- Files sort **chronologically** by upload date
- Video ID ensures **uniqueness** even with duplicate titles
- If upload date is unavailable, download timestamp is used instead

### Archive JSON Structure

The archive file (`yt_watchlater_archive.json`) stores metadata for deduplication:

```json
{
  "dQw4w9WgXcQ": {
    "title": "Introduction to Python",
    "upload_date": "20241015",
    "download_date": "2024-10-15T10:30:00Z",
    "filepath": "./yt_watchlater/20241015 Introduction to Python [dQw4w9WgXcQ].mp4"
  }
}
```

**Purpose:**
- Prevents re-downloading videos you already have
- Tracks when videos were downloaded
- Maintains a record of your archive

### Example Output Directory

```
yt_watchlater/
├── 20241015 Introduction to Python [dQw4w9WgXcQ].mp4
├── 20241014 Machine Learning Basics [abc123xyz].mp4
└── 20241013 Web Development Tutorial [xyz789abc].mp4

yt_watchlater_archive.json
```

## How It Works

### Deduplication & Resumability

1. **First Run:**
   - Script fetches your Watch Later playlist
   - Downloads all videos
   - Saves metadata to `archive.json`

2. **Subsequent Runs:**
   - Script checks each video ID against `archive.json`
   - **Skips** videos already downloaded
   - Only downloads **new** videos added to playlist

3. **Interrupted Downloads:**
   - If download is interrupted (network issue, manual stop)
   - Simply run the script again
   - Already-completed videos are automatically skipped
   - Continues from where it left off

**Example output:**
```
Skipping already downloaded: dQw4w9WgXcQ — Introduction to Python
Skipping already downloaded: abc123xyz — Machine Learning Basics
Downloading: xyz789abc — New Video Title
```

## Troubleshooting

### Error: "Unable to extract playlist"

**Cause:** Authentication required for Watch Later playlist.

**Solution:**
1. Export cookies from your browser (see [Setting Up Cookies](#setting-up-cookies-required-for-watch-later))
2. Set `COOKIES_FILE` in your `.env` file:
   ```bash
   COOKIES_FILE=youtube_cookies.txt
   ```

### Error: "ffmpeg not found"

**Cause:** ffmpeg is not installed or not in PATH.

**Solution:**
- **macOS:** `brew install ffmpeg`
- **Ubuntu/Debian:** `sudo apt install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Verify installation: `ffmpeg -version`

### Error: "No module named 'dotenv'" or "No module named 'yt_dlp'"

**Cause:** Dependencies not installed or UV not synced.

**Solution:**
```bash
# Make sure UV is installed
uv --version

# Sync dependencies
uv sync

# Run with UV
uv run python download.py
```

### Videos downloading very slowly

**Cause:** Network throttling or server limitations.

**Solution:**
- This is normal for large files
- yt-dlp respects rate limits automatically
- Be patient - high-quality videos take time

### Cookie file not working / authentication fails

**Cause:** Cookies may be expired or in wrong format.

**Solution:**
1. Re-export fresh cookies while logged into YouTube
2. Ensure cookie file is in Netscape format
3. Verify the file path in `.env` is correct
4. Try the `--cookies-from-browser` method

## Alternative Installation (Without UV)

If you prefer traditional pip-based installation:

### 1. Install Python 3.7+

Download from [python.org](https://www.python.org/downloads/)

### 2. Install Python Dependencies

```bash
pip install yt-dlp python-dotenv
```

### 3. Install ffmpeg

See [ffmpeg installation instructions](#2-install-ffmpeg) above.

### 4. Download the Script

```bash
curl -O https://raw.githubusercontent.com/yourusername/ytdlp_wrapper/main/download.py
chmod +x download.py
```

### 5. Run Directly

```bash
python3 download.py
```

**Note:** UV is recommended for faster installation and better dependency management.

## Advanced Usage

### Scheduling Automatic Downloads

You can set up automatic downloads using cron (Linux/macOS) or Task Scheduler (Windows).

**macOS/Linux cron example:**
```bash
# Edit crontab
crontab -e

# Add line to run daily at 2 AM
0 2 * * * cd /path/to/ytdlp_wrapper && /path/to/uv run python download.py >> download.log 2>&1
```

### Customizing Video Quality

Edit `download.py` and modify the `format` option in `ydl_opts`:

```python
ydl_opts = {
    "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",  # Limit to 1080p
    # ... other options
}
```

### Changing Output Format

Change the `merge_output_format` in `download.py`:

```python
ydl_opts = {
    # ... other options
    "merge_output_format": "mkv",  # Use MKV instead of MP4
}
```

## Project Structure

```
.
├── download.py                    # Main script
├── pyproject.toml                 # UV/Python project configuration
├── .env.example                   # Example configuration
├── .env                           # Your configuration (create from .env.example)
├── .gitignore                     # Prevents committing sensitive files
├── yt_watchlater/                 # Downloaded videos (created automatically)
├── yt_watchlater_archive.json     # Archive metadata (created automatically)
└── youtube_cookies.txt            # Your cookies (you provide this)
```

## FAQ

**Q: Why UV instead of pip?**
A: UV is 10-100x faster than pip, handles Python version management automatically, and provides better dependency resolution. It's also backwards compatible - if you prefer pip, it still works!

**Q: Can I download playlists other than Watch Later?**
A: Yes! Set `WATCHLATER_URL` in your `.env` to any public or private (with cookies) playlist URL.

**Q: Will this delete videos from my Watch Later playlist?**
A: No, this only downloads videos. Your YouTube playlist remains unchanged.

**Q: What happens if I delete a video file but it's still in the archive?**
A: The script will skip re-downloading it because it's still in `archive.json`. Remove the entry from the JSON file if you want to re-download.

**Q: Can I use this on multiple computers?**
A: Yes, but each computer maintains its own archive. Copy both videos and `archive.json` to sync.

**Q: Is this tool safe?**
A: The script is open source and you can review the code. It only uses yt-dlp's official functionality. However, use at your own risk and ensure compliance with YouTube's ToS.

**Q: Do I need to learn UV to use this?**
A: No! The basic commands (`uv sync` and `uv run python download.py`) are all you need. UV handles everything else automatically.

## Support

For issues with:
- **UV:** See [UV documentation](https://docs.astral.sh/uv/)
- **yt-dlp:** See [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp)
- **ffmpeg:** See [ffmpeg documentation](https://ffmpeg.org/documentation.html)
- **This script:** Review this README and check the [Troubleshooting](#troubleshooting) section

## License

This tool is provided as-is for educational purposes. Users are responsible for ensuring their use complies with all applicable laws and terms of service.

---

**Remember:** Always respect content creators' rights and YouTube's Terms of Service. This tool is for personal archival only.
