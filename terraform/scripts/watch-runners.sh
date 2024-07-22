#!/bin/bash

# Directory to watch for action runners
RUNNERS_DIR="/home/mediavmuser/action-runners"
LOG_DIR="${RUNNERS_DIR}/logs"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to start a runner
start_runner() {
    local runner_dir=$1
    local runner_name=$(basename "$runner_dir")
    local log_file="${LOG_DIR}/${runner_name}.log"

    echo "Starting runner: $runner_name"
    (cd "$runner_dir" && sudo -u mediavmuser ./run.sh >>"$log_file" 2>&1 &)
}

# Export function for subshells
export -f start_runner

# Initial run of all existing runners
for runner_dir in "$RUNNERS_DIR"/*/; do
    [ -d "$runner_dir" ] && start_runner "$runner_dir"
done

# Watch for new directories and start runners
inotifywait -m -r -e create "$RUNNERS_DIR" | while read -r path action file; do
    if [ -d "$path$file" ]; then
        start_runner "$path$file"
    fi
done

# terraform/scripts/watch-runners.sh
