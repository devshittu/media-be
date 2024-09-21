terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.30"
    }
  }
  required_version = ">= 0.12"
}

provider "digitalocean" {
  token = var.digitalocean_token
}

resource "digitalocean_ssh_key" "mediavm_ssh" {
  name       = "mediavmuser-ssh-key"
  public_key = file("~/.ssh/id_ed25519.pub") # Make sure this is your public key path
}
resource "digitalocean_vpc" "my_vpc" {
  name        = "media-app-vpc"
  region      = var.region
  description = "VPC for media app droplet"
}
# Create DigitalOcean Droplet (VM)

resource "digitalocean_droplet" "media_app_instance" {
  name   = var.instance_name
  region = var.region
  size   = var.machine_type # e.g., "s-1vcpu-1gb"
  image  = var.os_image     # Ubuntu 24.04 LTS

  ssh_keys = [
    digitalocean_ssh_key.mediavm_ssh.fingerprint
  ]

  ipv6     = true
  vpc_uuid = digitalocean_vpc.my_vpc.id

  # Use cloud-init to create the user and set up SSH keys and environment variables
  user_data = <<-EOF
    #cloud-config
    users:
      - name: ${var.ssh_username}
        sudo: ['ALL=(ALL) NOPASSWD:ALL']
        groups: sudo
        shell: /bin/bash
        ssh-authorized-keys:
          - ${file(var.ssh_public_key_path)}
  
    write_files:
      - path: /etc/profile.d/docker_env.sh
        content: |
          export DOCKER_HUB_TOKEN=${var.docker_hub_token}
          export DOCKER_HUB_USERNAME=${var.docker_hub_username}
        owner: root:root
        permissions: '0644'
  EOF

  tags = ["http-server", "https-server"]

  # Copy install_docker.sh script
  provisioner "file" {
    source      = "../scripts/install_docker.sh"
    destination = "/home/${var.ssh_username}/install_docker.sh"

    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file(var.ssh_private_key_path)
      host        = self.ipv4_address
    }
  }

  # Copy startup-script.sh
  provisioner "file" {
    source      = "../scripts/startup-script.sh"
    destination = "/home/${var.ssh_username}/startup-script.sh"

    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file(var.ssh_private_key_path)
      host        = self.ipv4_address
    }
  }

  # Copy additional scripts and service files
  provisioner "file" {
    source      = "../scripts/startup-script.service"
    destination = "/home/${var.ssh_username}/startup-script.service"

    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file(var.ssh_private_key_path)
      host        = self.ipv4_address
    }
  }

  provisioner "file" {
    source      = "../scripts/watch-runners.sh"
    destination = "/home/${var.ssh_username}/watch-runners.sh"

    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file(var.ssh_private_key_path)
      host        = self.ipv4_address
    }
  }

  provisioner "file" {
    source      = "../scripts/actions.runners.service"
    destination = "/home/${var.ssh_username}/actions.runners.service"

    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file(var.ssh_private_key_path)
      host        = self.ipv4_address
    }
  }
  # Copy setup_github_actions.sh script
  provisioner "file" {
    source      = "../scripts/setup_github_actions.sh"
    destination = "/home/${var.ssh_username}/setup_github_actions.sh"

    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file(var.ssh_private_key_path)
      host        = self.ipv4_address
    }
  }
  # Execute scripts and set up services as the less privileged user
  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = var.ssh_username
      private_key = file(var.ssh_private_key_path)
      host        = self.ipv4_address
    }

    inline = [
      # Export environment variables
      "export DOCKER_HUB_USERNAME='${var.docker_hub_username}'",
      "export DOCKER_HUB_TOKEN='${var.docker_hub_token}'",

      # Update package lists
      "sudo DEBIAN_FRONTEND=noninteractive apt-get update -y",

      # Install required packages
      "sudo apt-get install -y fail2ban ufw inotify-tools",

      # Set up firewall rules
      "sudo ufw default deny incoming",
      "sudo ufw default allow outgoing",
      "sudo ufw allow ssh",
      "sudo ufw allow 80/tcp",
      "sudo ufw allow 443/tcp",
      "echo 'y' | sudo ufw enable",

      # Enable and start fail2ban
      "sudo systemctl enable fail2ban",
      "sudo systemctl start fail2ban",

      # Ensure Docker install script runs with preserved environment variables
      # "chmod +x /home/${var.ssh_username}/install_docker.sh",
      # "sudo -E env USER=${var.ssh_username} /home/${var.ssh_username}/install_docker.sh",


      # # Create directories for action runners and logs
      # "sudo mkdir -p /home/${var.ssh_username}/action-runners/backend",
      # "sudo mkdir -p /home/${var.ssh_username}/action-runners/frontend",
      # "sudo mkdir -p /home/${var.ssh_username}/action-runners/logs",

      # # Set ownership and permissions
      # "sudo chown -R ${var.ssh_username}:${var.ssh_username} /home/${var.ssh_username}/action-runners",
      # "sudo chmod +x /home/${var.ssh_username}/watch-runners.sh",

      # # Move service files to appropriate locations
      # "sudo mv /home/${var.ssh_username}/startup-script.service /etc/systemd/system/startup-script.service",
      # "sudo mv /home/${var.ssh_username}/actions.runners.service /etc/systemd/system/actions.runners.service",

      # # Move watch-runners.sh to action-runners directory
      # "sudo mv /home/${var.ssh_username}/watch-runners.sh /home/${var.ssh_username}/action-runners/watch-runners.sh",
      # "sudo chown ${var.ssh_username}:${var.ssh_username} /home/${var.ssh_username}/action-runners/watch-runners.sh",


      # Ensure Docker install script runs with preserved environment variables as non-root user
      "chmod +x /home/${var.ssh_username}/install_docker.sh",
      "/home/${var.ssh_username}/install_docker.sh",

      # Create directories for action runners and logs
      "mkdir -p /home/${var.ssh_username}/action-runners/backend",
      "mkdir -p /home/${var.ssh_username}/action-runners/frontend",
      "mkdir -p /home/${var.ssh_username}/action-runners/logs",

      # Set ownership and permissions
      "chown -R ${var.ssh_username}:${var.ssh_username} /home/${var.ssh_username}/action-runners",
      "chmod +x /home/${var.ssh_username}/watch-runners.sh",
      "chmod +x /home/${var.ssh_username}/setup_github_actions.sh",

      # Move service files to appropriate locations
      "sudo mv /home/${var.ssh_username}/startup-script.service /etc/systemd/system/startup-script.service",
      "sudo mv /home/${var.ssh_username}/actions.runners.service /etc/systemd/system/actions.runners.service",

      # Move watch-runners.sh to action-runners directory
      "mv /home/${var.ssh_username}/watch-runners.sh /home/${var.ssh_username}/action-runners/watch-runners.sh",
      "chown ${var.ssh_username}:${var.ssh_username} /home/${var.ssh_username}/action-runners/watch-runners.sh",

      # Enable and start services
      "sudo systemctl daemon-reload",
      "sudo systemctl enable startup-script.service",
      "sudo systemctl start startup-script.service",
      "sudo systemctl enable actions.runners.service",
      "sudo systemctl start actions.runners.service"
    ]
  }
}
# Create a Floating IP
resource "digitalocean_floating_ip" "static_ip_media_app" {
  region = var.region
}


