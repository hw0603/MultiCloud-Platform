output "subnet_id" {
    value = aws_route_table_association.rt_association.subnet_id
    description = "route table이 연결된 subnet의 ID 정보입니다."
}

output "route_table_id" {
    value = aws_route_table_association.rt_association.route_table_id
    description = "연결된 route table 의 ID 정보입니다."
}