#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Retrieve the latest commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)
echo "Using commit hash: $COMMIT_HASH"

# Create Namespace
# echo "Creating namespace..."
# kubectl apply -f - <<EOF
# apiVersion: v1
# kind: Namespace
# metadata:
#   name: staging
#   labels:
#     app.kubernetes.io/managed-by: "Helm"
#   annotations:
#     meta.helm.sh/release-name: "web-app"
#     meta.helm.sh/release-namespace: "staging"
# EOF

# TODO:
# Download web-app-secret and configmap is provided in the helm chart so no need of provisioning again

# Deploy Redis
echo "Deploying Redis..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install db-redis bitnami/redis -f ./k8s/helms/dbs/redis-values.yaml --namespace staging --create-namespace

# Deploy Postgres
echo "Deploying Postgres..."
helm install db-postgres bitnami/postgresql -f ./k8s/helms/dbs/postgres-values.yaml --namespace staging

# Deploy Neo4j
echo "Deploying Neo4j..."
# kubectl apply -k k8s/overlays/staging/database/db-neo4j/ TODO: using kustomize.
# kubectl apply -f k8s/helms/shared/db-neo4j-configmap.yaml
helm install neo4j ./k8s/helms/neo4j --namespace staging

# Deploy Web App
# echo "Deploying Web App..."
# helm install web-app ./k8s/web-app --namespace staging --set deployment.webApp.image.tag=$COMMIT_HASH

echo "All services deployed successfully."

# ./deploy-all.sh
# k8s/scripts/deploy-all.sh