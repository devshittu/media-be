variable "digitalocean_token" {
  description = "The DigitalOcean API token."
  type        = string
}

variable "region" {
  description = "The DigitalOcean region where the droplet will be created."
  type        = string
}

variable "dns_zone_name" {
  description = "The name of the DNS zone for the domain."
  type        = string
}

variable "dns_name" {
  description = "The root domain name (e.g., example.com)."
  type        = string
}

variable "instance_name" {
  description = "The name of the DigitalOcean Droplet (VM)."
  type        = string
}

variable "ssh_username" {
  description = "The username for SSH connections."
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
variable "ssh_public_key_fingerprint" {
  description = "The fingerprint of the SSH public key to use for the Droplet."
  type        = string
}

variable "ssh_private_key_path" {
  description = "The path to the private SSH key for connecting to the Droplet."
  type        = string
}

variable "machine_type" {
  description = "The size of the DigitalOcean Droplet (e.g., s-1vcpu-1gb)."
  type        = string
}

variable "docker_hub_username" {
  description = "Docker Hub username for pulling images."
  type        = string
}

variable "docker_hub_token" {
  description = "Docker Hub token for authentication."
  type        = string
}
variable "vpc_name" {
  description = "The name of the VPC to create."
  type        = string
  default     = "media-app-vpc"
}


# terraform_do/variables.tf