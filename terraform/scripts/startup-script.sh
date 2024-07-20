#!/bin/bash
# /usr/local/bin/startup-script.sh

log_file="/var/log/startup-script.log"

# Function to log messages
log_message() {
    echo "$(date) - $1" >> "$log_file"
}

log_message "Checking action runner setup"

# Check if the action runner is setup, and perform your required actions
if [ -f /home/mediavmuser/action-runners/backend/config.sh ]; then
    log_message "Action runner is set up, performing actions..."
    # Add your startup commands here
    # Example:
    # /path/to/start-action-runner.sh
else
    log_message "Action runner is not set up."
fi

# Start the actions.runners.service
log_message "Starting actions.runners.service..."
# if sudo systemctl start actions.runners.service; then
#     log_message "actions.runners.service started successfully"
# else
#     log_message "Failed to start actions.runners.service"
# fi

log_message "Startup script finished successfully"

# terraform/scripts/startup-script.sh