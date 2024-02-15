resource "null_resource" "build_image" {
  provisioner "local-exec" {
    command = "eval $(minikube -p minikube docker-env) && cd ../docker &&  docker-compose up --build -d"
  }
}
