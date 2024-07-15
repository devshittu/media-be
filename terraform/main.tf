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

  project       = var.project
  location      = var.region
  repository_id = var.artifact_registry_name
  description   = "Docker repository"
  format        = "DOCKER"
}


resource "google_container_cluster" "autopilot_cluster" {
  name     = var.cluster_name
  location = var.region
  project  = var.project
  // Autopilot configuration
  enable_autopilot    = true
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


resource "google_dns_record_set" "gong_ng_a" {
  name         = var.dns_name
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = [google_compute_address.static_ip_media_be.address]
  project      = var.project
}

resource "google_dns_record_set" "www_gong_ng_cname" {
  name         = "www.${var.dns_name}"
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.custom_domain_gong_ng.name
  rrdatas      = [var.dns_name]
  project      = var.project
}

# VM


resource "google_compute_instance" "media_app_instance" {
  name         = var.instance_name
  machine_type = var.machine_type
  zone         = var.instance_zone
  project      = var.project

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 50
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.static_ip_media_be.address // Use the existing external IP
    }
  }


  metadata = {
    ssh-keys = "${var.ssh_username}:${var.ssh_public_key}"
    
    startup-script = <<-EOF
      #!/bin/bash
      echo 'export DOCKER_HUB_TOKEN=${var.docker_hub_token}' >> /etc/profile.d/docker_env.sh
      echo 'export DOCKER_HUB_USERNAME=${var.docker_hub_username}' >> /etc/profile.d/docker_env.sh
      chmod +x /etc/profile.d/docker_env.sh
      source /etc/profile.d/docker_env.sh
    EOF
  }


  tags = ["http-server", "https-server"]

  service_account {
    email  = "default"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }


  provisioner "file" {
    source      = "./scripts/install_docker.sh"
    destination = "/home/${var.ssh_username}/install_docker.sh"

    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file("~/.ssh/id_ed25519")
      host        = google_compute_instance.media_app_instance.network_interface.0.access_config.0.nat_ip
    }
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file("~/.ssh/id_ed25519") // Ensure you use the private key corresponding to the public key
      host        = google_compute_instance.media_app_instance.network_interface.0.access_config.0.nat_ip
    }


    inline = [
      "echo 'Welcome to Google Compute'",

      "sudo adduser --disabled-password --gecos '' ${var.regular_vm_user_username}",
      "echo '${var.regular_vm_user_username}:${var.regular_vm_user_password}' | sudo chpasswd",
      "sudo usermod -aG sudo ${var.regular_vm_user_username}",
      "echo '${var.regular_vm_user_username} ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/${var.regular_vm_user_username}",
      "sudo mkdir -p /home/${var.regular_vm_user_username}/.ssh",
      "sudo cp /home/${var.ssh_username}/.ssh/authorized_keys /home/${var.regular_vm_user_username}/.ssh/",
      "sudo chown -R ${var.regular_vm_user_username}:${var.regular_vm_user_username} /home/${var.regular_vm_user_username}/.ssh",
      "sudo chmod 700 /home/${var.regular_vm_user_username}/.ssh",
      "sudo chmod 600 /home/${var.regular_vm_user_username}/.ssh/authorized_keys",
      "sudo chmod +x /home/${var.ssh_username}/install_docker.sh",
      "sudo /home/${var.ssh_username}/install_docker.sh"

      # // Log in to Docker Hub (ensure environment variables are set)
      # "echo ${var.docker_hub_token} | docker login --username ${var.docker_hub_username} --password-stdin"
    ]

  }
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
