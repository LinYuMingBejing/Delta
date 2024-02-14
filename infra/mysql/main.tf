locals {
  database = "delta"
  username = "delta"
}

resource "random_password" "root_user_password" {
  length  = 12
  special = false
}

resource "random_password" "delta_user_password" {
  length  = 12
  special = false
}


resource "kubernetes_secret" "mysql_secret" {

  metadata {
    name = "mysql-secret"
  }

  data = {
    MYSQL_ROOT_PASSWORD = random_password.root_user_password.result,
    MYSQL_DATABASE      = local.database,
    MYSQL_USER          = local.username,
    MYSQL_PASSWORD      = random_password.delta_user_password.result,
  }
}

resource "kubernetes_persistent_volume_claim" "mysql_pvc" {

  metadata {
    name = "mysql-pvc"
  }

  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "10Gi"
      }
    }
  }
}

resource "kubernetes_deployment" "mysql_deployment" {
  depends_on = [kubernetes_persistent_volume_claim.mysql_pvc]

  metadata {
    name = "mysql-deployment"
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "mysql"
      }
    }

    template {
      metadata {
        labels = {
          app = "mysql"
        }
      }

      spec {
        container {
          name  = "mysql"
          image = "mysql:latest"
          env {
            name = "MYSQL_ROOT_PASSWORD"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.mysql_secret.metadata[0].name
                key  = "MYSQL_ROOT_PASSWORD"
              }
            }
          }
          env {
            name = "MYSQL_DATABASE"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.mysql_secret.metadata[0].name
                key  = "MYSQL_DATABASE"
              }
            }
          }
          env {
            name = "MYSQL_USER"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.mysql_secret.metadata[0].name
                key  = "MYSQL_USER"
              }
            }
          }
          env {
            name = "MYSQL_PASSWORD"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.mysql_secret.metadata[0].name
                key  = "MYSQL_PASSWORD"
              }
            }
          }
          volume_mount {
            name       = "mysql-data"
            mount_path = "/var/lib/mysql"
          }
        }

        volume {
          name = "mysql-data"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.mysql_pvc.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "mysql_service" {
  depends_on = [kubernetes_deployment.mysql_deployment]

  metadata {
    name = "mysql-service"
  }

  spec {
    selector = {
      app = kubernetes_deployment.mysql_deployment.spec[0].template[0].metadata[0].labels["app"]
    }

    port {
      protocol    = "TCP"
      port        = 3306
      target_port = 3306
    }
  }
}
