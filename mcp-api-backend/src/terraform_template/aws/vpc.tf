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


# Route Table
# subnet public1~2
resource "aws_route_table" "rt1" {
    vpc_id = aws_vpc.vpc.id
    
    tags = {
        Name = var.aws_route_table_name
    }
}

resource "aws_route_table_association" "rt1" {
    subnet_id = aws_subnet.subnet1.id
    route_table_id = aws_route_table.rt1.id
}

resource "aws_route_table_association" "rt2" {
    subnet_id = aws_subnet.subnet2.id
    route_table_id = aws_route_table.rt1.id
}

resource "aws_route" "rt1" {
  route_table_id         = aws_route_table.rt1.id
  gateway_id             = aws_internet_gateway.igw.id
  destination_cidr_block = "0.0.0.0/0"
}

# subnet public3~4
resource "aws_route_table" "rt3" {
    vpc_id = aws_vpc.vpc.id
    
    tags = {
        Name = var.aws_route_table_name
    }
}

resource "aws_route_table_association" "rt3" {
    subnet_id = aws_subnet.subnet3.id
    route_table_id = aws_route_table.rt3.id
}

resource "aws_route_table_association" "rt4" {
    subnet_id = aws_subnet.subnet4.id
    route_table_id = aws_route_table.rt4.id
}

resource "aws_route" "rt3" {
  route_table_id         = aws_route_table.rt3.id
  gateway_id             = aws_internet_gateway.igw.id
  destination_cidr_block = "0.0.0.0/0"
}
