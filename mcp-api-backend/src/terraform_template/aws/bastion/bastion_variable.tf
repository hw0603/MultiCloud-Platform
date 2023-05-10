
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


# Dependency
variable "aws_subnet_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws subnet name"
}

variable "aws_security_group_name" {
    type = list
    description = "SECURITY GROUP 이름을 특수문자 없이 입력하세요. (list)"
    default = ["aws security group name"]
}


# Provider setting

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}