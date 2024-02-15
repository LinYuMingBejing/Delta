module "minukube" {
  source = "./minikube"
}

module "mysql" {
  source     = "./mysql"
  depends_on = [module.minukube]
}

module "rabbitmq" {
  source     = "./rabbitmq"
  depends_on = [module.minukube]
}

module "build" {
  source     = "./image"
  depends_on = [module.minukube]
}

module "delta" {
  source         = "./app"
  depends_on     = [module.mysql, module.rabbitmq, module.build]
  image          = var.image
  ingress        = var.ingress
  external_mysql = var.external_mysql
  internal_mysql = {
    endpoint = module.mysql.connection_info.endpoint
    username = module.mysql.connection_info.username
    password = module.mysql.connection_info.password
    database = module.mysql.connection_info.database
  }
  resources    = var.resources
  rabbitmq_url = "pyamqp://${module.rabbitmq.rabbitmq_credentials.username}:${module.rabbitmq.rabbitmq_credentials.password}@rabbitmq-service.default.svc.cluster.local"
}
