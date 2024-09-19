
data "google_dns_record_set" "soa_record" {
  name         = google_dns_managed_zone.custom_domain_gong_ng.dns_name
  type         = "SOA"
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
}

data "google_dns_record_set" "ns_record" {
  name         = google_dns_managed_zone.custom_domain_gong_ng.dns_name
  type         = "NS"
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
}
