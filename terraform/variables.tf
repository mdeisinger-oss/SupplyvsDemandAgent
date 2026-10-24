variable "project_id" {
  description = "Google Cloud Project ID hosting MD-Supply-vs-Demand-Agent"
  type        = string
}

variable "region" {
  description = "Primary Google Cloud region for Cloud Run and Vertex AI deployment"
  type        = string
  default     = "europe-west3"
}

variable "service_name" {
  description = "Cloud Run service name for MD-Supply-vs-Demand-Agent"
  type        = string
  default     = "md-supply-vs-demand-agent"
}

variable "container_image" {
  description = "Container image URI in Artifact Registry"
  type        = string
  default     = "europe-west3-docker.pkg.dev/my-gcp-project/md-agent-repo/md-supply-vs-demand-agent:latest"
}
