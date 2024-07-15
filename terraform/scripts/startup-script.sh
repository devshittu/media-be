#!/bin/bash
# /usr/local/bin/startup-script.sh
echo "Startup script started"
# Check if the action runner is setup, and perform your required actions
# Example command to check for action runner setup
if [ -f /path/to/action-runner/config ]; then
  echo "Action runner is set up, performing actions..."
  # Add your startup commands here
  # Example:
  # /path/to/start-action-runner.sh
else
  echo "Action runner is not set up."
fi

echo "Startup script finished successfully"