# Add Webhook Notifications on Successful Download

## Why
Users may want to integrate the downloader with other systems, automation workflows, or notification services. Adding webhook support enables real-time notifications when videos are successfully downloaded, allowing integration with services like Discord, Slack, custom APIs, home automation systems, or logging platforms without polling or checking files manually.

## What Changes
- Add HTTP POST webhook functionality to send JSON payloads on successful downloads
- Add `WEBHOOK_URL` environment variable for webhook endpoint configuration
- Add `WEBHOOK_PORT` environment variable for port configuration (defaults to 80)
- Add optional `WEBHOOK_SECRET` environment variable for request authentication
- Send metadata (video title, ID, upload date, download date, filepath) as JSON payload
- Handle webhook failures gracefully (log errors but don't fail the download)
- Update `.env.example` with webhook configuration options (URL, PORT, SECRET)
- Document webhook usage, payload format, and integration examples in README

## Impact
- **Affected specs**: webhook-integration (new capability)
- **Affected code**: download.py (add webhook call in progress_hook after successful download)
- **User benefit**: Real-time notifications and integrations with external systems
- **Breaking changes**: None (webhook is optional, disabled by default)

