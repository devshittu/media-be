
# Outputs to get key information
output "droplet_ip" {
  description = "Public IP address of the Droplet"
  value       = digitalocean_droplet.media_app_instance.ipv4_address
}

output "ssh_command" {
  description = "SSH Command to connect to the Droplet"
  value       = "ssh ${var.ssh_username}@${digitalocean_droplet.media_app_instance.ipv4_address} -i ~/.ssh/id_ed25519"
}

# DNS A record for API Staging
output "api_staging_a_record" {
  description = "DNS A record for API Staging"
  value       = "api.staging.${digitalocean_domain.gong_ng.name} -> ${digitalocean_droplet.media_app_instance.ipv4_address}"
}

# DNS A record for App Staging
output "app_staging_a_record" {
  description = "DNS A record for App Staging"
  value       = "app.staging.${digitalocean_domain.gong_ng.name} -> ${digitalocean_droplet.media_app_instance.ipv4_address}"
}

# CNAME Record
output "www_cname_record" {
  description = "CNAME record for www"
  value       = "www.${digitalocean_domain.gong_ng.name} -> ${var.dns_name}."
}