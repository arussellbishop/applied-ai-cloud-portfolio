variable "region" {
  type    = string
  default = "eu-north-1"
}
variable "availability_zone" {
  type    = string
  default = "eu-north-1a"
}
variable "ssh_source_cidrs" {
  type = list(string)
}
variable "key_pair_name" {
  type = string
}
provider "aws" {
  region = var.region
}
module "platform" {
  source            = "../../modules/aws_lightsail"
  availability_zone = var.availability_zone
  key_pair_name     = var.key_pair_name
  ssh_source_cidrs  = var.ssh_source_cidrs
  tags = {
    Project = "portfolio", Environment = "reference"
  }
}
output "reference_host" {
  value = module.platform.host_name
}
