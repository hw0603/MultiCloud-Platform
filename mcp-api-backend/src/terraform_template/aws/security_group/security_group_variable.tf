# Security_group
variable "aws_security_group_name" {
    type = string
    description = "SECURITY GROUP 이름을 특수문자 없이 입력하세요."
    default = "aws security group name"
}

variable "aws_inbound_from_port" {
    type = number
    description = "Inbound 의 from Port 를 입력하세요."
    default = 80
}

variable "aws_inbound_to_port" {
    type = number
    description = "Inbound 의 to Port 를 입력하세요."
    default = 80
}

variable "aws_outbound_from_port" {
    type = number
    description = "Outbound 의 from Port 를 입력하세요."
    default = 80
}

variable "aws_outbound_to_port" {
    type = number
    description = "Outbound 의 to Port 를 입력하세요."
    default = 80
}

variable "aws_inbound_protocol" {
    type = string
    description = "Inbound Protocol 을 입력하세요."
    default = "tcp"
}

variable "aws_outbound_protocol" {
    type = string
    description = "Outbound Protocol 을 입력하세요."
    default = "tcp"
}

variable "aws_inbound_cidr_list" {
    type = list
    description = "Inbound Cidr 을 입력하세요."
    default = ["0.0.0.0/0"]
}

variable "aws_outbound_cidr_list" {
    type = list
    description = "Outbound Cidr 을 입력하세요."
    default = ["0.0.0.0/0"]
}


# Dependency
variable "aws_vpc_name" {
    type = string
    description = "VPC 이름을 특수문자 없이 입력하세요."
    default = "aws vpc name"
}


# Provider setting

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}
