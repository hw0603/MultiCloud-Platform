output "route_table_id" {
    value = aws_route_table.rt.id
    description = "route table의 ID 정보입니다."
}

output "route_table_arn" {
    value = aws_route_table.rt.arn
    description = "route table의 ARN 정보입니다."
}

output "vpc_id" {
    value = aws_route_table.rt.vpc_id
    description = "route table이 연결된 vpc ID 정보입니다."
}

output "route_table_owner" {
    value = aws_route_table.rt.owner_id
    description = "route table을 소유하고 있는 계정 ID입니다."
}