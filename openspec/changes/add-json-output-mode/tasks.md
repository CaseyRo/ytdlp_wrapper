## 1. Implementation

- [ ] 1.1 Add argparse for --json-output command-line flag
- [ ] 1.2 Add JSON_OUTPUT environment variable support
- [ ] 1.3 Create JSON output formatter function
- [ ] 1.4 Modify Rich console usage to be conditional based on JSON mode
- [ ] 1.5 Update progress_hook to collect data for JSON output
- [ ] 1.6 Modify show_banner, show_config_summary, and show_completion_summary to be conditional
- [ ] 1.7 Add JSON output at end of run_download() when in JSON mode
- [ ] 1.8 Test JSON output format and structure
- [ ] 1.9 Verify backward compatibility (no JSON flag = existing behavior)

## 2. Documentation

- [ ] 2.1 Update README.md with JSON output section
- [ ] 2.2 Add JSON output format documentation
- [ ] 2.3 Add command-line usage examples
- [ ] 2.4 Add environment variable documentation

## 3. Testing

- [ ] 3.1 Test with --json-output flag
- [ ] 3.2 Test with JSON_OUTPUT=true environment variable
- [ ] 3.3 Test JSON output with successful downloads
- [ ] 3.4 Test JSON output with skipped videos
- [ ] 3.5 Test JSON output with download errors
- [ ] 3.6 Test JSON output with cleanup operations
- [ ] 3.7 Verify no Rich formatting appears in JSON mode
- [ ] 3.8 Verify normal Rich output when JSON mode disabled
