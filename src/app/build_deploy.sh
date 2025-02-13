#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 4 ]; then
  echo "Usage: $0 <image_name> <region> <repository> <project_id>"
  exit 1
fi

IMAGE_NAME=$1
REGION=$2
REPOSITORY=$3
PROJECT_ID=$4

# Construct the full image path
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:latest"

gcloud builds submit --tag $IMAGE_URI

# Deploy to Cloud Run
gcloud run deploy "${IMAGE_NAME}" \
  --image "${IMAGE_URI}" \
  --platform managed \
  --region "${REGION}" \
  --port 8080 \
  --allow-unauthenticated
