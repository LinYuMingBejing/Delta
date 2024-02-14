resource "null_resource" "start_minikube" {
  provisioner "local-exec" {
    command = "minikube start"
  }
}

resource "null_resource" "configure_kubeconfig" {
  depends_on = [null_resource.start_minikube]

  provisioner "local-exec" {
    command = "eval $(minikube -p minikube docker-env)"
  }
}

resource "null_resource" "install_addons" {
  depends_on = [null_resource.configure_kubeconfig]

  provisioner "local-exec" {
    command = "minikube addons enable dashboard"
  }
}

resource "null_resource" "check_minikube" {
  depends_on = [null_resource.install_addons]

  provisioner "local-exec" {
    command = "kubectl wait --for=condition=ready pod -l component=kube-controller-manager -n kube-system --timeout=5m"
  }
}
