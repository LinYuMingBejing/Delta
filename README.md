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
a. Request 
 ```curl -X POST \
    http://www.delta.com/category \
    -H "Content-Type: application/json" \
    -H "X-DSEBD-AGENT: AGENT_1" \
    -H "HOST: www.deltaww-energy.com" \
    -d '{"name": "plants"}'
  ```
b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 201        | ``` {"code":201,"data":{"id":1,"name":"plants"}} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 415        | ``` {"code":415,"message":"Unsupported Media Type."} ```  |  
| 422        | ``` {"code":422,"message":"Invalid input type."} ```  |  
  
2. Get category
a. Request
  ```
    curl -X GET \
    http://www.delta.com/category/1 \
    -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
    -H "Referer: www.svc.deltaww-energy.com" \
    -H "HOST: www.deltaww-energy.com"
  ```
b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 200        | ``` {"code":200,"data":{"id":1,"name":"plants"}} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 403        | ``` {"code":403,"message":"Forbidden."} ```  | 
| 404        | ``` {"code":404,"message":"Not Found."} ```  | 

3. Update category
a. Request 
```curl -X PUT \
    http://www.delta.com/category/1 \
    -H "Content-Type: application/json" \
    -H "X-DSEBD-AGENT: AGENT_1" \
    -H "HOST: www.deltaww-energy.com" \
    -d '{"name": "cloth"}'
```
b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 201        | ``` {"code":201,"data":{"id":1,"name":"plants"}} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 404        | ``` {"code":404,"message":"Not Fonud"} ```  |  
| 415        | ``` {"code":415,"message":"Unsupported Media Type."} ```  |  
| 422        | ``` {"code":422,"message":"Invalid input type."} ```  |  


4. Delete category
a. Request 
```curl -X DELETE \
    http://www.delta.com/category/1 \
    -H "X-DSEBD-AGENT: AGENT_1" \
    -H "HOST: www.deltaww-energy.com" \
```
b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 201        | ``` {"code":201,"data":{"id":1,"name":"plants","message":"The action was performed successfully."}} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 404        | ``` {"code":404,"message":"Not Fonud"} ```  |  


5. Create cloth
a. Request
```
curl -X POST \
  http://www.delta.com/cloth \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"name": "Star", "code": "A-001", "unit_price":"300", "category_id":1}'
```
b. Response

|  Status Code  | Message    |
| --------    | :-----:| 
| 201        | ``` {"code":201,"data":{"category":"plants","code":"A-001","id":3,"name":"Star","unit_price":300},"message":"The action was performed successfully."} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 415        | ``` {"code":415,"message":"Unsupported Media Type."} ```  |  
| 422        | ``` {"code":422,"message":"Invalid input type."} ```  |  

6. Update cloth
a. Request
```
curl -X PUT \
  http://www.delta.com/cloth/3 \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"name": "Star2", "code": "A-001", "unit_price":"300", "category_id":1}'
```

b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 201        | ``` {"code":201,"data":{"category":"plants","code":"A-001","id":3,"name":"Star2","unit_price":300},"message":"The action was performed successfully."} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 415        | ``` {"code":415,"message":"Unsupported Media Type."} ```  |  
| 422        | ``` {"code":422,"message":"Invalid input type."} ```  |  

7. Query cloth
a. Request
```
curl -X GET \
  http://www.delta.com/cloth/3 \
  -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
  -H "Referer: www.svc.deltaww-energy.com" \
  -H "HOST: www.deltaww-energy.com"
```
b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 200        | ``` {"code":200,"data":{"category":"plants","code":"A-001","id":3,"name":"Star2","unit_price":300}} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 403        | ``` {"code":403,"message":"Forbidden."} ```  | 
| 404        | ``` {"code":404,"message":"Not Found."} ```  | 

8. Create inventory
a. Request
```
curl -X POST \
  http://www.delta.com/inventory/ \
  -H "Content-Type: application/json" \
  -H "X-DSEBD-AGENT: AGENT_1" \
  -H "HOST: www.deltaww-energy.com" \
  -d '{"cloth_id": 3, "color_id": 1, "size_id":2, "quantity":100}'
```

b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 201        | ``` {"code":201,"data":{"cloth_id":1,"color_id":1,"id":2,"quantity":20,"size_id":3},"message":"The action was performed successfully."} ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 415        | ``` {"code":415,"message":"Unsupported Media Type."} ```  |  
| 422        | ``` {"code":422,"message":"Invalid input type."} ```  |  

8. Query inventory

a. Request
```
curl -X GET \
  http://www.delta.com/inventory/cloth/1 \
  -H "Cookie: expires=Mon, 04 Dec 2024 08:18:32 GMT; domain=www.deltaww-energy.com" \
  -H "Referer: www.svc.deltaww-energy.com" \
  -H "HOST: www.deltaww-energy.com"
```

b. Response
|  Status Code  | Message    |
| --------    | :-----:| 
| 200        | ``` {"code":200,"data":[{"cloth_name":"NET","color_name":"\u7d05\u8272","inventory":300,"inventory_id":1,"size_name":"M"}] ```  |  
| 400        | ``` {"code":400,"message":"Bad Request."} ```  |
| 401        | ``` {"code":401,"message":"Unauthorized."} ```  |  
| 403        | ``` {"code":403,"message":"Forbidden."} ```  | 
| 404        | ``` {"code":404,"message":"Not Found."} ```  | 




