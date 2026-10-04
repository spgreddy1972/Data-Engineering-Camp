terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "8.5.0"
    }
  }
}

provider "google" {
  #credentials = '/home/osboxes/terraform-demo/keys/gcp-creds.json'
  project = "fluted-curve-510606-v6"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket"{
  name          = "fluted-curve-510606-v6-demo-bucket"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}