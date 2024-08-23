#!/bin/bash

# Set variables
KEY_FILE_PATH="./" #"$HOME/"
PROJECT_ID="taishaprj"
TERRAFORM_SERVICE_ACCOUNT_NAME="terraform-admin"
TERRAFORM_SERVICE_ACCOUNT="$TERRAFORM_SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"

GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME="github-actions"
GITHUB_ACTIONS_SERVICE_ACCOUNT="$GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"

# Create Terraform service account
gcloud iam service-accounts create $TERRAFORM_SERVICE_ACCOUNT_NAME \
    --description="Service account for Terraform to automate various infrastructure tasks" \
    --display-name="Terraform Admin"

# Assign roles to Terraform service account
declare -a TERRAFORM_ROLES=(
    "roles/compute.admin"
    "roles/container.admin"
    "roles/iam.serviceAccountUser"
    "roles/dns.admin"
    "roles/artifactregistry.admin"
)

for ROLE in "${TERRAFORM_ROLES[@]}"; do
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$TERRAFORM_SERVICE_ACCOUNT" \
        --role="$ROLE"
done

# Create a key for the Terraform service account
echo "Creating key file for the $TERRAFORM_SERVICE_ACCOUNT_NAME service account..."
TERRAFORM_KEY_FILE="${KEY_FILE_PATH}${TERRAFORM_SERVICE_ACCOUNT_NAME}-service-key.json"
gcloud iam service-accounts keys create $TERRAFORM_KEY_FILE \
    --iam-account="$TERRAFORM_SERVICE_ACCOUNT"
echo "Service account setup complete. Key file created at $TERRAFORM_KEY_FILE"

# Create GitHub Actions service account
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

# Assign roles to the GitHub Actions service account
declare -a GITHUB_ACTIONS_ROLES=(
    "roles/container.admin"
    "roles/storage.admin"
    "roles/viewer"
    "roles/container.clusterViewer"
    "roles/container.clusterAdmin"
    "roles/container.viewer"
    "roles/artifactregistry.writer"
)

for ROLE in "${GITHUB_ACTIONS_ROLES[@]}"; do
    assign_role "$ROLE"
done

# Create a key for the GitHub Actions service account
echo "Creating key file for the service account..."
GITHUB_ACTIONS_KEY_FILE="${KEY_FILE_PATH}${GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME}-service-key.json"
gcloud iam service-accounts keys create $GITHUB_ACTIONS_KEY_FILE \
    --iam-account="$GITHUB_ACTIONS_SERVICE_ACCOUNT"
echo "Service account setup complete. Key file created at $GITHUB_ACTIONS_KEY_FILE"

# Convert the key file to base64 and output it
echo "Converting key file to base64..."
BASE64_KEY=$(base64 -i $GITHUB_ACTIONS_KEY_FILE | tr -d '\n')
echo "Service account setup complete."
echo "Base64-encoded key file:"
echo $BASE64_KEY
echo "Copy the above base64-encoded key and add it as a GitHub secret named 'GKE_KEY'."

# Save the base64-encoded key to a file (optional)
echo $BASE64_KEY > "${KEY_FILE_PATH}${GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME}-service-key-base64.txt"
echo "Base64-encoded key file saved to ${KEY_FILE_PATH}${GITHUB_ACTIONS_SERVICE_ACCOUNT_NAME}-service-key-base64.txt"

# Function to check assigned roles
check_assigned_roles() {
    local service_account_email=$1
    gcloud projects get-iam-policy $PROJECT_ID \
        --flatten="bindings[].members" \
        --format="table(bindings.role)" \
        --filter="bindings.members:serviceAccount:$service_account_email"
}

echo "Roles assigned to $GITHUB_ACTIONS_SERVICE_ACCOUNT:"
check_assigned_roles $GITHUB_ACTIONS_SERVICE_ACCOUNT

echo "Roles assigned to $TERRAFORM_SERVICE_ACCOUNT:"
check_assigned_roles $TERRAFORM_SERVICE_ACCOUNT
