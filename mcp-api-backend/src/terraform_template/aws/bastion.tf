# EC2
resource "aws_eip" "bastion" {
    instance = aws_instance.bastion.id
    vpc = true
    tags = {
        Name = var.aws_bastion_eip
    }
}

resource "aws_instance" "bastion" {
    ami = var.aws_bastion_ami
    instance_type = var.aws_bastion_instance_type
    security_group = [aws_security_group.security_group.id]
    subnet_id = aws_subnet.subnet1.id
    key_name = var.aws_bastion_key_name
    disable_api_termination = true
    root_block_device {
        volume_size = var.aws_bastion_volumne_size
        volume_type = "gp3"
        delete_on_termination = true
        tags = {
            Name = var.aws_bastion_ec2_name
        }
    }
    tags = {
        Name = var.aws_bastion_ec2_name
    }
}
