resource "aws_alb" "alb" {
  internal = false
  load_balancer_type = "application"
  security_groups = data.aws_security_groups.selected_security_groups.ids
  subnets = data.aws_subnets.selected_subnets.ids
  # true : ALB가 재생성되어야 할 때 새로운 ALB를 먼저 생성 후 예전 ALB를 지우도록
  lifecycle { create_before_destroy = true }
  enable_cross_zone_load_balancing = true
}

resource "aws_alb_target_group" "alb_target_group" {
  port = var.aws_alb_target_group_port
  protocol = var.aws_alb_target_group_protocol
  vpc_id = data.aws_vpc.selected_vpc.id

  tags = {
    Name = var.aws_alb_target_group_name
  }
}

resource "aws_alb_target_group_attachment" "instance" {
  target_group_arn = aws_alb_target_group.alb_target_group.arn
  target_id        = data.aws_instance.selected_instance.id
}

# Dependency
data "aws_vpc" "selected_vpc" {
    filter {
        name   = "tag:Name"
        values = [var.aws_vpc_name]
    }
}

data "aws_instance" "selected_instance" {
    filter {
        name   = "tag:Name"
        values = [var.aws_alb_target_instance_name]
    }
}

data "aws_security_groups" "selected_security_groups" {
    filter {
        name   = "tag:Name"
        values = var.aws_security_group_name_list
    }
}

data "aws_subnets" "selected_subnets" {
  filter {
    name   = "tag:Name"
    values = var.aws_subnet_name_list
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