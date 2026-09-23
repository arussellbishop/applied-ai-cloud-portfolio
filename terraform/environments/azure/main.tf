variable "subscription_id" {
  type        = string
  description = "Existing subscription only, if separately authorized; never needed for validate."
}
variable "ssh_source_cidrs" {
  type = list(string)
}
variable "ssh_public_key" {
  type = string
}
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
module "platform" {
  source           = "../../modules/azure_host"
  ssh_source_cidrs = var.ssh_source_cidrs
  ssh_public_key   = var.ssh_public_key
  tags = {
    project = "portfolio", environment = "reference"
  }
}
output "reference_host" {
  value = module.platform.host_name
}
