# Webhook Integration Specification

## ADDED Requirements

### Requirement: Webhook Configuration
The application SHALL support optional webhook configuration via environment variables.

#### Scenario: Webhook URL configuration
- **GIVEN** a user wants to receive notifications
- **WHEN** they set the WEBHOOK_URL environment variable
- **THEN** the application sends HTTP POST requests to that URL on successful downloads
- **AND** the webhook is disabled if WEBHOOK_URL is not set

#### Scenario: Webhook port configuration
- **GIVEN** a user wants to specify a custom port
- **WHEN** they set the WEBHOOK_PORT environment variable
- **THEN** the application constructs the webhook URL with the specified port
- **AND** the port defaults to 80 if WEBHOOK_PORT is not set

#### Scenario: Default port behavior
- **GIVEN** a user sets WEBHOOK_URL but not WEBHOOK_PORT
- **WHEN** a webhook is sent
- **THEN** the request is sent to port 80
- **AND** the URL is constructed as http://hostname:80/path or https://hostname:80/path

#### Scenario: Custom port usage
- **GIVEN** a user sets WEBHOOK_PORT to 8080
- **WHEN** a webhook is sent
- **THEN** the request is sent to the specified port
- **AND** the URL includes the custom port (e.g., http://hostname:8080/path)

#### Scenario: Webhook authentication
- **GIVEN** a user sets WEBHOOK_SECRET environment variable
- **WHEN** webhook notifications are sent
- **THEN** the request includes an Authorization header with the secret
- **AND** the header format is `Authorization: Bearer {WEBHOOK_SECRET}`

#### Scenario: Optional webhook usage
- **GIVEN** a user does not configure WEBHOOK_URL
- **WHEN** videos are downloaded
- **THEN** the application functions normally without webhooks
- **AND** no errors are raised about missing webhook configuration

### Requirement: Webhook Payload
The application SHALL send a JSON payload containing video metadata on successful downloads.

#### Scenario: Complete payload structure
- **GIVEN** a video is successfully downloaded
- **WHEN** the webhook is triggered
- **THEN** the payload includes video_id, title, upload_date, download_date, and filepath
- **AND** the payload is valid JSON
- **AND** all fields are populated (or null if unavailable)

#### Scenario: Payload content accuracy
- **GIVEN** a video with known metadata
- **WHEN** the webhook sends the payload
- **THEN** video_id matches the YouTube video ID
- **AND** title matches the video title
- **AND** upload_date is in YYYYMMDD format (or null)
- **AND** download_date is in ISO 8601 format
- **AND** filepath contains the absolute or relative path to the downloaded file

#### Scenario: Example payload format
- **GIVEN** the webhook documentation
- **WHEN** users review the payload structure
- **THEN** they see an example like:
  ```json
  {
    "video_id": "dQw4w9WgXcQ",
    "title": "Example Video Title",
    "upload_date": "20241015",
    "download_date": "2024-10-15T14:30:00Z",
    "filepath": "./yt_watchlater/20241015 Example Video Title [dQw4w9WgXcQ].mp4"
  }
  ```

### Requirement: HTTP Request Handling
The application SHALL send webhook requests with appropriate HTTP headers and error handling.

#### Scenario: HTTP POST method
- **GIVEN** a webhook is configured
- **WHEN** a notification is sent
- **THEN** the request uses HTTP POST method
- **AND** Content-Type header is set to application/json

#### Scenario: Request timeout
- **GIVEN** a webhook endpoint is slow or unresponsive
- **WHEN** the request takes too long
- **THEN** the request times out after a reasonable period (e.g., 10 seconds)
- **AND** the timeout does not crash the application

#### Scenario: Authentication header
- **GIVEN** WEBHOOK_SECRET is configured
- **WHEN** a webhook request is sent
- **THEN** the Authorization header contains `Bearer {WEBHOOK_SECRET}`
- **AND** the secret is not logged or exposed in error messages

### Requirement: Error Handling
The application SHALL handle webhook failures gracefully without interrupting downloads.

#### Scenario: Webhook endpoint unreachable
- **GIVEN** the webhook URL is invalid or unreachable
- **WHEN** a download completes
- **THEN** the webhook failure is logged to stderr
- **AND** the download process continues successfully
- **AND** the video metadata is still saved to archive.json

#### Scenario: Webhook returns error status
- **GIVEN** the webhook endpoint returns 4xx or 5xx status
- **WHEN** a notification is sent
- **THEN** the error is logged with status code
- **AND** downloads continue unaffected

#### Scenario: Network timeout
- **GIVEN** the webhook request times out
- **WHEN** the timeout occurs
- **THEN** a timeout error is logged
- **AND** subsequent downloads are not affected

#### Scenario: No webhook configured
- **GIVEN** WEBHOOK_URL is not set
- **WHEN** videos are downloaded
- **THEN** no webhook requests are made
- **AND** no warnings or errors about webhooks appear

### Requirement: Documentation
The README and configuration files SHALL document webhook integration thoroughly.

#### Scenario: Environment variables documented
- **GIVEN** a user reviews .env.example
- **WHEN** they look for webhook configuration
- **THEN** they find WEBHOOK_URL with description and example
- **AND** they find WEBHOOK_SECRET with explanation of optional authentication

#### Scenario: README webhook section
- **GIVEN** a user wants to integrate webhooks
- **WHEN** they read the README
- **THEN** they find a dedicated webhook section
- **AND** they see the JSON payload structure documented
- **AND** they find integration examples (Discord, Slack, custom API)

#### Scenario: Integration examples provided
- **GIVEN** a user wants to use webhooks with popular services
- **WHEN** they review the documentation
- **THEN** they find example webhook URLs for Discord, Slack, or similar services
- **AND** they see example payload handling code or instructions

#### Scenario: Troubleshooting guidance
- **GIVEN** a user encounters webhook issues
- **WHEN** they check troubleshooting section
- **THEN** they find guidance on testing webhooks
- **AND** they see common error messages explained
- **AND** they know how to verify webhook functionality

