# MCP에서 내부적으로 remote-state를 사용하므로 terraform 코드에서는 별도의 backend를 사용하지 않아도 됨
# terraform backend 설정 예시

terraform {
    backend "http" {
        address = "http://localhost:8080/terraform_state/{id}"
        lock_address = "http://localhost:8080/terraform_lock/{id}"
        lock_method = "PUT"
        unlock_address = "http://localhost:8080/terraform_lock/{id}"
        unlock_method = "DELETE"
    }
}

provider "aws" {
    region = "${var.region}"
}
