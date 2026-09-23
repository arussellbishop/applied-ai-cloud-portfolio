variable "project_id" {
  type        = string
  description = "Existing project identifier supplied externally; this reference creates no project."
}
variable "region" {
  type    = string
  default = "europe-west1"
}
variable "zone" {
  type    = string
  default = "europe-west1-b"
}
variable "machine_type" {
  type    = string
  default = "e2-small"
  validation {
    condition     = var.machine_type == "e2-small"
    error_message = "Reference sizing is intentionally bounded to e2-small shared CPU."
  }
}
module "contract" {
  source = "../container_host"
}
resource "google_compute_network" "host" {
  project                 = var.project_id
  name                    = "${var.name}-vpc"
  auto_create_subnetworks = false
}
resource "google_compute_subnetwork" "host" {
  project                  = var.project_id
  name                     = "${var.name}-subnet"
  region                   = var.region
  ip_cidr_range            = "10.43.1.0/24"
  network                  = google_compute_network.host.id
  private_ip_google_access = true
}
resource "google_compute_firewall" "http" {
  project       = var.project_id
  name          = "${var.name}-http"
  network       = google_compute_network.host.name
  direction     = "INGRESS"
  source_ranges = ["0.0.0.0/0"]
  target_tags   = [var.name]
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }
}
resource "google_compute_firewall" "ssh" {
  project       = var.project_id
  name          = "${var.name}-ssh"
  network       = google_compute_network.host.name
  direction     = "INGRESS"
  source_ranges = var.ssh_source_cidrs
  target_tags   = [var.name]
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
resource "google_compute_address" "host" {
  project      = var.project_id
  name         = "${var.name}-ipv4"
  region       = var.region
  address_type = "EXTERNAL"
  network_tier = "STANDARD"
}
resource "google_service_account" "host" {
  project      = var.project_id
  account_id   = "${var.name}-vm"
  display_name = "Reference host without project IAM grants"
}
resource "google_compute_instance" "host" {
  project      = var.project_id
  name         = var.name
  zone         = var.zone
  machine_type = var.machine_type
  tags         = [var.name]
  labels = {
    purpose = "reference-only", managed_by = "terraform"
  }
  can_ip_forward            = false
  allow_stopping_for_update = true
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2404-lts-amd64"
      type  = "pd-standard"
      size  = 20
    }
  }
  network_interface {
    subnetwork = google_compute_subnetwork.host.id
    access_config {
      nat_ip       = google_compute_address.host.address
      network_tier = "STANDARD"
    }

  }
  metadata = {
    "enable-oslogin"         = true
    "block-project-ssh-keys" = true
    "serial-port-enable"     = false
    "user-data"              = module.contract.cloud_init
  }
  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }
  service_account {
    email  = google_service_account.host.email
    scopes = ["https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write"]
  }
  depends_on = [google_compute_firewall.http, google_compute_firewall.ssh]
}
output "public_ipv4" {
  value     = google_compute_address.host.address
  sensitive = true
}
output "host_name" {
  value = google_compute_instance.host.name
}
output "host_contract" {
  value = module.contract.contract
}
