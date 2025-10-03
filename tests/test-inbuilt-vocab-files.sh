#!/bin/bash
set -euo pipefail

# TODO: Improve:
# - loop through files in alphabetical order
# - better formatting with colours, the `testing with vocab file` gets overwritten by test result
# - overall result at the end

# Temp file for captured output
TMP_OUTPUT_FILE=$(mktemp)
trap 'rm -f "$TMP_OUTPUT_FILE"' EXIT

MODE="auto"
if [[ "${1:-}" == "--manual" ]]; then
  MODE="manual"
fi

while IFS= read -r vocab_file; do
  echo -ne "\r\033[K"
  echo "Testing with vocab file: $vocab_file"

  if [[ "$MODE" == "manual" ]]; then
    # Just start the process, don’t check success/failure
    go run ./src session \
      --number 500 \
      --session-config tests/examples/example-session-config.json \
      --vocab-list "$vocab_file" \
      --server-port 5500
  else
    # Full check mode
    go run ./src session \
      --number 500 \
      --session-config tests/examples/example-session-config.json \
      --vocab-list "$vocab_file" \
      --server-port 5500 >"$TMP_OUTPUT_FILE" 2>&1 </dev/null &

    PID=$!
    sleep 7
    if kill -0 "$PID" 2>/dev/null; then
      echo -ne "\r\033[K"
      echo "Success: TUI started for $vocab_file"
      kill "$PID"
      wait "$PID" 2>/dev/null || true
    else
      wait "$PID" 2>/dev/null || true
      status=$?
      echo -ne "\r\033[K"
      echo "Error running with $vocab_file (exit code: $status):"
      cat "$TMP_OUTPUT_FILE"
    fi
  fi

  echo -ne "\r\033[K"
  echo "----------------------------------------"

done < <(find assets -name "*.txt")
