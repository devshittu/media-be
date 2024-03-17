#!/bin/bash

# Function to encode a value in base64
encode_to_base64() {
    echo -n "$1" | base64
}

# Function to determine if a key is sensitive based on its name
is_sensitive_key() {
    local key_name="$1"
    if [[ "$key_name" =~ (KEY|ID|TOKEN|NUMBER|SECRET|CREDENTIALS?|PASSWORD) ]]; then
        return 0 # True, key is considered sensitive
    else
        return 1 # False, key is not considered sensitive
    fi
}

# Process the .env file to encode sensitive values
process_env_file() {
    local env_file="${1:-.env}" # Default to .env if no specific file is provided

    if [ ! -f "$env_file" ]; then
        echo "File not found: $env_file" >&2
        exit 1
    fi

    while IFS='=' read -r key value || [ -n "$key" ]; do
        # Remove potential Windows CR characters
        key=$(echo $key | tr -d '\r')
        value=$(echo $value | tr -d '\r')

        if is_sensitive_key "$key"; then
            local encoded_value=$(encode_to_base64 "$value")
            echo "$key: $encoded_value"
        fi
    done <"$env_file"
}

# Main execution block
# Parse command-line options
while getopts "f:" opt; do
    case $opt in
    f) file_path="$OPTARG" ;;
    *)
        echo "Incorrect usage. Correct command: $0 [-f path/to/.env]" >&2
        exit 1
        ;;
    esac
done

# Call the processing function with the provided or default .env file
process_env_file "${file_path:-.env}"

# k8s-manifests/encode_sensitive.sh