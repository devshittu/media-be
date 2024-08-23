project                   = "taishaprj"
region                    = "europe-west2"
credentials               = "./terraform-admin-service-key.json"
dns_zone_name             = "custom-domain-gong-ng"
dns_name                  = "gong.ng."
compute_address_name      = "media-be-ip"
cluster_name              = "gliese-autopilot-cluster"
artifact_registry_name    = "media-app-repo"
terraform_service_account = "terraform-admin@taishaprj.iam.gserviceaccount.com"

instance_name = "media-app-instance"
instance_zone = "europe-west2-a"
machine_type  = "e2-medium"

ssh_username        = "mediavmuser"
ssh_public_key      = "ssh-ed25519 AAAA__Sample_Key email@*.com"
docker_hub_username = "devshittu"
docker_hub_token    = "dckr_pat_0_Sample_Token"

regular_vm_user_username = "user_name"
regular_vm_user_password = "sample_password"

# terraform/terraform.tfvars
