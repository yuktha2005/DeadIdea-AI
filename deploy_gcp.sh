#!/bin/bash
# PHOENIX PROTOCOL - Automated Deployment Script for Google Cloud Platform
# Purpose: This script automates the build and deployment of DeadIdea AI to Google Cloud Run.
# Usage: ./deploy_gcp.sh YOUR_PROJECT_ID

if [ -z "$1" ]; then
    echo "Usage: ./deploy_gcp.sh [PROJECT_ID]"
    exit 1
fi

PROJECT_ID=$1
SERVICE_NAME="deadidea-ai"
REGION="us-central1"

echo "🚀 Initiating Phoenix Protocol: Cloud Deployment..."

# 1. Enable Required Google Cloud APIs
echo "📡 Enabling Google Cloud APIs..."
gcloud services enable run.googleapis.com containerregistry.googleapis.com aiplatform.googleapis.com

# 2. Build the Container Image using Google Cloud Build
echo "🏗️ Building Container Image on Google Cloud..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 3. Deploy to Google Cloud Run (IaC approach using flags)
echo "☁️ Deploying to Google Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars="API_URL=http://localhost:8000" \
    --description="DeadIdea AI - The Phoenix Protocol"

echo "✅ Phoenix Protocol Deployment Complete."
echo "🔗 Access your dashboard at the URL provided above."
