# Route Rule 생성
resource "aws_route" "route_rule" {
  route_table_id = data.aws_route_table.selected_rt.id
  destination_cidr_block = var.destination_cidr
  gateway_id = data.aws_internet_gateway.selected_igw.id
}


# Dependency
data "aws_route_table" "selected_rt" {
  filter {
    name   = "tag:Name"
    values = [var.aws_route_table_name]
  }
}

data "aws_internet_gateway" "selected_igw" {
  filter {
    name   = "tag:Name"
    values = [var.aws_internet_gateway_name]
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