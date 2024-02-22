image = {
  repository = "docker-flask"
  pullPolicy = "Never"
}

resources = {
  limits = {
    cpu    = "200m"
    memory = "100Mi"
  }
  requests = {
    cpu    = "100m"
    memory = "50Mi"
  }
}

ingress = {
  external = {
    ingressClass = "nginx-external"
    fqdn         = "www.deltaww-energy.com"
  }
}

external_mysql = {
  endpoint = "localhost:3306"
  database = "demo8"
  username = "root"
  password = "root"
}
