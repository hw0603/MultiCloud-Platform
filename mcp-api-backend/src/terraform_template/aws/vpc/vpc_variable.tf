# VPC
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

# Internet Gateway
variable "aws_internet_gateway_name" {
    type = string
    description = "INTERNET GATEWAY 이름을 특수문자 없이 입력하세요."
    default = "aws igw name"
}


# Provider Setting

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}