# MicroCart
Scalable Microservice Architecture for E-Commerce

This project focuses on developing a backend system for a simple e-commerce platform using microservice architecture and AWS services. It implements various microservices, including User Management, Product and Cart Management. The project includes user authentication with JWT, product management with DynamoDB, and image storage on S3/localstack. The system will be containerized using Docker, deployed on AWS ECS with CloudWatch for application monitoring.


## USER SERVICE API 
http://13.48.31.12:8001/docs#/

![USER SERVICE API](api_user.png)


## PRODUCT SERVICE API 
http://13.48.31.12:8002/docs#/

![PRODUCT SERVICE API](api_product.png)


## CART SERVICE API 
http://13.48.31.12:8003/docs#/

![CART SERVICE API](api_cart.png)

## Monitoring
![ec2](ec2.png)

## example to test

### register user
![token](token_example_register.png)

### login and use token for other endpoints
![token](token_example_login.png)

