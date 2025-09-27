#!/bin/bash

# A temporary file to capture the output of failed commands.
TMP_OUTPUT_FILE=$(mktemp)
# Ensure the temp file is cleaned up on script exit.
trap 'rm -f "$TMP_OUTPUT_FILE"' EXIT

# Use process substitution to avoid stdin issues, which is still best practice.
while IFS= read -r vocab_file; do
  echo "Testing with vocab file: $vocab_file"

  # 1. Run the command in the background (&).
  #    This preserves the TTY, allowing the TUI to start.
  #    Redirect its stdout and stderr to our temp file.
  go run ./src session \
    --number 500 \
    --session-config tests/examples/example-session-config.json \
    --vocab-list "$vocab_file" \
    --server-port 5500 > "$TMP_OUTPUT_FILE" 2>&1 </dev/null &

  # 2. Capture the Process ID (PID) of the background command.
  PID=$!

  # 3. Wait for 7 seconds.
  sleep 7

  # 4. Check if the process is still running.
  #    `kill -0` doesn't actually kill the process; it just checks if it exists.
  if kill -0 "$PID" 2>/dev/null; then
    # SUCCESS: The process is still running, so the TUI must have started.
    echo "Success: TUI started for $vocab_file"
    # Clean up by killing the process.
    kill "$PID"
    # Wait for the process to be fully cleaned up by the system.
    wait "$PID" 2>/dev/null
  else
    # FAILURE: The process died before the 7 seconds were up.
    # `wait` retrieves the exit code.
    wait "$PID" 2>/dev/null
    status=$?
    echo "Error running with $vocab_file (exit code: $status):"
    # Print the output we captured.
    cat "$TMP_OUTPUT_FILE"
  fi

  echo "----------------------------------------"

done < <(find assets -name "*.txt")