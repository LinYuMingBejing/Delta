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
    fqdn         = "www.delta.com"
  }
}

external_mysql = {
  endpoint = "0.tcp.jp.ngrok.io:15832"
  database = "demo8"
  username = "root"
  password = "root"
}
