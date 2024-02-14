output "connection_info" {
  value = {
    endpoint = "${kubernetes_service.mysql_service.spec[0].cluster_ip}:3306"
    username = kubernetes_secret.mysql_secret.data["MYSQL_USER"],
    password = kubernetes_secret.mysql_secret.data["MYSQL_PASSWORD"],
    database = kubernetes_secret.mysql_secret.data["MYSQL_DATABASE"],
  }
  sensitive = true
}
