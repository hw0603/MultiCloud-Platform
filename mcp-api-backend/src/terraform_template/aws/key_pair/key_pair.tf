# Key Pair
resource "tls_private_key" "pk" {
    algorithm = "RSA"
    rsa_bits = 4096
}

resource "aws_key_pair" "web_admin" {
    key_name = var.aws_key_name
    public_key = tls_private_key.pk.public_key_openssh
}

# Provider Setting
provider "aws" {
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
    region = var.aws_region
}

terraform {
    required_version = ">=1.0.0"
}