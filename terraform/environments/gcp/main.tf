variable "project_id" {
  type = string
}
variable "ssh_source_cidrs" {
  type = list(string)
}
provider "google" {
  project = var.project_id
  region  = "europe-west1"
}
module "platform" {
  source           = "../../modules/gcp_host"
  project_id       = var.project_id
  ssh_source_cidrs = var.ssh_source_cidrs
}
output "reference_host" {
  value = module.platform.host_name
}
