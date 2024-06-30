output "kubeconfig" {
  value = google_container_cluster.autopilot_cluster.master_auth.0.cluster_ca_certificate
}

output "media_be_ip_address" {
  value = google_compute_address.static_ip_media_be.address
}


output "artifact_registry_url" {
  value = "europe-west2-docker.pkg.dev/${var.project}/${var.artifact_registry_name}"
}
