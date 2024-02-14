locals {
  username = "delta"
}

resource "random_password" "rabbitmq_password" {
  length  = 12
  special = false
}

resource "kubernetes_secret" "rabbitmq_secret" {

  metadata {
    name = "rabbitmq-secret"
  }

  data = {
    RABBITMQ_DEFAULT_USER = local.username,
    RABBITMQ_DEFAULT_PASS = random_password.rabbitmq_password.result,
  }
}

resource "kubernetes_deployment" "rabbitmq_deployment" {

  metadata {
    name = "rabbitmq-deployment"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "rabbitmq"
      }
    }

    template {
      metadata {
        labels = {
          app = "rabbitmq"
        }
      }

      spec {
        container {
          name  = "rabbitmq"
          image = "rabbitmq:management"
          env {
            name = "RABBITMQ_DEFAULT_USER"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.rabbitmq_secret.metadata[0].name
                key  = "RABBITMQ_DEFAULT_USER"
              }
            }
          }
          env {
            name = "RABBITMQ_DEFAULT_PASS"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.rabbitmq_secret.metadata[0].name
                key  = "RABBITMQ_DEFAULT_PASS"
              }
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "rabbitmq_service" {
  depends_on = [kubernetes_deployment.rabbitmq_deployment]

  metadata {
    name = "rabbitmq-service"
  }

  spec {
    selector = {
      app = kubernetes_deployment.rabbitmq_deployment.spec[0].template[0].metadata[0].labels["app"]
    }

    port {
      name        = "rabbitmq"
      protocol    = "TCP"
      port        = 5672
      target_port = 5672
    }

    port {
      name        = "management"
      protocol    = "TCP"
      port        = 15672
      target_port = 15672
    }
  }
}
