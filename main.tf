# AWS Provider Configuration
provider "aws" {
  region = "eu-west-1"
}

# Terraform Settings
terraform {
  required_version = ">= 1.1.1"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.37"
    }
  }
}

# Local Variables for SSM Parameters
locals {
  parameters = {
    token = {
      value       = "secret123123!!!"
      type        = "SecureString"
      tier        = "Advanced"
      description = "token"
    }
    apiKey = {
      value       = "secret123123!!!"
      type        = "SecureString"
      tier        = "Advanced"
      description = "apiKey"
    }
  }
}

# Module to Create SSM Parameters
module "multiple" {
  source  = "terraform-aws-modules/ssm-parameter/aws"

  for_each = local.parameters

  name            = each.key
  value           = each.value.value
  type            = each.value.type
  description     = each.value.description
  tier            = each.value.tier
}
