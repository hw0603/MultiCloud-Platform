output "vpc_id" {
    value = aws_vpc.vpc.id
    description = "vpc의 ID 정보입니다."
}

output "cidr_ip" {
    value = aws_vpc.vpc.cidr_block
    description = "vpc의 cidr 정보입니다."
}

output "owner_id" {
    value = aws_vpc.vpc.owner_id
    description = "vpc를 소유하고 있는 계정 ID입니다."
}