output "nat_gateway_id" {
    value = aws_nat_gateway.nat_gateway.id
    description = "nat gateway의 ID 정보입니다."
}

output "eip_IP" {
    value = aws_eip.nat_gateway.address
    description = "elastic IP 주소 정보입니다."
}

output "igw_id" {
    value = data.aws_internet_gateway.selected_igw.id
    description = "nat gateway와 종속된 internet gateway ID 정보입니다."
}

output "subnet_id" {
    value = data.aws_subnet.selected_subnet.id
    description = "nat gateway가 연결된 subnet id 정보입니다."
}
