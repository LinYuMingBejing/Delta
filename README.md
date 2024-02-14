# Delta Energy Task
## Description:  
* I am an online clothing retailer, selling various sizes and types of clothing. I currently want to manage the inventory status of my store through a backend system.

| Name        | Code   |  Category |  Size  |  Unit Price |  Inventory  |Color    |
| --------    | :-----:| :----:    | :----: | :----:      | :----:      | :----:  |
| Star        | A-001  |  cloth    | S/M    | 200         | 20          | Red/Blue|
| Moon        | A-002  |  cloth    | S/M/L  | 300         | 10          | Red/White|
| Eagle       | B-001  |  plants   | L      | 100         | 23          | Green|
| Bird        | B-002  |  plants   | S/L    | 50          | 12          | Black|

## Prerequisites: Terraform, Docker, MySQL in local

```
$ brew install terraform
```
## Start the application
### First, expose the MySQL port in local
```
$ ngork 3306
```
* You will get the new mysql endpoint
![](https://ibb.co/8DfppJW)

### Replace the values of external_mysql in delta.tfvars
```
$ vim delta.tfvars
```

### Start the project
```
$ terraform init
$ terraform apply -var-file=delta.tfvars
```

### Enable ingress
```
$ minikube addons enable ingress
$ minikube tunnel
```

## MAC M1 Ingress not work
```
https://github.com/kubernetes/minikube/issues/13510
$ vim /etc/hosts/
127.0.0.1 www.delta.com
```

### Local Test
```
eval $(minikube -p minikube docker-env)
cd docker
sudo docker-compose up --build -d
```

### DB Migration
```
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```


## API Test
1. Create category
 ```curl -X POST \
    http://www.delta.com/category \
    -H "Content-Type: application/json" \
    -H "X-DSEBD-AGENT: AGENT_1" \
    -H "HOST: www.deltaww-energy.com" \
    -d '{"name": "plants"}'
  ```
  Response
  ```{"code":201,"data":{"id":1,"name":"plants"}}```
2. Get category
  ```
    curl -X GET \
    http://www.delta.com/color \
    -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
    -H "Referer: www.svc.deltaww-energy.com" \
    -H "HOST: www.deltaww-energy.com"
  ```
curl -X GET \
    http://localhost:8080/color \
    -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
    -H "Referer: www.svc.deltaww-energy.com" \
    -H "HOST: www.deltaww-energy.com"


curl -X POST \
  http://localhost:8080/cloth \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"name": "NET", "code": "Taiwan", "unit_price":"300", "category_id":4}'

curl -X PUT \
  http://localhost:5000/cloth/1 \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"name": "NET", "code": "SKII", "unit_price":"300", "category_id":1}'

curl -X GET \
  http://localhost:8080/cloth/1 \
  -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
  -H "Referer: www.svc.deltaww-energy.com" \
  -H "HOST: www.deltaww-energy.com"

curl -X POST \
  http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"cloth_id": 1, "color_id": 1, "size_id":2, "quantity":-1}'

curl -X POST \
  http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"cloth_id": 1, "color_id": 1, "size_id":2, "quantity":-1}'

curl -X GET \
  http://localhost:5000/inventory/cloth/1 \
  -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
  -H "Referer: www.svc.deltaww-energy.com" \
  -H "HOST: www.deltaww-energy.com"






