# access_key
variable "aws_access_key" {
    type = string
    default = ""
}

# secret_key
variable "aws_secret_key" {
    type = string
    default = ""
}

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}

# subnet region
variable "aws_subnet_region" {
    type = string
    default = "ap-northeast-2a"
}


# key_name
variable "aws_key_name" {
    type = string
    default = "key-pair"
}

# public_key
variable "aws_public_key_name" {
    type = string
    description = "SSH 키를 입력해주세요."
    default = "key-04267ebefb1c15928"
}


# vpc
variable "aws_vpc_cidr" {
    type = string
    description = "허용된 CIDR 블록 사이즈는 입니다."
    default = "10.0.0.0/16"
}

variable "aws_vpc_name" {
    type = string
    description = "VPC 이름을 특수문자 없이 입력하세요."
    default = "aws vpc name"
}


# CIDR
variable "aws_cidr1"    { default = "10.0.0.0/24" }
variable "aws_cidr2"    { default = "10.0.1.0/24" }
variable "aws_cidr3"    { default = "10.0.2.0/24" }
variable "aws_cidr4"    { default = "10.0.3.0/24" }


# subnet
variable "aws_subnet_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws subnet name"
}


# Internet Gateway
variable "aws_internet_gateway_name" {
    type = string
    description = "INTERNET GATEWAY 이름을 특수문자 없이 입력하세요."
    default = "aws igw name"
}


# NAT Gateway
variable "aws_nat_gateway_name" {
    type = string
    description = "NAT GATEWAY 이름을 특수문자 없이 입력하세요."
    default = "aws nat-igw name"
}

variable "aws_nat_gateway_eip_name" {
    type = string
    description = "NAT GATEWAY EIP 이름을 특수문자 없이 입력하세요."
    default = "aws nat-igw-eip name"
}


# Route Table
variable "aws_route_table_name" {
    type = string
    description = "ROUTE TABLE 이름을 특수문자 없이 입력하세요."
    default = "aws rt name"
}


# security_group
variable "aws_security_group_name" {
    type = string
    description = "SECURITY GROUP 이름을 특수문자 없이 입력하세요."
    default = "aws security group name"
}


# inbound from port
variable "aws_inbound_from_port" {
    type = number
    description = "Inbound 의 from Port 를 입력하세요."
    default = 80
}


# inbound to port
variable "aws_inbound_to_port" {
    type = number
    description = "Inbound 의 to Port 를 입력하세요."
    default = 80
}


# outbound from port
variable "aws_outbound_from_port" {
    type = number
    description = "Outbound 의 from Port 를 입력하세요."
    default = 80
}


# outbound to port
variable "aws_outbound_to_port" {
    type = number
    description = "Outbound 의 to Port 를 입력하세요."
    default = 80
}


# inbound protocol
variable "aws_inbound_protocol" {
    type = string
    description = "Inbound Protocol 을 입력하세요."
    default = "tcp"
}


# outbound protocol
variable "aws_outbound_protocol" {
    type = string
    description = "Outbound Protocol 을 입력하세요."
    default = "tcp"
}


# inbound cidr
variable "aws_inbound_cidr" {
    type = string
    description = "Inbound Cidr 을 입력하세요."
    default = "0.0.0.0/0"
}


# outbound cidr
variable "aws_outbound_cidr" {
    type = string
    description = "Outbound Cidr 을 입력하세요."
    default = "0.0.0.0/0"
}

# bastion
variable "aws_bastion_eip" {
    type = string
    default = "aws bastion eip name"
}

variable "aws_bastion_ami" {
    type = string
    default = "ami-04cebc8d6c4f297a3"
}

variable "aws_bastion_instance_type" {
    type = string
    default = "t2.micro"
}

variable "aws_bastion_key_name" {
    type = string
    default = "key-pair"
}

variable "aws_bastion_volumne_size" {
    default = 8
}

variable "aws_bastion_ec2_name" {
    type = string
    default = "aws bastion ec2 name"
}
