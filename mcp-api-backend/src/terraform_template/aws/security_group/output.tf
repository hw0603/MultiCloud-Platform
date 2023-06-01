output "security_group_id" {
    value = aws_security_group.security_group.id
    description = "security group의 ID 정보입니다."
}

output "vpc_id" {
    value = aws_security_group.security_group.vpc_id
    description = "security group와 연결된 VPC의 ID 정보입니다."
}

output "security_group_owner" {
    value = aws_security_group.security_group.owner_id
    description = "security group을 소유하고 있는 계정 ID입니다."
}

output "security_group_ingress" {
    value = aws_security_group.security_group.ingress
    description = "security group의 ingress 정보입니다."
}

output "security_group_egress" {
    value = aws_security_group.security_group.egress
    description = "security group의 egress 정보입니다."
}