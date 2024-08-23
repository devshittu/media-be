#!/bin/bash

KEY_FILE_PATH="./" #"$HOME/"
PROJECT_ID="taishaprj"
TERRAFORM_SERVICE_ACCOUNT_NAME="terraform-admin"
TERRAFORM_SERVICE_ACCOUNT="$TERRAFORM_SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"

GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME="github-actions"
GITHUB_ACTIONS_SERVICE_ACCOUNT="$GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $TERRAFORM_SERVICE_ACCOUNT_NAME \
    --description="Service account for Terraform to automate various infrastructure tasks" \
    --display-name="Terraform Admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$TERRAFORM_SERVICE_ACCOUNT" \
    --role="roles/compute.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$TERRAFORM_SERVICE_ACCOUNT" \
    --role="roles/container.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$TERRAFORM_SERVICE_ACCOUNT" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$TERRAFORM_SERVICE_ACCOUNT" \
    --role="roles/dns.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$TERRAFORM_SERVICE_ACCOUNT" \
    --role="roles/artifactregistry.admin"

# Create a key for the service account
echo "Creating key file for the $TERRAFORM_SERVICE_ACCOUNT_NAME service account..."
KEY_FILE="${KEY_FILE_PATH}${TERRAFORM_SERVICE_ACCOUNT_NAME}-service-key.json"
gcloud iam service-accounts keys create $KEY_FILE \
    --iam-account="$TERRAFORM_SERVICE_ACCOUNT"

echo "Service account setup complete. Key file created at $KEY_FILE"

# My github actions setup

gcloud iam service-accounts create $GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME \
    --description="Service account for GitHub Actions CI/CD pipeline" \
    --display-name="GitHub Actions"

# Function to assign roles with retries
assign_role() {
    local role=$1
    local attempts=3
    local count=0
    while [ $count -lt $attempts ]; do
        if gcloud projects add-iam-policy-binding $PROJECT_ID \
            --member="serviceAccount:$GITHUB_ACTIONS_SERVICE_ACCOUNT" \
            --role="$role"; then
            echo "Role $role assigned successfully."
            return 0
        else
            echo "Failed to assign role $role. Retrying..."
            count=$((count + 1))
            sleep 2
        fi
    done
    echo "Failed to assign role $role after $attempts attempts."
    return 1
}

# Assign roles to the service account
assign_role "roles/container.admin"
assign_role "roles/storage.admin"
assign_role "roles/viewer"
assign_role "roles/container.clusterViewer"
assign_role "roles/container.clusterAdmin"
assign_role "roles/container.viewer"
assign_role "roles/artifactregistry.writer"

# Create a key for the service account
echo "Creating key file for the service account..."
KEY_FILE="${KEY_FILE_PATH}${GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME}-service-key.json"
gcloud iam service-accounts keys create $KEY_FILE \
    --iam-account="$GITHUB_ACTIONS_SERVICE_ACCOUNT"

echo "Service account setup complete. Key file created at $KEY_FILE"

# Convert the key file to base64 and output it
echo "Converting key file to base64..."
BASE64_KEY=$(base64 -i ${KEY_FILE_PATH}${GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME}-service-key.json | tr -d '\n')

echo "Service account setup complete."
echo "Base64-encoded key file:"
echo $BASE64_KEY
echo "Copy the above base64-encoded key and add it as a GitHub secret named 'GKE_KEY'."

# Save the base64-encoded key to a file (optional)
echo $BASE64_KEY >${KEY_FILE_PATH}${GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME}-service-key-base64.txt
echo "Base64-encoded key file saved to ${KEY_FILE_PATH}${GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME}-service-key-base64.txt"

# terraform/scripts/grant_roles.sh
