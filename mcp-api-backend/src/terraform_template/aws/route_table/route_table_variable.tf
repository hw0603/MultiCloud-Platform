# Route Table
variable "aws_route_table_name" {
    type = string
    description = "ROUTE TABLE 이름을 특수문자 없이 입력하세요."
    default = "aws rt name"
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
