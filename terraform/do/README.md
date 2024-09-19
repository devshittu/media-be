Add a specific resource on the gcp

```sh

terraform init

terraform apply -var-file="terraform.staging.tfvars" --auto-approve  


terraform destroy -var-file="terraform.staging.tfvars" --auto-approve  
```
