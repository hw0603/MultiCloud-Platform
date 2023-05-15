# Subnet
variable "aws_subnet_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws subnet name"
}

variable "aws_cidr"    { default = "10.0.0.0/24" }

variable "aws_subnet_region" {
    type = string
    description = "SUBNET 을 생성할 Availability Zone을 입력하세요."
    default = "ap-northeast-2a"
}

variable "public_ip_launch_flag" {
    type = bool
    description = "public subnet (true) / private subnet(false) 여부를 true/false로 입력하세요"
    default = false
}



# Dependency

# VPC
variable "aws_vpc_name" {
    type = string
    description = "subnet을 생성할 vpc 이름을 입력하세요."
    default = "aws vpc name"
}


# Provider Setting

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}
