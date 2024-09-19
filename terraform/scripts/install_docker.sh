#!/bin/bash

# This script installs Docker on Ubuntu 22.04

# Source environment variables
source /etc/profile.d/docker_env.sh

# Exit if credentials are not set
if [ -z "$DOCKER_HUB_USERNAME" ] || [ -z "$DOCKER_HUB_TOKEN" ]; then
  echo "Docker Hub credentials are not set."
  exit 1
fi

# Step 1: Remove existing Docker key and list file
sudo rm -f /usr/share/keyrings/docker-archive-keyring.gpg
sudo rm -f /etc/apt/sources.list.d/docker.list

# Step 2: Update package list
sudo apt update

# Step 3: Install prerequisite packages
sudo apt install -y  ca-certificates curl gnupg lsb-release apt-transport-https software-properties-common

# Step 4: Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Step 5: Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Step 6: Update package list again
sudo apt update

# Step 7: Check Docker package availability
apt-cache policy docker-ce

# Step 8: Install Docker
sudo apt install -y  docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Step 9: Verify Docker installation
# sudo systemctl status docker

# Step 8: Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker

# Step 10: Log in to Docker Hub using environment variables
echo "$DOCKER_HUB_TOKEN" | docker login --username "$DOCKER_HUB_USERNAME" --password-stdin

# Step 11: Add the current user to the Docker group
sudo usermod -aG docker $USER

# Print completion message
echo "Docker installation script completed."

# Exit script gracefully
exit 0

# terraform/scripts/install_docker.sh