# 서브넷 ID
output "subnet_id" {
    value = aws_subnet.subnet.id
}

# 서브넷 arn
output "subnet_arn" {
    value = aws_subnet.subnet.arn
}

# 서브넷이 있는 vpc ID
output "subnet_vpc" {
    value = aws_subnet.subnet.vpc_id
}

# 서브넷 cidr
output "subnet_cidr" {
    value = aws_subnet.subnet.cidr_block
}

# 서브넷 owner ID
output "owner_id" {
    value = aws_subnet.subnet.owner_id
}