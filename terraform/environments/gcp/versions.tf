terraform {
  required_version = ">= 1.14.7, < 1.15.0"
  required_providers {
    google = {
      source = "hashicorp/google", version = "= 8.4.0"
    }

  }
}
