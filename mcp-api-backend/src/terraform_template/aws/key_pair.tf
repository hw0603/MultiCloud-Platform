resource "tls_private_key" "pk" {
    algorithm = "RSA"
    rsa_bits = 4096
}

resource "aws_key_pair" "web_admin" {
    key_name = var.aws_key_name
    public_key = tls_private_key.pk.public_key_openssh
}
