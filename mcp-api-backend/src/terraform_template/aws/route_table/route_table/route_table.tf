# Route Table 생성
resource "aws_route_table" "rt" {
    vpc_id = data.aws_vpc.selected_vpc.id

    tags = {
        Name = var.aws_route_table_name
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