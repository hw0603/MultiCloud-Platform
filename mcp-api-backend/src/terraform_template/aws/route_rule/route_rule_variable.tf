# Route Rule
variable "destination_cidr" {
  default = "0.0.0.0/0"
}

variable "aws_route_table_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws rt name"
}

variable "aws_internet_gateway_name" {
    type = string
    description = "INTERNET GATEWAY 이름을 특수문자 없이 입력하세요."
    default = "aws igw name"
}

# Provider setting

# region
variable "aws_region" {
    type = string
    default = "ap-northeast-2"
}