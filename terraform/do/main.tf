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
  size   = var.machine_type # Set to "e2-medium" equivalent
  image  = "ubuntu-22-04-x64"

  # Apply the correct SSH key fingerprint
  #   ssh_keys = [var.ssh_public_key_fingerprint]
  ssh_keys = [
    "${digitalocean_ssh_key.mediavm_ssh.fingerprint}"
  ]
  # Enable IPv6 and private networking
  ipv6     = true
  vpc_uuid = digitalocean_vpc.my_vpc.id

  connection {
    type = "ssh"
    # user        = var.ssh_username
    user = "root"
    host = self.ipv4_address
    # host        = digitalocean_droplet.media_app_instance.ipv4_address
    # private_key = file(var.ssh_private_key_path)
    private_key = file("~/.ssh/id_ed25519")
    timeout     = "2m"
  }



  # Create a lower-privilege user and assign sudo permissions
  provisioner "remote-exec" {
    inline = [
      "export DEBIAN_FRONTEND=noninteractive",

      # Check if the /home/mediavmuser path exists and handle it
      "if [ -e /home/mediavmuser ]; then sudo rm -rf /home/mediavmuser; fi",

      "sudo adduser --disabled-password --gecos '' ${var.ssh_username}",
      "echo '${var.ssh_username}:${var.regular_vm_user_password}' | sudo chpasswd",
      "sudo usermod -aG sudo ${var.ssh_username}",
      "echo '${var.ssh_username} ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/${var.ssh_username}",

      # Create the .ssh directory for the new user
      "sudo mkdir -p /home/${var.ssh_username}/.ssh",
      "sudo cp /root/.ssh/authorized_keys /home/${var.ssh_username}/.ssh/",
      "sudo chown -R ${var.ssh_username}:${var.ssh_username} /home/${var.ssh_username}/.ssh",
      "sudo chmod 700 /home/${var.ssh_username}/.ssh",
      "sudo chmod 600 /home/${var.ssh_username}/.ssh/authorized_keys"
    ]
  }

  #   # Install fail2ban and UFW, set up firewall
  #   provisioner "remote-exec" {
  #     inline = [
  #       "export DEBIAN_FRONTEND=noninteractive",
  #       "sudo apt-get update -y",
  #       "sudo apt-get upgrade -y",
  #       "sudo apt-get install -y fail2ban ufw",

  #       # Set up firewall rules
  #       "sudo ufw default deny incoming",
  #       "sudo ufw default allow outgoing",
  #       "sudo ufw allow ssh",
  #       "sudo ufw allow 80/tcp",
  #       "sudo ufw allow 443/tcp",
  #       "sudo ufw --force enable",

  #       # Enable fail2ban service
  #       "sudo systemctl enable fail2ban",
  #       "sudo systemctl start fail2ban"
  #     ]
  #   }


  # Ensure install_docker.sh is provisioned and executed
  provisioner "file" {
    source      = "../scripts/install_docker.sh"
    destination = "/home/${var.ssh_username}/install_docker.sh"

    connection {
      type        = "ssh"
      user        = "root"
      private_key = file("~/.ssh/id_ed25519")
      host        = digitalocean_droplet.media_app_instance.ipv4_address
    }
  }

  provisioner "file" {
    source      = "../scripts/startup-script.sh"
    destination = "/home/${var.ssh_username}/startup-script.sh"

    connection {
      type        = "ssh"
      user        = "root"
      private_key = file("~/.ssh/id_ed25519")
      host        = digitalocean_droplet.media_app_instance.ipv4_address
    }
  }


  #   Connect as lower-privileged user for Docker setup
  #   provisioner "remote-exec" {
  #     connection {
  #       type        = "ssh"
  #       user        = var.ssh_username
  #       private_key = file("~/.ssh/id_ed25519")
  #       host        = self.ipv4_address
  #       timeout     = "2m"
  #     }

  #     inline = [
  #       # Ensure Docker install script runs
  #       "chmod +x /home/${var.ssh_username}/install_docker.sh",
  #       "sudo /home/${var.ssh_username}/install_docker.sh",

  #       # Run startup script
  #       "chmod +x /home/${var.ssh_username}/startup-script.sh",
  #       "/home/${var.ssh_username}/startup-script.sh"
  #     ]
  #   }
  tags = ["http-server", "https-server"]
}


# DNS Zone
resource "digitalocean_domain" "gong_ng" {
  name = var.dns_name
}

# A Records for API and App Staging
resource "digitalocean_record" "api_staging_a" {
  domain = digitalocean_domain.gong_ng.name
  type   = "A"
  name   = "api.staging"
  value  = digitalocean_droplet.media_app_instance.ipv4_address
  ttl    = 300
}

resource "digitalocean_record" "app_staging_a" {
  domain = digitalocean_domain.gong_ng.name
  type   = "A"
  name   = "app.staging"
  value  = digitalocean_droplet.media_app_instance.ipv4_address
  ttl    = 300
}


resource "digitalocean_record" "www_gong_ng_cname" {
  #   name   = "www.${var.dns_name}"
  name   = "www"
  type   = "CNAME"
  ttl    = 300
  domain = digitalocean_domain.gong_ng.name
  value  = "${var.dns_name}." # Add a dot at the end of the domain name
}
# DMARC TXT Record
resource "digitalocean_record" "_dmarc_gong_ng_txt" {
  domain = digitalocean_domain.gong_ng.name
  type   = "TXT"
  name   = "_dmarc"
  value  = "v=DMARC1; p=none; rua=mailto:dmarc_agg@vali.email;"
  ttl    = 300
}

resource "digitalocean_record" "s1_domainkey_gong_ng" {
  name   = "s1._domainkey.${var.dns_name}"
  type   = "CNAME"
  ttl    = 300
  domain = digitalocean_domain.gong_ng.name
  value  = "s1.domainkey.u46027326.wl077.sendgrid.net." # Add a dot at the end
}

resource "digitalocean_record" "s2_domainkey_gong_ng" {
  name   = "s2._domainkey.${var.dns_name}"
  type   = "CNAME"
  ttl    = 300
  domain = digitalocean_domain.gong_ng.name
  value  = "s2.domainkey.u46027326.wl077.sendgrid.net." # Add a dot at the end
}

resource "digitalocean_record" "em2803_gong_ng_cname" {
  name   = "em2803.${var.dns_name}"
  type   = "CNAME"
  ttl    = 300
  domain = digitalocean_domain.gong_ng.name
  value  = "u46027326.wl077.sendgrid.net." # Add a dot at the end
}

# Firewall Rules for HTTP and HTTPS
resource "digitalocean_firewall" "http_https_firewall" {
  name        = "http-https-firewall"
  droplet_ids = [digitalocean_droplet.media_app_instance.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

# terraform_do/main.tf
