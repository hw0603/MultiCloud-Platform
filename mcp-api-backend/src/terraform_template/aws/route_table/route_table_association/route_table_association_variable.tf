# Route Table Association
variable "aws_subnet_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws subnet name"
}


variable "aws_route_table_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws rt name"
}


# Provider setting

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}


