variable "name" {
  description = "Unique reference deployment name; never reuse the live host name."
  type        = string
  default     = "portfolio-reference"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,30}$", var.name))
    error_message = "Use 3-31 lowercase letters, digits or hyphens, starting with a letter."

  }
}
variable "ssh_source_cidrs" {
  description = "Explicit operator/runner public IPv4 /32 allowlist; never world-open SSH. No real values committed."
  type        = list(string)
  validation {
    condition     = length(var.ssh_source_cidrs) > 0 && alltrue([for cidr in var.ssh_source_cidrs : can(cidrnetmask(cidr)) && endswith(cidr, "/32") && !startswith(cidr, "0.") && !startswith(cidr, "127.")])
    error_message = "Supply at least one valid non-loopback IPv4 /32 management source."

  }
}
