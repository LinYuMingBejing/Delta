# Delta Energy Task
## Description:  
* I am an online clothing retailer, selling various sizes and types of clothing. I currently want to manage the inventory status of my store through a backend system.

| Name        | Code   |  Category |  Size  |  Unit Price |  Inventory  |Color    |
| --------    | :-----:| :----:    | :----: | :----:      | :----:      | :----:  |
| Star        | A-001  |  cloth    | S/M    | 200         | 20          | Red/Blue|
| Moon        | A-002  |  cloth    | S/M/L  | 300         | 10          | Red/White|
| Eagle       | B-001  |  plants   | L      | 100         | 23          | Green|
| Bird        | B-002  |  plants   | S/L    | 50          | 12          | Black|

## Architect
![Architect](https://i.imgur.com/Ll4WsA2.png)

## Folder Structrue
```
├── app
│   ├── api
│   │   ├── ....    => API related development
│   ├── settings
│   ├── utils
│   │   ├── middleware => Check header
│   ├── constant.py  
│   ├── exception.py => Exception class
│   ├── listener.py  => Celery config
│   ├── models.py    => Model config
│   ├── schema.py    => Define input schema
│   ├── task.py
├── chart            => K8S yaml
├── cmd              => DB init scripts
├── docker           => Build image scripts
├── infra            => Terraform related scripts
├── migrations       => DB Migrate
├── .gitignore
├── Dockerfile
├── .......
└── uwsgi.ini
```


## Prerequisites: Terraform, Docker, MySQL in local

```
$ brew install terraform
```
## Start the application
### First, expose the MySQL port in local
```
$ ngrok tcp 3306
```
* You will get the new mysql endpoint
![Expose](https://i.imgur.com/9mkfq5V.png)

### Replace the values of external_mysql in delta.tfvars
```
$ cd infra
$ vim delta.tfvars
```

### Start the project
```
$ cd infra
$ terraform init
$ terraform apply -var-file=delta.tfvars
```

### Enable ingress
```
$ minikube addons enable ingress
$ minikube tunnel
```

## MAC M1 Ingress not work
Issue: https://github.com/kubernetes/minikube/issues/13510
```
$ vim /etc/hosts/
127.0.0.1 www.delta.com
```

### Local Test
```
$ eval $(minikube -p minikube docker-env)
$ cd docker
$ sudo docker-compose up --build -d
```

### DB Migration
```
$ python3 manage.py db init
$ python3 manage.py db migrate
$ python3 manage.py db upgrade
```
## Delta Energy Unit Test
1. Redirect
* Request 
```
curl -L http://www.delta.com/dsebd/api/v1/resource \
    -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
    -H "Referer: www.svc.deltaww-energy.com" \
    -H "HOST: www.deltaww-energy.com"
```
* Response

|  Status Code  | Message    |
| --------    | -----| 
| 302        | {"code":302,"message":"Redirect successfully.","path":"/dsebd/api/v1/sta"} | 
| 400        | {"code":400,"message":"Bad Request."}  | 
| 401        | {"code":401,"message":"Unauthorized."}  |  
| 403        | {"code":403,"message":"Forbidden."}  | 

2. About Me
* Request 
```
curl http://www.delta.com/dsebd/about/me \
    -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
    -H "Referer: www.svc.deltaww-energy.com" \
    -H "HOST: www.deltaww-energy.com"
```
* Response

|  Status Code  | Message    |
| --------    | -----| 
| 200        | {"code":200,"message":"The action was performed successfully."} | 
| 400        | {"code":400,"message":"Bad Request."}  | 
| 401        | {"code":401,"message":"Unauthorized."}  |  
| 403        | {"code":403,"message":"Forbidden."}  | 

## DB CRUD Test
1. Create category
* Request 
 ```
 curl -X POST \
    http://www.delta.com/category \
    -H "Content-Type: application/json" \
    -H "X-DSEBD-AGENT: AGENT_1" \
    -H "HOST: www.deltaww-energy.com" \
    -d '{"name": "plants"}'
  ```
* Response

|  Status Code  | Message    |
| --------    | -----| 
| 201        |  {"code":201,"data":{"id":1,"name":"plants"}}  |  
| 400        |  {"code":400,"message":"Bad Request."}  |
| 401        |  {"code":401,"message":"Unauthorized."}  |  
| 415        |  {"code":415,"message":"Unsupported Media Type."}  |  
| 422        |  {"code":422,"message":"Invalid input type."}   |  
  
2. Get category
* Request
  ```
    curl -X GET \
    http://www.delta.com/category/1 \
    -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
    -H "Referer: www.svc.deltaww-energy.com" \
    -H "HOST: www.deltaww-energy.com"
  ```
* Response

|  Status Code  | Message    |
| --------    | -----| 
| 200        | {"code":200,"data":{"id":1,"name":"plants"}}  |  
| 400        | {"code":400,"message":"Bad Request."}  |
| 401        | {"code":401,"message":"Unauthorized."}  |  
| 403        | {"code":403,"message":"Forbidden."}  | 
| 404        | {"code":404,"message":"Not Found."}  | 

3. Update category
* Request 
```curl -X PUT \
    http://www.delta.com/category/1 \
    -H "Content-Type: application/json" \
    -H "X-DSEBD-AGENT: AGENT_1" \
    -H "HOST: www.deltaww-energy.com" \
    -d '{"name": "cloth"}'
```
* Response

|  Status Code  | Message    |
| --------    | -----| 
| 201        |  {"code":201,"data":{"id":1,"name":"plants"}}   |  
| 400        |  {"code":400,"message":"Bad Request."}   |
| 401        |  {"code":401,"message":"Unauthorized."}   |  
| 404        |  {"code":404,"message":"Not Fonud"}  |  
| 415        |  {"code":415,"message":"Unsupported Media Type."}  |  
| 422        |  {"code":422,"message":"Invalid input type."}  |  


4. Delete category
* Request 
```curl -X DELETE \
    http://www.delta.com/category/1 \
    -H "X-DSEBD-AGENT: AGENT_1" \
    -H "HOST: www.deltaww-energy.com" \
```
* Response

|  Status Code  | Message    |
| --------    | -----| 
| 201        | {"code":201,"data":{"id":1,"name":"plants","message":"The action was performed successfully."}}  |  
| 400        | {"code":400,"message":"Bad Request."}  |
| 401        | {"code":401,"message":"Unauthorized."}  |  
| 404        | {"code":404,"message":"Not Fonud"} |  


5. Create cloth
* Request
```
curl -X POST \
  http://www.delta.com/cloth \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"name": "Star", "code": "A-001", "unit_price":"300", "category_id":1}'
```
* Response

|  Status Code  | Message    |
| --------    | -----| 
| 201        |  {"code":201,"data":{"category":"plants","code":"A-001","id":3,"name":"Star","unit_price":300},"message":"The action was performed successfully."}  |  
| 400        |  {"code":400,"message":"Bad Request."}   |
| 401        |  {"code":401,"message":"Unauthorized."}  |  
| 415        |  {"code":415,"message":"Unsupported Media Type."}  |  
| 422        |  {"code":422,"message":"Invalid input type."}  |  

6. Update cloth
* Request
```
curl -X PUT \
  http://www.delta.com/cloth/3 \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"name": "Star2", "code": "A-001", "unit_price":"300", "category_id":1}'
```

* Response

|  Status Code  | Message    |
| --------    | -------- | 
| 201        |  {"code":201,"data":{"category":"plants","code":"A-001","id":3,"name":"Star2","unit_price":300},"message":"The action was performed successfully."}   |  
| 400        |  {"code":400,"message":"Bad Request."}  |
| 401        |  {"code":401,"message":"Unauthorized."}   |  
| 415        |  {"code":415,"message":"Unsupported Media Type."}   |  
| 422        |  {"code":422,"message":"Invalid input type."}   |  

7. Query cloth
*. Request
```
curl -X GET \
  http://www.delta.com/cloth/3 \
  -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
  -H "Referer: www.svc.deltaww-energy.com" \
  -H "HOST: www.deltaww-energy.com"
```
*. Response
|  Status Code  | Message    |
| --------    | --------| 
| 200        |  {"code":200,"data":{"category":"plants","code":"A-001","id":3,"name":"Star2","unit_price":300}}  |  
| 400        |  {"code":400,"message":"Bad Request."}   |
| 401        |  {"code":401,"message":"Unauthorized."}   |  
| 403        |  {"code":403,"message":"Forbidden."}   | 
| 404        |  {"code":404,"message":"Not Found."}   | 

8. Create inventory
*. Request
```
curl -X POST \
  http://www.delta.com/inventory/ \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"cloth_id": 3, "color_id": 1, "size_id":2, "quantity":100}'
```

*. Response
|  Status Code  | Message    |
| --------    | --------| 
| 201        |  {"code":201,"data":{"cloth_id":1,"color_id":1,"id":2,"quantity":20,"size_id":3},"message":"The action was performed successfully."}   |  
| 400        |  {"code":400,"message":"Bad Request."}   |
| 401        |  {"code":401,"message":"Unauthorized."}   |  
| 415        |  {"code":415,"message":"Unsupported Media Type."}   |  
| 422        |  {"code":422,"message":"Invalid input type."}  |  

9. Query inventory

*. Request
```
curl -X GET \
  http://www.deltaww-energy.com/size \
  -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
  -H "Referer: www.svc.deltaww-energy.com" \
  -H "HOST: www.deltaww-energy.com"
```

*. Response
|  Status Code  | Message    |
| --------    | -----| 
| 200        | {"code":200,"data":[{"cloth_name":"NET","color_name":"RED","inventory":300,"inventory_id":1,"size_name":"M"}]   |  
| 400        |  {"code":400,"message":"Bad Request."}   |
| 401        |  {"code":401,"message":"Unauthorized."}   |  
| 403        |  {"code":403,"message":"Forbidden."}   | 
| 404        |  {"code":404,"message":"Not Found."}  | 




