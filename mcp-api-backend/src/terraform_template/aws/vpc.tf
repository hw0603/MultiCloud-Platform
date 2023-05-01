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


# NAT Gateway
resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_gateway.id
  subnet_id     = aws_subnet1.id
  depends_on    = [aws_internet_gateway.igw]

  tags = {
    Name = var.aws_nat_gateway_name
  }
}

resource "aws_eip" "nat_gateway" {
  vpc        = true
  depends_on = [aws_internet_gateway.igw]

  tags = {
    Name = var.aws_nat_gateway_eip_name
  }
}
