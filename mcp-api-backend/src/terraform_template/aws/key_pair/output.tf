output "key_pair_id" {
    value = aws_key_pair.web_admin.id
    description = "key pair의 ID 정보입니다."
}

output "key_pair_arn" {
    value = aws_key_pair.web_admin.arn
    description = "key pair의 ARN 정보입니다."
}

output "public_key" {
    value = aws_key_pair.web_admin.public_key
    description = "public key 정보입니다."
}
