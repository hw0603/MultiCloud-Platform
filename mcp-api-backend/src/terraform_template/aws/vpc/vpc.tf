# VPC
resource "aws_vpc" "vpc" {

    cidr_block = var.aws_vpc_cidr
    enable_dns_support = true
    enable_dns_hostnames = true

    tags = {
        Name = var.aws_vpc_name
    }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.vpc.id

    tags = {
        Name = var.aws_internet_gateway_name
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
