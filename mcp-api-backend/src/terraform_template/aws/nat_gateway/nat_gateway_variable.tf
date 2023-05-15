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

# dependency
variable "aws_internet_gateway_name" {
    type = string
    default = "aws igw name"
}

variable "aws_subnet_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws subnet name"
}

# access_key

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}
