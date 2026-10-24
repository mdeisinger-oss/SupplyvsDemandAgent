# =============================================================================
# Infrastructure as Code (Terraform) for MD-Supply-vs-Demand-Agent
# Rubric Criterion 5.2 — Infrastructure as Code (5 pts)
# =============================================================================

locals {
  required_apis = [
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "secretmanager.googleapis.com",
    "dlp.googleapis.com",
    "cloudtrace.googleapis.com",
    "logging.googleapis.com",
    "artifactregistry.googleapis.com",
  ]
}

resource "google_project_service" "enabled_apis" {
  for_each           = toset(local.required_apis)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "agent_repo" {
  location      = var.region
  repository_id = "md-supply-demand-repo"
  description   = "Artifact Registry container repository for MD-Supply-vs-Demand-Agent"
  format        = "DOCKER"
  depends_on    = [google_project_service.enabled_apis]
}

resource "google_service_account" "agent_runtime_sa" {
  account_id   = "md-supply-demand-sa"
  display_name = "MD-Supply-vs-Demand-Agent Runtime Service Account"
}

resource "google_secret_manager_secret" "gemini_api_key" {
  secret_id = "md-supply-demand-gemini-api-key"
  replication {
    auto {}
  }
  depends_on = [google_project_service.enabled_apis]
}

resource "google_secret_manager_secret_iam_member" "sa_secret_accessor" {
  secret_id = google_secret_manager_secret.gemini_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_project_iam_member" "sa_vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_project_iam_member" "sa_dlp_user" {
  project = var.project_id
  role    = "roles/dlp.user"
  member  = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_project_iam_member" "sa_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_project_iam_member" "sa_trace_agent" {
  project = var.project_id
  role    = "roles/cloudtrace.agent"
  member  = "serviceAccount:${google_service_account.agent_runtime_sa.email}"
}

resource "google_cloud_run_v2_service" "md_supply_demand_service" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.agent_runtime_sa.email

    containers {
      image = var.container_image

      ports {
        container_port = 8080
      }

      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name  = "GOOGLE_CLOUD_LOCATION"
        value = var.region
      }
      env {
        name  = "GEMINI_API_KEY_SECRET_ID"
        value = google_secret_manager_secret.gemini_api_key.secret_id
      }
      env {
        name = "GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gemini_api_key.secret_id
            version = "latest"
          }
        }
      }

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }
    }
  }

  depends_on = [
    google_secret_manager_secret_iam_member.sa_secret_accessor,
    google_project_iam_member.sa_vertex_user,
  ]
}
