resource "aws_security_group" "security_group" {
  name = var.aws_security_group_name
  vpc_id = aws_vpc.vpc.id
  ingress {
    from_port = var.aws_inbound_from_port
    to_port = var.aws_inbound_to_port
    protocol = var.aws_inbound_protocol
    cidr_blocks = [var.aws_inbound_cidr]
  }

  egress {
    from_port = var.aws_outbound_from_port
    to_port = var.aws_outbound_to_port
    protocol = var.aws_outbound_protocol
    cidr_blocks = [var.aws_outbound_cidr]
  }
}