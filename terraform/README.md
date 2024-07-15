Add a specific resource on the gcp

```sh

terraform init

terraform apply -target=google_compute_instance.media_app_instance --auto-approve


terraform destroy -target=google_compute_instance.media_app_instance --auto-approve
```
