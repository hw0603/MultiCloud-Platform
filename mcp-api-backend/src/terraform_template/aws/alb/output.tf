output "alb_id" {
    value = aws_alb.alb.id
    description = "alb의 ID 정보입니다."
}

output "alb_arn" {
    value = aws_alb.alb.arn
    description = "alb의 ARN 정보입니다."
}

output "alb_target_group" {
    value = aws_alb_target_group.alb_target_group.id
    description = "alb target group의 ID 정보입니다."
}

output "alb_target_group_arn" {
    value = aws_alb_target_group.alb_target_group.arn
    description = "alb target group의 ARN 정보입니다."
}

