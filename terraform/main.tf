terraform {
  required_version = ">= 1.5.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.38"
    }
  }
}

provider "kubernetes" {
  config_path    = pathexpand("~/.kube/config")
  config_context = "kind-ticket-tracker-cluster"
}

resource "kubernetes_resource_quota_v1" "ticket_tracker_quota" {
  metadata {
    name      = "ticket-tracker-quota"
    namespace = "ticket-tracker"
  }

  spec {
    hard = {
      pods                   = "10"
      persistentvolumeclaims = "2"
      "requests.storage"     = "2Gi"
    }
  }
}
