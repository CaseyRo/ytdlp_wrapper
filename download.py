#!/usr/bin/env python3

import os
import sys
import json
import datetime
import time
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

# Initialize Rich console
console = Console()

# Global variables for statistics
stats = {
    "start_time": None,
    "downloaded": [],
    "skipped": [],
    "errors": []
}

def show_banner():
    """Display welcome banner"""
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
    config_text = f"""[bold]Playlist:[/bold] {WATCHLATER_URL}
[bold]Output Directory:[/bold] {OUTPUT_DIR}
[bold]Archive File:[/bold] {ARCHIVE_JSON}
[bold]Cookies:[/bold] {'✓ Configured' if COOKIES_FILE else '✗ Not set'}
[bold]Webhook:[/bold] {'✓ Enabled (' + WEBHOOK_URL + ':' + str(WEBHOOK_PORT) + ')' if WEBHOOK_URL else '✗ Disabled'}"""

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
    if not stats["start_time"]:
        return

    elapsed = time.time() - stats["start_time"]
    minutes, seconds = divmod(int(elapsed), 60)

    # Create statistics panel
    summary_text = f"""[bold]Total Videos:[/bold] {len(stats['downloaded']) + len(stats['skipped'])}
[bold green]Downloaded:[/bold green] {len(stats['downloaded'])}
[bold yellow]Skipped:[/bold yellow] {len(stats['skipped'])}
[bold red]Errors:[/bold red] {len(stats['errors'])}
[bold]Duration:[/bold] {minutes}m {seconds}s"""

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
                console.print(f"[green]✓[/green] Webhook notification sent successfully")
            else:
                console.print(f"[yellow]⚠[/yellow] Webhook returned status {response.status}")

    except HTTPError as e:
        console.print(f"[yellow]⚠[/yellow] Webhook HTTP error {e.code}: {e.reason}")
    except URLError as e:
        console.print(f"[yellow]⚠[/yellow] Webhook URL error: {e.reason}")
    except TimeoutError:
        console.print(f"[yellow]⚠[/yellow] Webhook request timed out")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Webhook failed: {e}")

# Hook: called periodically with download status
def progress_hook(d):
    # d is a dict with info, see d['status'] in {“downloading”, “finished”}
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
                    "download_date": datetime.datetime.utcnow().isoformat() + "Z",
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

                # Display success message
                console.print(f"[green]✅ Downloaded:[/green] {metadata.get('title', 'Unknown')}")

                # Send webhook notification (includes video_id in payload)
                send_webhook(metadata)
    # (you could also track progress in “downloading” status if you like)

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
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        newname = f"{ts} {parts[1]}"
        newpath = os.path.join(dirname, newname)
        try:
            os.rename(filepath, newpath)
            return newpath
        except Exception as e:
            print("Warning: rename fallback failed:", e, file=sys.stderr)
    return filepath

def run_download():
    # Initialize start time
    stats["start_time"] = time.time()

    # Display welcome banner and configuration
    show_banner()
    show_config_summary()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    archive = load_archive()

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "paths": {"home": OUTPUT_DIR},
        "progress_hooks": [progress_hook],
        "download_archive": None,  # we won’t use the built-in archive, we use JSON
        "outtmpl": determine_outtmpl(),
        "merge_output_format": "mp4",  # or mkv, as you prefer
        "quiet": False,
        "no_warnings": True,
        # set mtime so the file timestamp matches upload date (if available)
        # default behavior of yt-dlp is to set file mtime to upload-date if known. (see man) :contentReference[oaicite:0]{index=0}
        # If you want always use download time, you can disable it:
        # "no_mtime": True,
    }
    if COOKIES_FILE:
        ydl_opts["cookiefile"] = COOKIES_FILE

    with YoutubeDL(ydl_opts) as ydl:
        # You can optionally filter out already-downloaded via our JSON archive:
        # But easier: let yt-dlp fetch playlist entries, then skip by ourselves
        # Actually, we can pass a custom “download” list: for each entry, if id in archive, skip
        info = ydl.extract_info(WATCHLATER_URL, download=False)
        entries = info.get("entries", [])
        to_download = []
        for ent in entries:
            vid = ent.get("id")
            if vid is None:
                continue
            if vid in archive:
                stats["skipped"].append({"video_id": vid, "title": ent.get('title')})
                console.print(f"[yellow]⏭️  Skipped:[/yellow] {ent.get('title', 'Unknown')} [dim](already downloaded)[/dim]")
            else:
                to_download.append(ent.get("webpage_url"))

        if not to_download:
            console.print("[yellow]ℹ️  Nothing new to download.[/yellow]")
            show_completion_summary()
            return

        # Show download count
        console.print(f"\n[cyan]📥 Downloading {len(to_download)} new video(s)...[/cyan]\n")

        # Now actually download
        ydl.download(to_download)

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

if __name__ == "__main__":
    try:
        run_download()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠ Download interrupted by user[/yellow]")
        show_completion_summary()
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        sys.exit(1)
