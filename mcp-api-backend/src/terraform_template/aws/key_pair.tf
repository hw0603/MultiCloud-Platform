resource "aws_key_pair" "web_admin" {
    key_name = var.aws_key_name
    public_key = var.aws_public_key_name
}
