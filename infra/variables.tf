variable "image" {
  type = object({
    repository = string
    pullPolicy = string
  })
}

variable "external_mysql" {
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
