# VPC
resource "aws_vpc" "vpc" {
    cidr_block = var.aws_vpc_cidr
    enable_dns_support = true
    enable_dns_hostnames = true

    tags = {
        Name = var.aws_vpc_name
    }
}
