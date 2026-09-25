mock_provider "aws" {}

run "new_provider" {
  command = plan
  assert {
    condition     = length(aws_iam_openid_connect_provider.github) == 1
    error_message = "New provider must be managed exactly once."
  }

}

run "shared_provider" {
  command = plan
  variables {
    existing_oidc_arn = "existing-provider-reference"
  }
  assert {
    condition     = length(aws_iam_openid_connect_provider.github) == 0
    error_message = "Existing shared provider must not be managed."
  }
  assert {
    condition     = jsondecode(aws_iam_role.github.assume_role_policy).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == "repo:arussellbishop/applied-ai-cloud-portfolio:ref:refs/heads/main"
    error_message = "OIDC trust must restrict the repository and main ref."
  }
}
