#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Retrieve the latest commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)
echo "Using commit hash: $COMMIT_HASH"

# Create Namespace
echo "Creating namespace..."
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
EOF

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
kubectl apply -k k8s/overlays/staging/database/db-neo4j/

# Deploy Web App
echo "Deploying Web App..."
helm install web-app ./k8s/web-app --namespace staging --set deployment.webApp.image.tag=$COMMIT_HASH

echo "All services deployed successfully."


# k8s/scripts/deploy-all.sh