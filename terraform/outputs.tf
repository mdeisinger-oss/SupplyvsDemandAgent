output "cloud_run_service_url" {
  description = "Public HTTPS URL of the deployed MD-Supply-vs-Demand-Agent service"
  value       = google_cloud_run_v2_service.md_supply_demand_service.uri
}

output "service_account_email" {
  description = "Runtime IAM Service Account for MD-Supply-vs-Demand-Agent"
  value       = google_service_account.agent_runtime_sa.email
}

output "secret_manager_secret_id" {
  description = "Secret Manager secret ID storing the Gemini API key"
  value       = google_secret_manager_secret.gemini_api_key.secret_id
}
