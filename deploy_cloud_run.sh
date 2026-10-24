#!/usr/bin/env bash
# =============================================================================
# Automated Deployment Script using ADK CLI (`adk deploy cloud_run`) & gcloud
# =============================================================================
set -euo pipefail

PROJECT_ID="${1:-${GOOGLE_CLOUD_PROJECT:-your-gcp-project-id}}"
REGION="${2:-europe-west3}"
SERVICE_NAME="md-supply-vs-demand-agent"

echo "=== 1. Running Golden Dataset Regression Suite Before Deployment ==="
python3 eval/run_evaluation.py

echo "=== 2. Deploying via Google ADK CLI (or gcloud Cloud Run fallback) ==="
if command -v adk >/dev/null 2>&1; then
  adk deploy cloud_run \
    --project="${PROJECT_ID}" \
    --region="${REGION}" \
    --service_name="${SERVICE_NAME}" \
    md_supply_demand_agent
else
  gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --project "${PROJECT_ID}" \
    --region "${REGION}" \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${REGION}"
fi
