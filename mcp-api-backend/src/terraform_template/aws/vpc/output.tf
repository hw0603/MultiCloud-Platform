output "vpc_id" {
    value = aws_vpc.vpc.id
}

output "cidr_ip" {
    value = aws_vpc.vpc.cidr_block
}

output "owner_id" {
    value = aws_vpc.vpc.owner_id
}