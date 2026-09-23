variable "availability_zone" {
  type = string
}
variable "key_pair_name" {
  type        = string
  description = "Existing operator-managed Lightsail public key-pair name; no key generation or private material."
}
variable "blueprint_id" {
  type    = string
  default = "ubuntu_24_04"
}
variable "bundle_id" {
  type        = string
  default     = "small_3_0"
  description = "Reference 2-vCPU / 2-GiB bundle. Confirm regional catalogue before any separately authorized use."
  validation {
    condition     = var.bundle_id == "small_3_0"
    error_message = "This cost-bounded reference permits only the small_3_0 bundle."
  }
}
variable "tags" {
  type    = map(string)
  default = {}
}
module "contract" {
  source = "../container_host"
}
resource "aws_lightsail_instance" "host" {
  name              = var.name
  availability_zone = var.availability_zone
  blueprint_id      = var.blueprint_id
  bundle_id         = var.bundle_id
  key_pair_name     = var.key_pair_name
  ip_address_type   = "ipv4"
  user_data         = module.contract.cloud_init
  tags = merge(var.tags, {
    Purpose = "reference-only", ManagedBy = "Terraform"
  })
}
resource "aws_lightsail_static_ip" "host" {
  name = "${var.name}-ipv4"
}
resource "aws_lightsail_static_ip_attachment" "host" {
  static_ip_name = aws_lightsail_static_ip.host.id
  instance_name  = aws_lightsail_instance.host.id
}
resource "aws_lightsail_instance_public_ports" "host" {
  instance_name = aws_lightsail_instance.host.name
  port_info {
    protocol  = "tcp"
    from_port = 80
    to_port   = 80
    cidrs     = ["0.0.0.0/0"]
  }
  port_info {
    protocol  = "tcp"
    from_port = 22
    to_port   = 22
    cidrs     = var.ssh_source_cidrs
  }
}
output "public_ipv4" {
  value     = aws_lightsail_static_ip.host.ip_address
  sensitive = true
}
output "host_name" {
  value = aws_lightsail_instance.host.name
}
output "host_contract" {
  value = module.contract.contract
}
