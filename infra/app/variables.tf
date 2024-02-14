variable "namespace" {
  type    = string
  default = "com-delta"
}

variable "image" {
  type = object({
    repository = string
    pullPolicy = string
  })
}

variable "replicaCount" {
  type    = number
  default = 1
}

variable "external_mysql" {
  type = object({
    endpoint = string
    database = string
    username = string
    password = string
  })
}

variable "internal_mysql" {
  type = object({
    endpoint = string
    database = string
    username = string
    password = string
  })
}

variable "ingress" {
  type = object({
    external = object({
      fqdn = string
    })
  })
}

variable "resources" {
  type = object({
    limits = object({
      cpu    = string
      memory = string
    })
    requests = object({
      cpu    = string
      memory = string
    })
  })
}

variable "rabbitmq_url" {
  type = string
}
