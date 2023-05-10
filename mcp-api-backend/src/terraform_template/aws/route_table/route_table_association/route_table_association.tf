# route table을 subnet에 연결
resource "aws_route_table_association" "rt_association" {
    subnet_id = data.aws_subnet.selected_subnet.id
    route_table_id = data.aws_route_table.selected_rt.id
}


# Dependency
data "aws_subnet" "selected_subnet" {
    filter {
        name   = "tag:Name"
        values = [var.aws_subnet_name]
    }
}

data "aws_route_table" "selected_rt" {
    filter {
        name   = "tag:Name"
        values = [var.aws_route_table_name]
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