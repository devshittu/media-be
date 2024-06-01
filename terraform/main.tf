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
  credentials = file("./media-app-terraform-service-key.json")
  project     = "media-app-418813"
  region      = "europe-west2"
}


resource "google_container_cluster" "autopilot_cluster" {
  name     = "gliese-autopilot-cluster"
  location = "europe-west2"
  project  = "media-app-418813"

  // Autopilot configuration
  enable_autopilot = true
  deletion_protection = false
}

resource "google_compute_address" "static_ip_media_be" {
  name         = "media-be-ip"
  project      = "media-app-418813"
  address_type = "EXTERNAL"
  region       = "europe-west2"
}

output "kubeconfig" {
  value = google_container_cluster.autopilot_cluster.master_auth.0.cluster_ca_certificate
}

output "media_be_ip_address" {
  value = google_compute_address.static_ip_media_be.address
}


# NEW


resource "google_dns_managed_zone" "custom_domain_gong_ng" {
  name     = "custom-domain-gong-ng"
  dns_name = "gong.ng."
  description = "Managed zone for gong.ng"
  visibility = "public"
  dnssec_config {
    state = "off"
  }

  project = "media-app-418813"
}

resource "google_dns_record_set" "api_staging_a" {
  name         = "api.staging.gong.ng."
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = [google_compute_address.static_ip_media_be.address]
  project = "media-app-418813"
}

resource "google_dns_record_set" "gong_ng_soa" {
  name         = "gong.ng."
  type         = "SOA"
  ttl          = 21600
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = ["ns-cloud-d1.googledomains.com. cloud-dns-hostmaster.google.com. 1 21600 3600 259200 300"]

  project = "media-app-418813"
}

resource "google_dns_record_set" "gong_ng_a" {
  name         = "gong.ng."
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = ["34.49.110.1"]
  project = "media-app-418813"
}

resource "google_dns_record_set" "gong_ng_ns" {
  name         = "gong.ng."
  type         = "NS"
  ttl          = 21600
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = [
    "ns-cloud-d1.googledomains.com.",
    "ns-cloud-d2.googledomains.com.",
    "ns-cloud-d3.googledomains.com.",
    "ns-cloud-d4.googledomains.com."
  ]
  project = "media-app-418813"
}

resource "google_dns_record_set" "www_gong_ng_cname" {
  name         = "www.gong.ng."
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = ["gong.ng."]

  project = "media-app-418813"
}

# # Grant Compute Admin role
# gcloud projects add-iam-policy-binding media-app-418813 \
#     --member="serviceAccount:terraform-admin@media-app-418813.iam.gserviceaccount.com" \
#     --role="roles/compute.admin"

# # Grant Kubernetes Engine Admin role
# gcloud projects add-iam-policy-binding media-app-418813 \
#     --member="serviceAccount:terraform-admin@media-app-418813.iam.gserviceaccount.com" \
#     --role="roles/container.admin"

# # Grant Service Account User role
# gcloud projects add-iam-policy-binding media-app-418813 \
#     --member="serviceAccount:terraform-admin@media-app-418813.iam.gserviceaccount.com" \
#     --role="roles/iam.serviceAccountUser"

# gcloud projects add-iam-policy-binding media-app-418813 \
#     --member="serviceAccount:terraform-admin@media-app-418813.iam.gserviceaccount.com" \
#     --role="roles/dns.admin"


# gcloud dns managed-zones delete custom-domain-gong-ng --project=media-app-418813
