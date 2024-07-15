Add a specific resource on the gcp

```sh

terraform init

terraform apply -var-file="terraform.staging.tfvars" -target=google_compute_instance.media_app_instance --auto-approve


terraform destroy -target=google_compute_instance.media_app_instance --auto-approve
```
