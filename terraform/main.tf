terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.31.1"
    }
  }
  required_version = ">= 0.12"
}


provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}



resource "google_artifact_registry_repository" "media-app-dev-repo" {

  project    = var.project
  location   = var.region
  repository_id = var.artifact_registry_name
  description = "Docker repository"
  format     = "DOCKER"
}

# resource "google_artifact_registry_repository_iam_member" "artifact_registry_admin" {
#   provider = google

#   project    = var.project
#   location   = var.region
#   repository = google_artifact_registry_repository.artifact_registry.repository_id

#   role   = "roles/artifactregistry.admin"
#   member = "serviceAccount:${var.terraform_service_account}"
# }


resource "google_container_cluster" "autopilot_cluster" {
  name               = var.cluster_name
  location           = var.region
  project            = var.project
  // Autopilot configuration
  enable_autopilot   = true
  deletion_protection = false
}

resource "google_compute_address" "static_ip_media_be" {
  name         = var.compute_address_name
  project      = var.project
  address_type = "EXTERNAL"
  region       = var.region
}




# NEW

resource "google_dns_managed_zone" "custom_domain_gong_ng" {
  name        = var.dns_zone_name
  dns_name    = var.dns_name
  description = "Managed zone for ${var.dns_name}"
  visibility  = "public"
  dnssec_config {
    state = "off"
  }
  project = var.project
}

resource "google_dns_record_set" "api_staging_a" {
  name         = "api.staging.${var.dns_name}"
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = [google_compute_address.static_ip_media_be.address]
  project      = var.project
}

resource "google_dns_record_set" "gong_ng_soa" {
  name         = var.dns_name
  type         = "SOA"
  ttl          = 21600
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = ["ns-cloud-d1.googledomains.com. cloud-dns-hostmaster.google.com. 1 21600 3600 259200 300"]
  project      = var.project
}

resource "google_dns_record_set" "gong_ng_a" {
  name         = var.dns_name
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = ["34.49.110.1"]
  project      = var.project
}

resource "google_dns_record_set" "gong_ng_ns" {
  name         = var.dns_name
  type         = "NS"
  ttl          = 21600
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = [
    "ns-cloud-d1.googledomains.com.",
    "ns-cloud-d2.googledomains.com.",
    "ns-cloud-d3.googledomains.com.",
    "ns-cloud-d4.googledomains.com."
  ]
  project = var.project
}

resource "google_dns_record_set" "www_gong_ng_cname" {
  name         = "www.${var.dns_name}"
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = [var.dns_name]
  project      = var.project
}

# # Grant Compute Admin role
# gcloud projects add-iam-policy-binding gong-ng \
#     --member="serviceAccount:terraform-admin@gong-ng.iam.gserviceaccount.com" \
#     --role="roles/compute.admin"

# # Grant Kubernetes Engine Admin role
# gcloud projects add-iam-policy-binding gong-ng \
#     --member="serviceAccount:terraform-admin@gong-ng.iam.gserviceaccount.com" \
#     --role="roles/container.admin"

# # Grant Service Account User role
# gcloud projects add-iam-policy-binding gong-ng \
#     --member="serviceAccount:terraform-admin@gong-ng.iam.gserviceaccount.com" \
#     --role="roles/iam.serviceAccountUser"

# gcloud projects add-iam-policy-binding gong-ng \
#     --member="serviceAccount:terraform-admin@gong-ng.iam.gserviceaccount.com" \
#     --role="roles/dns.admin"


# gcloud dns managed-zones delete custom-domain-gong-ng --project=gong-ng
