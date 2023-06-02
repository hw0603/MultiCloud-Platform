output "instance_id" {
    value = aws_instance.bastion.id
    description = "instance의 ID 정보입니다."
}

output "instance_arn" {
    value = aws_instance.bastion.arn
    description = "instance의 ARN 정보입니다."
}

output "instance_ip" {
    value = aws_eip.bastion.address
    description = "instance에 할당된 adress입니다."
}

output "subnet_id" {
  value = aws_instance.bastion.subnet_id
  description = "aws instance이 연결된 subnet ID 정보입니다."
}