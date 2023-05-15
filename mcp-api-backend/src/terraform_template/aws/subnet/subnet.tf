# Subnet
resource "aws_subnet" "subnet" {
    vpc_id = data.aws_vpc.selected_vpc.id
    cidr_block = var.aws_cidr
    map_public_ip_on_launch = var.public_ip_launch_flag
    availability_zone = var.aws_subnet_region
    tags = {
        Name = var.aws_subnet_name
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

