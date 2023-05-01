# VPC
resource "aws_vpc" "vpc" {
    cidr_block = var.aws_vpc_cidr
    enable_dns_support = true
    enable_dns_hostnames = true

    tags = {
        Name = var.aws_vpc_name
    }
}

# Subnet
resource "aws_subnet" "subnet1" {
    vpc_id = aws_vpc.vpc.id
    cir_block = var.aws_vpc_cidr
    map_public_ip_on_launch = true
    availability_zone = var.aws_region
    tags = {
        Name = var.aws_subnet_name
    }
}

resource "aws_subnet" "subnet2" {
    vpc_id = aws_vpc.vpc.id
    cidr_block = var.aws_vpc_cidr
    map_public_ip_on_launch = true
    availability_zone = var.aws_region
    tags = {
        Name = var.aws_subnet_name
    }
}

resource "aws_subnet" "subnet3" {
    vpc_id = aws_vpc.vpc.id
    cidr_block = var.aws_vpc_cidr
    map_public_ip_on_launch = false
    availability_zone = var.aws_region
    tags = {
        Name = var.aws_subnet_name
    }
}

resource "aws_subnet" "subnet4" {
    vpc_id = aws_vpc.vpc.id
    cidr_block = var.aws_vpc_cidr
    map_public_ip_on_launch = false
    availability_zone = var.aws_region
    tags = {
        Name = var.aws_subnet_name
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
  subnet_id     = aws_subnet.subnet1.id
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

