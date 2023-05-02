# EC2
resource "aws_eip" "bastion" {
    instance = aws_instance.bastion.id
    vpc = true
    tags = {
        Name = var.aws_bastion_eip
    }
}

resource "aws_instance" "bastion" {
    

}