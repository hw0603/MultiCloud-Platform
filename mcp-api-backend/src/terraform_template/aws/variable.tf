# access_key
variable "aws_access_key" {
    type = string
}

# secret_key
variable "aws_secret_key" {
    type = string
}

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}


# key_name
variable "aws_key_name" {
    type = string
    default = "web_admin"
}

# public_key
variable "aws_public_key_name" {
    type = string
    description = "SSH 키를 입력해주세요."
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
