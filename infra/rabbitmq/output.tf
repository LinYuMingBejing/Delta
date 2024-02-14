output "rabbitmq_credentials" {
  value = {
    username = local.username,
    password = random_password.rabbitmq_password.result
  }
}

output "rabbitmq_service_hostname" {
  value = kubernetes_service.rabbitmq_service.metadata.0.name
}
