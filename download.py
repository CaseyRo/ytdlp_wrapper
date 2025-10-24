#!/usr/bin/env python3

import os
import sys
import json
import datetime
import time
import argparse
from yt_dlp import YoutubeDL
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# Load .env file if it exists (python-dotenv is optional)
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load from .env file in current directory
except ImportError:
    # python-dotenv not installed, skip .env file loading
    pass

# Configuration (you can override via env vars, .env file, or command-line args)
# Priority: command-line env vars > .env file > defaults
WATCHLATER_URL = os.environ.get("WATCHLATER_URL", "https://www.youtube.com/playlist?list=WL")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "./yt_watchlater")
ARCHIVE_JSON = os.environ.get("ARCHIVE_JSON", "./yt_watchlater_archive.json")
COOKIES_FILE = os.environ.get("COOKIES_FILE", None)  # optional

# Webhook configuration (optional)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)
WEBHOOK_PORT = int(os.environ.get("WEBHOOK_PORT", "80"))
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", None)

# Storage retention configuration (optional)
RETENTION_DAYS = os.environ.get("RETENTION_DAYS", None)

# Playlist management configuration (optional)
PLAYLIST_REVERSE = os.environ.get("PLAYLIST_REVERSE", "true").lower() in ("true", "1", "yes")  # Default: true (newest first)
MAX_DOWNLOADS = os.environ.get("MAX_DOWNLOADS", None)  # Default: None (unlimited)
PLAYLIST_START = os.environ.get("PLAYLIST_START", None)  # Default: None (start from beginning)
PLAYLIST_END = os.environ.get("PLAYLIST_END", None)  # Default: None (go to end)

# JSON output configuration
JSON_OUTPUT = os.environ.get("JSON_OUTPUT", "false").lower() in ("true", "1", "yes")

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="YouTube Watch Later Downloader with JSON output support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download.py                    # Normal rich output
  python download.py --json-output     # JSON output mode
  JSON_OUTPUT=true python download.py  # JSON output via environment variable
        """
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results in JSON format instead of rich terminal formatting"
    )
    return parser.parse_args()

# Parse arguments
args = parse_arguments()

# Override JSON_OUTPUT with command line argument if provided
if args.json_output:
    JSON_OUTPUT = True

# Initialize Rich console (conditional based on JSON mode)
console = Console() if not JSON_OUTPUT else None

# Global variables for statistics
stats = {
    "start_time": None,
    "downloaded": [],
    "skipped": [],
    "errors": [],
    "cleaned_files": [],
    "cleaned_bytes": 0
}

def format_json_output():
    """Format the final results as JSON output"""
    if not stats["start_time"]:
        return json.dumps({"error": "No execution data available"})

    elapsed = time.time() - stats["start_time"]

    # Calculate cleanup statistics
    cleanup_stats = None
    if stats['cleaned_files']:
        cleanup_stats = {
            "files_deleted": len(stats['cleaned_files']),
            "space_freed_bytes": stats['cleaned_bytes']
        }

    # Build the JSON output
    result = {
        "summary": {
            "total_videos": len(stats['downloaded']) + len(stats['skipped']),
            "downloaded_count": len(stats['downloaded']),
            "skipped_count": len(stats['skipped']),
            "error_count": len(stats['errors']),
            "duration_seconds": round(elapsed, 2)
        },
        "downloaded": stats['downloaded'],
        "skipped": stats['skipped'],
        "errors": stats['errors']
    }

    # Add cleanup stats if available
    if cleanup_stats:
        result["cleanup"] = cleanup_stats

    return json.dumps(result, indent=2, ensure_ascii=False)

def show_banner():
    """Display welcome banner"""
    if JSON_OUTPUT:
        return  # Skip banner in JSON mode

    banner = Panel(
        "[bold cyan]📹 YouTube Watch Later Downloader[/bold cyan]\n"
        "[dim]v1.0.0[/dim]",
        box=box.DOUBLE,
        border_style="cyan"
    )
    console.print(banner)
    console.print()

def show_config_summary():
    """Display configuration summary panel"""
    if JSON_OUTPUT:
        return  # Skip config summary in JSON mode

    retention_status = '✗ Disabled'
    if RETENTION_DAYS:
        try:
            days = int(RETENTION_DAYS)
            if days > 0:
                retention_status = f'✓ {days} days'
            else:
                retention_status = '✗ Disabled (invalid value)'
        except (ValueError, TypeError):
            retention_status = '✗ Disabled (invalid value)'

    # Playlist management status
    playlist_order = '✓ Newest first' if PLAYLIST_REVERSE else 'Oldest first'
    max_dl_status = f'max {MAX_DOWNLOADS}' if MAX_DOWNLOADS else 'unlimited'

    # Build playlist range string
    range_parts = []
    if PLAYLIST_START:
        range_parts.append(f'start={PLAYLIST_START}')
    if PLAYLIST_END:
        range_parts.append(f'end={PLAYLIST_END}')
    playlist_range = ', '.join(range_parts) if range_parts else 'full playlist'

    config_text = f"""[bold]Playlist:[/bold] {WATCHLATER_URL}
