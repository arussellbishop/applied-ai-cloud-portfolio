# Azure validated reference

REFERENCE_ONLY_NOT_DEPLOYED. The module declares a resource group, dedicated VNet/subnet, subnet NSG, Standard static public IP, NIC and small Linux VM. B1ms is a low-cost burstable reference, not CPU-equivalent to the live 2-vCPU host; suitability depends on credits and measured memory. No subscription or credentials are created or requested.

HTTP is allowed from the Internet only on TCP 80. SSH is allowed only from required explicit /32 sources. A final deny rule overrides Azure's default inbound VNet allowance. Wildcard source ports allow ephemeral client ports; wildcard destinations scope to this dedicated subnet, not arbitrary authorization. The VM uses an externally provided public SSH key with password authentication disabled, secure boot and vTPM. No VM identity or RBAC grants are created. Provider-managed OS-disk encryption is the baseline.

The shared cloud-init contract does not install the runtime or configure deployment credentials. Azure-specific guest compatibility, trusted launch/SKU/image support, outbound package access, IAM and blue/green bootstrap would require future live testing. Provider validation cannot guarantee regional capacity or a chosen image's continued availability. No VM, disk, IP, VNet, NSG or resource group has been deployed.

Azure VM compute, managed disk, Standard public IPv4 and egress can be billed separately. Stopping/deallocating compute would not by itself remove all costs; this phase creates none. No load balancer, NAT gateway, database or log workspace is modeled.

Source: [AzureRM Linux VM](https://registry.terraform.io/providers/hashicorp/azurerm/5.6.0/docs/resources/linux_virtual_machine).
