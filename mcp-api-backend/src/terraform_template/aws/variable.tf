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


# subnet
variable "aws_subnet_name" {
    type = string
    description = "SUBNET 이름을 특수문자 없이 입력하세요."
    default = "aws subnet name"
}
