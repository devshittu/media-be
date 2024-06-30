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
