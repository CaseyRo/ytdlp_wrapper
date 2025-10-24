## Why

The current ytdlp wrapper provides rich terminal output with progress bars, colored messages, and formatted tables. However, when running in automated environments, this rich output is not useful and can interfere with programmatic processing. Users need a way to get clean, structured JSON output that contains only the essential results (what was downloaded, rejected, failed, etc.) without any terminal formatting or progress indicators.

## What Changes

- Add a new `--json-output` command-line flag that suppresses all Rich terminal formatting
- When JSON mode is enabled, output only raw JSON containing download results
- JSON output includes: downloaded videos, skipped videos, errors, and summary statistics
- Use standard Python argparse library for command-line parsing
- Maintain backward compatibility - existing behavior unchanged when flag not used
- Add environment variable `JSON_OUTPUT=true` as alternative to command-line flag
- Update README.md with JSON output usage examples

## Impact

- Affected specs: terminal-ui (modified to support JSON output mode), user-documentation (updated with basic examples)
- Affected code: download.py (main script logic for output formatting and CLI parsing)
- Affected documentation: README.md (new JSON output section)
- **BREAKING**: None - this is purely additive functionality
