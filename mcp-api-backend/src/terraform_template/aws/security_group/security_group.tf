# Security Group
resource "aws_security_group" "security_group" {
    vpc_id = data.aws_vpc.selected_vpc.id

    ingress {
        from_port = var.aws_inbound_from_port
        to_port = var.aws_inbound_to_port
        protocol = var.aws_inbound_protocol
        cidr_blocks = var.aws_inbound_cidr_list
    }

    egress {
        from_port = var.aws_outbound_from_port
        to_port = var.aws_outbound_to_port
        protocol = var.aws_outbound_protocol
        cidr_blocks = var.aws_outbound_cidr_list
    }

  tags = {
    Name = var.aws_security_group_name
  }
}


# Dependency
data "aws_vpc" "selected_vpc" {
    filter {
        name   = "tag:Name"
        values = [var.aws_vpc_name]
    }
}


# Provider Setting
provider "aws" {
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
    region = var.aws_region
}

terraform {
    required_version = ">=1.0.0"
}