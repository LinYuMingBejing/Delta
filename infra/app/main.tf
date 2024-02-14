resource "kubernetes_namespace" "delta-app" {
  metadata {
    name = "delta"
  }
}


resource "helm_release" "api_server" {
  name             = "api-server"
  namespace        = var.namespace
  create_namespace = true
  chart            = "${path.module}/../../chart"
  max_history      = 5

  values = [
    "${file("${path.module}/../../chart/values.yaml")}"
  ]

  set {
    name  = "image.repository"
    value = var.image.repository
    type  = "string"
  }

  set {
    name  = "image.pullPolicy"
    value = var.image.pullPolicy
    type  = "string"
  }

  set {
    name  = "replicaCount"
    value = var.replicaCount
    type  = "auto"
  }


  set {
    name  = "ingress.external.fqdn"
    value = var.ingress.external.fqdn
    type  = "string"
  }

  set {
    name  = "resources.limits.cpu"
    value = var.resources.limits.cpu
    type  = "string"
  }

  set {
    name  = "resources.limits.memory"
    value = var.resources.limits.memory
    type  = "string"
  }

  set {
    name  = "resources.requests.cpu"
    value = var.resources.requests.cpu
    type  = "string"
  }

  set {
    name  = "resources.requests.memory"
    value = var.resources.requests.memory
    type  = "string"
  }

  set {
    name  = "env.CELERY_BROKER_URL"
    value = var.rabbitmq_url
    type  = "string"
  }

  set {
    name  = "env.EXTERNAL_DB_ENDPOINT"
    value = var.external_mysql.endpoint
    type  = "string"
  }

  set {
    name  = "env.EXTERNAL_DB_DELTA"
    value = var.external_mysql.database
    type  = "string"
  }

  set {
    name  = "env.INTERNAL_DB_ENDPOINT"
    value = var.internal_mysql.endpoint
    type  = "string"
  }

  set {
    name  = "env.INTERNAL_DB_DELTA"
    value = var.internal_mysql.database
    type  = "string"
  }

  set_sensitive {
    name  = "secrets.EXTERNAL_DB_USERNAME"
    value = var.external_mysql.username
    type  = "string"
  }

  set_sensitive {
    name  = "secrets.EXTERNAL_DB_PASSWORD"
    value = var.external_mysql.password
    type  = "string"
  }

  set_sensitive {
    name  = "secrets.INTERNAL_DB_USERNAME"
    value = var.internal_mysql.username
    type  = "string"
  }

  set_sensitive {
    name  = "secrets.INTERNAL_DB_PASSWORD"
    value = var.internal_mysql.password
    type  = "string"
  }
}
