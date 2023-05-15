variable "aws_alb_target_group_name" {
    type = string
    default = "aws alb target group name"
}

variable "aws_alb_target_group_port" {
    type = number
    default = 80
}

variable "aws_alb_target_group_protocol" {
    type = string
    default = "HTTP"
}

variable "aws_alb_target_instance_name" {
    type = string
    default = "aws bastion ec2 name"
}

variable "aws_alb_security_group_name" {
    type = list
    description = "SECURITY GROUP 이름을 특수문자 없이 입력하세요."
    default = ["aws security group name"]
}

# Dependency
variable "aws_vpc_name" {
    type = string
    description = "VPC 이름을 특수문자 없이 입력하세요."
    default = "aws vpc name"
}

variable "aws_security_group_name_list" {
    type = list
    description = "SECURITY GROUP 이름을 특수문자 없이 입력하세요. (list)"
    default = ["aws security group name"]
}

variable "aws_subnet_name_list" {
    type = list
    description = "SUBNET 이름을 특수문자 없이 입력하세요. (list)"
    default = ["aws subnet name"]
}

# Provider setting

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}