# Assign the Floating IP to the Droplet
resource "digitalocean_floating_ip_assignment" "ip_assignment" {
  droplet_id = digitalocean_droplet.media_app_instance.id
  ip_address = digitalocean_floating_ip.static_ip_media_app.ip_address
}

# Declare the domain in DigitalOcean
resource "digitalocean_domain" "gong_ng" {
  name = var.dns_name # "gong.ng"
}

# A Records
resource "digitalocean_record" "api_staging_a" {
  domain = digitalocean_domain.gong_ng.name
  type   = "A"
  name   = "api.staging"
  value  = digitalocean_floating_ip.static_ip_media_app.ip_address
  ttl    = 300
}

resource "digitalocean_record" "app_staging_a" {
  domain = digitalocean_domain.gong_ng.name
  type   = "A"
  name   = "app.staging"
  value  = digitalocean_floating_ip.static_ip_media_app.ip_address
  ttl    = 300
}

resource "digitalocean_record" "gong_ng_a" {
  domain = digitalocean_domain.gong_ng.name
  type   = "A"
  name   = "@"
  value  = digitalocean_floating_ip.static_ip_media_app.ip_address
  ttl    = 300
}

# CNAME Records
resource "digitalocean_record" "www_gong_ng_cname" {
  domain = digitalocean_domain.gong_ng.name
  type   = "CNAME"
  name   = "www"
  value  = "${var.dns_name}."
  ttl    = 300
}

resource "digitalocean_record" "www_api_staging_gong_ng_cname" {
  domain = digitalocean_domain.gong_ng.name
  type   = "CNAME"
  name   = "www.api.staging"
  value  = "${var.dns_name}."
  ttl    = 300
}

resource "digitalocean_record" "www_app_staging_gong_ng_cname" {
  domain = digitalocean_domain.gong_ng.name
  type   = "CNAME"
  name   = "www.app.staging"
  value  = "${var.dns_name}."
  ttl    = 300
}

# TXT Records
resource "digitalocean_record" "_dmarc_gong_ng_txt" {
  domain = digitalocean_domain.gong_ng.name
  type   = "TXT"
  name   = "_dmarc"
  value  = "v=DMARC1; p=none; rua=mailto:dmarc_agg@vali.email;"
  ttl    = 300
}

# SendGrid CNAME Records
resource "digitalocean_record" "em2803_gong_ng_cname" {
  domain = digitalocean_domain.gong_ng.name
  type   = "CNAME"
  name   = "em2803"
  value  = "u46027326.wl077.sendgrid.net."
  ttl    = 300
}

resource "digitalocean_record" "s1_domainkey_gong_ng" {
  domain = digitalocean_domain.gong_ng.name
  type   = "CNAME"
  name   = "s1._domainkey"
  value  = "s1.domainkey.u46027326.wl077.sendgrid.net."
  ttl    = 300
}

resource "digitalocean_record" "s2_domainkey_gong_ng" {
  domain = digitalocean_domain.gong_ng.name
  type   = "CNAME"
  name   = "s2._domainkey"
  value  = "s2.domainkey.u46027326.wl077.sendgrid.net."
  ttl    = 300
}

# Firewall Rules for SSH, HTTP, and HTTPS
resource "digitalocean_firewall" "http_https_ssh_firewall" {
  name        = "http-https-ssh-firewall"
  droplet_ids = [digitalocean_droplet.media_app_instance.id]

  # Allow SSH (port 22)
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow HTTP (port 80)
  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow HTTPS (port 443)
  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow ICMP outbound traffic (e.g., ping)
  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Allow all outbound traffic (optional)
  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
# terraform/do/main.tf
