# Mock provider only. No API calls, credentials, backend or infrastructure.
mock_provider "aws" {}
variables {
  ssh_source_cidrs = ["10.42.0.10/32"] # Synthetic fixture, not a deployed management address.
  key_pair_name    = "mock-existing-key"
}
run "reference_contract" {
  command = plan
  assert {
    condition     = module.platform.host_name == "portfolio-reference"
    error_message = "Reference must not reuse live production identity."
  }
  assert {
    condition     = length(module.platform.host_contract.container_controls) == 5
    error_message = "Shared runtime control contract changed."
  }
  assert {
    condition     = strcontains(module.platform.host_contract.private_backends, "no published")
    error_message = "Backends must remain private."
  }
}
