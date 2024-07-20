variable "project" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

variable "credentials" {
  description = "The path to the GCP credentials file"
  type        = string
}

variable "dns_zone_name" {
  description = "The DNS zone name"
  type        = string
}

variable "dns_name" {
  description = "The DNS name"
  type        = string
}

variable "compute_address_name" {
  description = "The name of the compute address"
  type        = string
}

variable "cluster_name" {
  description = "The name of the Kubernetes cluster"
  type        = string
}

variable "artifact_registry_name" {
  description = "The name of the Artifact Registry"
  type        = string
  default     = "media-app-repo"
}
variable "terraform_service_account" {
  description = "The account to use for the terraform service"
  type        = string
}

variable "instance_name" {
  description = "Name of the VM instance"
  type        = string
  default     = "media-app-instance"
}

variable "instance_zone" {
  description = "The zone in which the VM instance will be created"
  type        = string
  default     = "us-central1-a"
}

variable "machine_type" {
  description = "The machine type to use for the VM instance"
  type        = string
  default     = "e2-medium"
}

variable "ssh_username" {
  description = "The SSH username"
  type        = string
}


variable "regular_vm_user_username" {
  description = "The less privileged user name to use for the VM instance"
  type        = string
}


variable "regular_vm_user_password" {
  description = "The less privileged user password to use for the VM instance"
  type        = string
}

variable "ssh_public_key" {
  description = "The SSH public key"
  type        = string
}

variable "docker_hub_username" {
  description = "The docker hub username"
  type        = string
  default = "devshittu"
}

variable "docker_hub_token" {
  description = "The docker hub token"
  type        = string
}

variable "ssh_private_key_path" {
  description = "Path to the SSH private key file"
  type        = string
  default     = "~/.ssh/id_ed25519"
}