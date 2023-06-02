output "route_rule_id" {
    value = aws_route.route_rule.id
    description = "route rule의 ID 정보입니다."
}

output "route_table_id" {
    value = aws_route.route_rule.route_table_id
    description = "연결된 route table의 ID 정보입니다."
}

output "igw_id" {
    value = aws_route.route_rule.gateway_id
    description = "연결된 internet gateway의 ID 정보입니다."
}
