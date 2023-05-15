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
    security_groups = data.aws_security_groups.selected_security_group.ids
    subnet_id = data.aws_subnet.selected_subnet.id
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

# Dependency
data "aws_security_groups" "selected_security_group" {
    filter {
        name   = "tag:Name"
        values = var.aws_security_group_name
    }
}

data "aws_subnet" "selected_subnet" {
  filter {
    name   = "tag:Name"
    values = [var.aws_subnet_name]
  }
}


# Provider setting
provider "aws" {
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
    region = var.aws_region
}

terraform {
    required_version = ">=1.0.0"
}