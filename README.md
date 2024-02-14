
```
cd docker
sudo docker-compose up --build -d
```

```
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

``` 
terraform init
terraform apply -var-file=delta.tfvars
```
expose mysql port
```
ngork 3306
```


MAC M1 Ingress not work
```
https://github.com/kubernetes/minikube/issues/13510
vim /etc/hosts/
127.0.0.1 www.delta.com
```










