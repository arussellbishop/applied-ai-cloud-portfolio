variable "location" {
  type    = string
  default = "northeurope"
}
variable "admin_username" {
  type    = string
  default = "platformoperator"
}
variable "ssh_public_key" {
  type        = string
  description = "Operator-owned public SSH key only; private key never enters Terraform."
}
variable "vm_size" {
  type    = string
  default = "Standard_B1ms"
  validation {
    condition     = var.vm_size == "Standard_B1ms"
    error_message = "Reference sizing is intentionally bounded to B1ms (not equivalent CPU to Lightsail)."
  }
}
variable "tags" {
  type    = map(string)
  default = {}
}
module "contract" {
  source = "../container_host"
}
resource "azurerm_resource_group" "host" {
  name     = "${var.name}-rg"
  location = var.location
  tags = merge(var.tags, {
    purpose = "reference-only"
  })
}
resource "azurerm_virtual_network" "host" {
  name                = "${var.name}-vnet"
  location            = var.location
  resource_group_name = azurerm_resource_group.host.name
  address_space       = ["10.42.0.0/16"]
  tags                = var.tags
}
resource "azurerm_subnet" "host" {
  name                 = "application"
  resource_group_name  = azurerm_resource_group.host.name
  virtual_network_name = azurerm_virtual_network.host.name
  address_prefixes     = ["10.42.1.0/24"]
}
resource "azurerm_network_security_group" "host" {
  name                = "${var.name}-nsg"
  location            = var.location
  resource_group_name = azurerm_resource_group.host.name
  tags                = var.tags
  security_rule {
    name                       = "public-http"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"

  }
  security_rule {
    name                       = "restricted-management"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefixes    = var.ssh_source_cidrs
    destination_address_prefix = "*"

  }
  # Override the default AllowVNetInBound rule: unrelated VNet peers gain no ingress.
  security_rule {
    name                       = "deny-other-ingress"
    priority                   = 4000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"

  }
}
resource "azurerm_subnet_network_security_group_association" "host" {
  subnet_id                 = azurerm_subnet.host.id
  network_security_group_id = azurerm_network_security_group.host.id
}
resource "azurerm_public_ip" "host" {
  name                = "${var.name}-ipv4"
  location            = var.location
  resource_group_name = azurerm_resource_group.host.name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = var.tags
}
resource "azurerm_network_interface" "host" {
  name                = "${var.name}-nic"
  location            = var.location
  resource_group_name = azurerm_resource_group.host.name
  tags                = var.tags
  ip_configuration {
    name                          = "primary"
    subnet_id                     = azurerm_subnet.host.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.host.id
  }
}
resource "azurerm_linux_virtual_machine" "host" {
  name                            = var.name
  location                        = var.location
  resource_group_name             = azurerm_resource_group.host.name
  size                            = var.vm_size
  admin_username                  = var.admin_username
  disable_password_authentication = true
  network_interface_ids           = [azurerm_network_interface.host.id]
  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 30
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }
  secure_boot_enabled = true
  vtpm_enabled        = true
  custom_data         = base64encode(module.contract.cloud_init)
  tags = merge(var.tags, {
    purpose = "reference-only"
  })
  depends_on = [azurerm_subnet_network_security_group_association.host]
}
output "public_ipv4" {
  value     = azurerm_public_ip.host.ip_address
  sensitive = true
}
output "host_name" {
  value = azurerm_linux_virtual_machine.host.name
}
output "host_contract" {
  value = module.contract.contract
}
