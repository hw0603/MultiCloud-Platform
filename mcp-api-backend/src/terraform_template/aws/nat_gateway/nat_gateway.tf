# NAT Gateway
resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_gateway.id
  subnet_id     = data.aws_subnet.selected_subnet.id
  depends_on    = [data.aws_internet_gateway.selected_igw]

  tags = {
    Name = var.aws_nat_gateway_name
  }
}

# Elastic IP
resource "aws_eip" "nat_gateway" {
  vpc        = true
  depends_on = [data.aws_internet_gateway.selected_igw]

  tags = {
    Name = var.aws_nat_gateway_eip_name
  }
}


# Dependency
data "aws_internet_gateway" "selected_igw" {
  filter {
      name   = "tag:Name"
      values = [var.aws_internet_gateway_name]
  }
}

data "aws_subnet" "selected_subnet" {
  filter {
    name   = "tag:Name"
    values = [var.aws_subnet_name]
  }
}


# Provider setting
provider "aws" {
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
    region = var.aws_region
}

terraform {
    required_version = ">=1.0.0"
}