[bold]Output Directory:[/bold] {OUTPUT_DIR}
[bold]Archive File:[/bold] {ARCHIVE_JSON}
[bold]Cookies:[/bold] {'✓ Configured' if COOKIES_FILE else '✗ Not set'}
[bold]Webhook:[/bold] {'✓ Enabled (' + WEBHOOK_URL + ':' + str(WEBHOOK_PORT) + ')' if WEBHOOK_URL else '✗ Disabled'}
[bold]Retention:[/bold] {retention_status}
[bold]Playlist Order:[/bold] {playlist_order}
[bold]Download Limit:[/bold] {max_dl_status} ({playlist_range})"""

    panel = Panel(
        config_text,
        title="[bold]Configuration[/bold]",
        border_style="blue",
        box=box.ROUNDED
    )
    console.print(panel)
    console.print()

def show_completion_summary():
    """Display completion summary with statistics"""
    if JSON_OUTPUT:
        return  # Skip completion summary in JSON mode

    if not stats["start_time"]:
        return

    elapsed = time.time() - stats["start_time"]
    minutes, seconds = divmod(int(elapsed), 60)

    # Create statistics panel
    summary_text = f"""[bold]Total Videos:[/bold] {len(stats['downloaded']) + len(stats['skipped'])}
[bold green]Downloaded:[/bold green] {len(stats['downloaded'])}
[bold yellow]Skipped:[/bold yellow] {len(stats['skipped'])}
[bold red]Errors:[/bold red] {len(stats['errors'])}"""

    # Add cleanup stats if any files were cleaned
    if stats['cleaned_files']:
        size_mb = stats['cleaned_bytes'] / (1024 * 1024)
        if size_mb >= 1024:
            size_str = f"{size_mb / 1024:.2f} GB"
        else:
            size_str = f"{size_mb:.1f} MB"
        summary_text += f"\n[bold orange1]Cleaned:[/bold orange1] {len(stats['cleaned_files'])} files ({size_str})"

    summary_text += f"\n[bold]Duration:[/bold] {minutes}m {seconds}s"

    panel = Panel(
        summary_text,
        title="[bold]Summary[/bold]",
        border_style="green",
        box=box.DOUBLE
    )
    console.print()
    console.print(panel)

    # Show downloaded videos table if any
    if stats["downloaded"]:
        console.print()
        table = Table(title="Downloaded Videos", box=box.SIMPLE, show_header=True, header_style="bold cyan")
        table.add_column("Video ID", style="dim")
        table.add_column("Title", style="cyan")
        table.add_column("Upload Date", style="green")

        for video in stats["downloaded"]:
            table.add_row(
                video.get("video_id", ""),
                video.get("title", "Unknown")[:60],
                video.get("upload_date", "Unknown")
            )

        console.print(table)

# Load archive (JSON mapping video_id -> metadata)
def load_archive():
    if os.path.exists(ARCHIVE_JSON):
        with open(ARCHIVE_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

# Save archive
def save_archive(ar):
    tmp = ARCHIVE_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ar, f, indent=2, ensure_ascii=False)
    os.replace(tmp, ARCHIVE_JSON)

# Send webhook notification
def send_webhook(payload):
    """Send HTTP POST webhook with video metadata. Fails gracefully on errors."""
    if not WEBHOOK_URL:
        return  # Webhook not configured, skip silently

    try:
        # Parse URL and construct full endpoint with port
        parsed = urlparse(WEBHOOK_URL)

        # Construct full URL with port
        if parsed.scheme:
            # URL has scheme (http:// or https://)
            if parsed.port:
                # Port already in URL, use as-is
                full_url = WEBHOOK_URL
            else:
                # Add port to URL
                netloc_with_port = f"{parsed.hostname}:{WEBHOOK_PORT}"
                full_url = f"{parsed.scheme}://{netloc_with_port}{parsed.path}"
                if parsed.query:
                    full_url += f"?{parsed.query}"
        else:
            # No scheme, assume http and add port
            full_url = f"http://{WEBHOOK_URL.lstrip('/')}"
            if WEBHOOK_PORT != 80:
                # Parse again to insert port correctly
                parsed = urlparse(full_url)
                netloc_with_port = f"{parsed.hostname}:{WEBHOOK_PORT}"
                full_url = f"{parsed.scheme}://{netloc_with_port}{parsed.path}"

        # Prepare JSON payload
        json_data = json.dumps(payload).encode('utf-8')

        # Create request with headers
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': len(json_data)
        }

        # Add authentication if secret is configured
        if WEBHOOK_SECRET:
            headers['Authorization'] = f'Bearer {WEBHOOK_SECRET}'

        req = Request(full_url, data=json_data, headers=headers, method='POST')

        # Send request with timeout
        with urlopen(req, timeout=10) as response:
            if response.status >= 200 and response.status < 300:
                if not JSON_OUTPUT:
                    console.print(f"[green]✓[/green] Webhook notification sent successfully")
            else:
                if not JSON_OUTPUT:
                    console.print(f"[yellow]⚠[/yellow] Webhook returned status {response.status}")

    except HTTPError as e:
        if not JSON_OUTPUT:
            console.print(f"[yellow]⚠[/yellow] Webhook HTTP error {e.code}: {e.reason}")
    except URLError as e:
        if not JSON_OUTPUT:
            console.print(f"[yellow]⚠[/yellow] Webhook URL error: {e.reason}")
    except TimeoutError:
        if not JSON_OUTPUT:
            console.print(f"[yellow]⚠[/yellow] Webhook request timed out")
    except Exception as e:
        if not JSON_OUTPUT:
            console.print(f"[yellow]⚠[/yellow] Webhook failed: {e}")

# Hook: called periodically with download status
def progress_hook(d):
    # d is a dict with info, see d['status'] in {"downloading", "finished", "error"}
    if d.get("status") == "finished":
        # final path
        filepath = d.get("filename")
        info = d.get("info_dict", {})
        vid = info.get("id")
        # In some cases, filename may still be temp; but here we assume it's final
        if vid:
            # record in archive
            archive = load_archive()
            if vid not in archive:
                metadata = {
                    "video_id": vid,
                    "title": info.get("title"),
                    "upload_date": info.get("upload_date"),
                    "download_date": datetime.datetime.now(datetime.UTC).isoformat(),
                    "filepath": filepath,
                }
                # Save to archive (use original format without video_id key)
                archive[vid] = {
                    "title": metadata["title"],
                    "upload_date": metadata["upload_date"],
                    "download_date": metadata["download_date"],
                    "filepath": metadata["filepath"],
                }
                save_archive(archive)

                # Track in stats
                stats["downloaded"].append(metadata)

                # Display success message (skip in JSON mode)
                if not JSON_OUTPUT:
                    console.print(f"[green]✅ Downloaded:[/green] {metadata.get('title', 'Unknown')}")

                # Send webhook notification (includes video_id in payload)
                send_webhook(metadata)
    elif d.get("status") == "error":
        # Track download errors
        info = d.get("info_dict", {})
        vid = info.get("id", "unknown")
        title = info.get("title", "Unknown")
        error_msg = d.get("error", "Unknown error")

        stats["errors"].append({
            "video_id": vid,
            "title": title,
            "error": str(error_msg)
        })

        if not JSON_OUTPUT:
            console.print(f"[red]❌ Error:[/red] {title} [dim](ID: {vid})[/dim]")
            console.print(f"[dim]   Skipping and continuing with next video...[/dim]\n")
    # (you could also track progress in "downloading" status if you like)

def determine_outtmpl():
    # Template tries upload date; fallback to placeholder that we’ll rename later
    # Use a placeholder prefix “ZZZ” or something so fallback ones cluster
    return os.path.join(OUTPUT_DIR, "%(upload_date)s %(title)s [%(id)s].%(ext)s")

def rename_fallback_missing_timestamp(filepath, info):
    """
    If the filename begins with something like “NA ” (upload_date not known),
    rename it so that the prefix is download timestamp.
    """
    dirname, fname = os.path.split(filepath)
    # Here, info dict has 'download_date' or we used archive timestamp
    vid = info.get("id")
    # Only rename if we find “NA” or empty date prefix
    # Eg: filename = "NA My Title [abcd].mp4"
    parts = fname.split(" ", 1)
    if parts and (parts[0] == "NA" or parts[0] == ""):
        # new timestamp
        ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
        newname = f"{ts} {parts[1]}"
        newpath = os.path.join(dirname, newname)
        try:
            os.rename(filepath, newpath)
            return newpath
        except Exception as e:
            print("Warning: rename fallback failed:", e, file=sys.stderr)
    return filepath

def cleanup_old_files(archive, retention_days):
    """
    Delete files older than retention_days based on download_date in archive.
    Returns updated archive with removed entries.
    """
    if not retention_days or retention_days <= 0:
        return archive

    # Calculate cutoff date
    cutoff_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=retention_days)

    # Track files to delete
    to_delete = []

    # Find files older than retention period
    for video_id, metadata in archive.items():
        download_date_str = metadata.get("download_date")
        if not download_date_str:
            # No download_date, skip with warning
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Skipping cleanup for {video_id}: missing download_date")
            continue

        try:
            # Parse ISO format date (e.g., "2024-10-15T10:30:00Z")
            download_date = datetime.datetime.fromisoformat(download_date_str.replace('Z', '+00:00'))
            # Make timezone-naive for comparison
            download_date = download_date.replace(tzinfo=None)

            if download_date < cutoff_date:
                to_delete.append((video_id, metadata))
        except (ValueError, AttributeError) as e:
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Invalid download_date for {video_id}: {e}")
            continue

    if not to_delete:
        if not JSON_OUTPUT:
            console.print("[dim]ℹ️  No files to clean up (all within retention period)[/dim]")
        return archive

    # Delete files and track results
    if not JSON_OUTPUT:
        console.print(f"[cyan]🗑️  Cleaning up {len(to_delete)} file(s) older than {retention_days} days...[/cyan]")

    deleted_count = 0
    for video_id, metadata in to_delete:
        filepath = metadata.get("filepath")
        if not filepath:
            # No filepath, just remove from archive
            archive.pop(video_id, None)
            continue

        try:
            # Get file size before deletion
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                os.remove(filepath)
                stats["cleaned_bytes"] += file_size
                deleted_count += 1
                if not JSON_OUTPUT:
                    console.print(f"[dim]  Deleted: {os.path.basename(filepath)}[/dim]")
            else:
                # File already missing, just log warning
                if not JSON_OUTPUT:
                    console.print(f"[yellow]⚠[/yellow] File not found (already deleted?): {filepath}")

            # Remove from archive
            archive.pop(video_id, None)
            stats["cleaned_files"].append(video_id)

        except PermissionError:
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Permission denied deleting: {filepath}")
            # Keep in archive since we couldn't delete
        except Exception as e:
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Error deleting {filepath}: {e}")
            # Keep in archive since we couldn't delete

    # Show summary
    if deleted_count > 0:
        size_mb = stats["cleaned_bytes"] / (1024 * 1024)
        if size_mb >= 1024:
            size_str = f"{size_mb / 1024:.2f} GB"
        else:
            size_str = f"{size_mb:.1f} MB"
        if not JSON_OUTPUT:
            console.print(f"[green]✅ Cleanup complete:[/green] Removed {deleted_count} file(s), freed {size_str}")

    if not JSON_OUTPUT:
        console.print()
    return archive

def run_download():
    # Initialize start time
    stats["start_time"] = time.time()

    # Display welcome banner and configuration
    show_banner()
    show_config_summary()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    archive = load_archive()

    # Run cleanup if retention is configured
    if RETENTION_DAYS:
        try:
            retention_days = int(RETENTION_DAYS)
            if retention_days > 0:
                archive = cleanup_old_files(archive, retention_days)
                save_archive(archive)
            else:
                if not JSON_OUTPUT:
                    console.print("[yellow]⚠[/yellow] RETENTION_DAYS must be a positive number (cleanup disabled)")
                    console.print()
        except (ValueError, TypeError):
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Invalid RETENTION_DAYS value: {RETENTION_DAYS} (cleanup disabled)")
                console.print()

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "paths": {"home": OUTPUT_DIR},
        "progress_hooks": [progress_hook],
        "download_archive": None,  # we won't use the built-in archive, we use JSON
        "outtmpl": determine_outtmpl(),
        "merge_output_format": "mp4",  # or mkv, as you prefer
        "quiet": JSON_OUTPUT,  # Suppress yt-dlp output in JSON mode
        "no_warnings": True,
        "ignoreerrors": True,  # Continue on download errors (e.g., private/unavailable videos)
        # set mtime so the file timestamp matches upload date (if available)
        # default behavior of yt-dlp is to set file mtime to upload-date if known. (see man)
        # If you want always use download time, you can disable it:
        # "no_mtime": True,

        # Playlist management options
        "playlistreverse": PLAYLIST_REVERSE,  # Download newest first (default: true)
    }

    # Add optional playlist management settings
    if COOKIES_FILE:
        ydl_opts["cookiefile"] = COOKIES_FILE
    if MAX_DOWNLOADS:
        try:
            ydl_opts["max_downloads"] = int(MAX_DOWNLOADS)
        except ValueError:
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Invalid MAX_DOWNLOADS value: {MAX_DOWNLOADS} (ignoring)")
    if PLAYLIST_START:
        try:
            ydl_opts["playlist_start"] = int(PLAYLIST_START)
        except ValueError:
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Invalid PLAYLIST_START value: {PLAYLIST_START} (ignoring)")
    if PLAYLIST_END:
        try:
            ydl_opts["playlist_end"] = int(PLAYLIST_END)
        except ValueError:
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Invalid PLAYLIST_END value: {PLAYLIST_END} (ignoring)")

    # Let's use a different approach - disable playlistreverse temporarily for limiting
    if MAX_DOWNLOADS:
        try:
            max_dl = int(MAX_DOWNLOADS)
            # Set a reasonable limit for playlist processing to avoid downloading all metadata
            # We'll check 3x the max downloads to ensure we find enough new videos
            estimated_check = max_dl * 3
            estimated_check = min(estimated_check, 100)  # Cap at 100 to avoid long waits

            if not JSON_OUTPUT:
                console.print(f"[cyan]📋 Checking up to {estimated_check} most recent videos for new downloads...[/cyan]\n")

            # Temporarily disable playlistreverse to get predictable item numbering
            # We'll handle the reverse order in our filtering logic instead
            ydl_opts["playlistreverse"] = False
            ydl_opts["playlist_items"] = f"1:{estimated_check}"

        except ValueError:
            if not JSON_OUTPUT:
                console.print(f"[yellow]⚠[/yellow] Invalid MAX_DOWNLOADS value: {MAX_DOWNLOADS}")
            max_dl = None
    else:
        max_dl = None

    with YoutubeDL(ydl_opts) as ydl:
        # Extract playlist info with limited scope
        info = ydl.extract_info(WATCHLATER_URL, download=False)
        entries = info.get("entries", [])

        # Filter out already downloaded videos
        # Since we disabled playlistreverse, entries are in oldest-first order
        # We need to reverse them to get newest-first, then filter
        to_download = []
        skipped_count = 0

        # Reverse the entries to get newest first (since playlistreverse was disabled)
        entries_reversed = list(reversed(entries))

        for ent in entries_reversed:
            vid = ent.get("id")
            if vid is None:
                continue
            if vid in archive:
                stats["skipped"].append({"video_id": vid, "title": ent.get('title')})
                skipped_count += 1
                if not JSON_OUTPUT:
                    console.print(f"[yellow]⏭️  Skipped:[/yellow] {ent.get('title', 'Unknown')} [dim](already downloaded)[/dim]")
            else:
                to_download.append(ent.get("webpage_url"))
                # Stop if we've reached max downloads limit
                if max_dl and len(to_download) >= max_dl:
                    break

        if not to_download:
            if not JSON_OUTPUT:
                console.print("[yellow]ℹ️  Nothing new to download.[/yellow]")
                if skipped_count > 0:
                    console.print(f"[dim]ℹ️  Found {skipped_count} already downloaded videos in recent playlist[/dim]")
            show_completion_summary()
            return

        # Show download count
        if not JSON_OUTPUT:
            console.print(f"\n[cyan]📥 Downloading {len(to_download)} new video(s)...[/cyan]\n")

        # Track which videos we're attempting to download
        attempted_videos = {}
        for url in to_download:
            try:
                # Extract video ID from URL
                if 'v=' in url:
                    vid = url.split('v=')[-1].split('&')[0]
                elif 'youtu.be/' in url:
                    vid = url.split('youtu.be/')[-1].split('?')[0]
                else:
                    vid = url.split('/')[-1].split('?')[0]
                attempted_videos[vid] = url
            except:
                pass

        # Now actually download with proper limiting
        # Use yt-dlp's built-in max_downloads if we have a limit
        if max_dl and len(to_download) > max_dl:
            # Limit the downloads to max_dl videos
            to_download = to_download[:max_dl]
            if not JSON_OUTPUT:
                console.print(f"[cyan]📝 Limited to {max_dl} downloads as configured[/cyan]\n")

        # Download the videos
        ydl.download(to_download)

        # After download, check which videos failed (attempted but not downloaded)
        archive_after = load_archive()
        downloaded_ids = set(stats["downloaded"])
        for vid, url in attempted_videos.items():
            if vid not in archive_after and vid not in [d.get("video_id") for d in stats["downloaded"]]:
                # This video was attempted but not downloaded
                if vid not in [e.get("video_id") for e in stats["errors"]]:
                    stats["errors"].append({
                        "video_id": vid,
                        "title": "Unknown",
                        "error": "Failed to download (video may be private, unavailable, or removed)"
                    })

        # After download, perform fallback renaming where upload_date was missing
        # For video in archive that has filepath, we can check filename and rename if needed
        archive2 = load_archive()
        for vid, meta in archive2.items():
            fp = meta.get("filepath")
            if not fp:
                continue
            # We want to re-open the file info via yt-dlp to get metadata
            try:
                info_vid = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
            except Exception:
                info_vid = {}
            newpath = rename_fallback_missing_timestamp(fp, info_vid)
            # if renamed, update archive
            if newpath != fp:
                archive2[vid]["filepath"] = newpath
        save_archive(archive2)

    # Show completion summary
    show_completion_summary()

    # Output JSON if in JSON mode
    if JSON_OUTPUT:
        print(format_json_output())

if __name__ == "__main__":
    try:
        run_download()
    except KeyboardInterrupt:
        if not JSON_OUTPUT:
            console.print("\n[yellow]⚠ Download interrupted by user[/yellow]")
        show_completion_summary()
        if JSON_OUTPUT:
            print(format_json_output())
        sys.exit(0)
    except Exception as e:
        if not JSON_OUTPUT:
            console.print(f"\n[red]❌ Error: {e}[/red]")
        if JSON_OUTPUT:
            error_result = {
                "error": str(e),
                "summary": {
                    "total_videos": 0,
                    "downloaded_count": 0,
                    "skipped_count": 0,
                    "error_count": 1,
                    "duration_seconds": 0
                },
                "downloaded": [],
                "skipped": [],
                "errors": [{"error": str(e)}]
            }
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)
