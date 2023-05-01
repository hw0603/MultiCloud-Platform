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
    map_public_ip_on_launch = true
    availability_zone = var.aws_region
    tags = {
        Name = var.aws_subnet_name
    }
}

resource "aws_subnet" "subnet4" {
    vpc_id = aws_vpc.vpc.id
    cidr_block = var.aws_vpc_cidr
    map_public_ip_on_launch = true
    availability_zone = var.aws_region
    tags = {
        Name = var.aws_subnet_name
    }
}
