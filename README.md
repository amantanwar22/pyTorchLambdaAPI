# AWS Lambda + PyTorch (Container Image Method) + Parameterized API

URL - https://xn4qvsoz7st5oog64jd2pdhl2y0sxmzf.lambda-url.ap-south-1.on.aws/ 

## 1. Objective

The goal of this task was to successfully run PyTorch inside AWS Lambda. Because PyTorch is extremely large (>700MB) and requires system-level math libraries, it cannot be loaded as a standard Lambda Layer (which has a 250MB limit).

Instead, we used the Lambda Container Image method, packaging the code and dependencies into a Docker image and deploying it via Amazon ECR. We then exposed the function via a public Function URL to act as an API that accepts query parameters.

## 2. Why Container Images for PyTorch?

Size Limits: Lambda Layers are limited to 250MB (unzipped). PyTorch is far larger. Container images allow up to 10GB.

System Dependencies: PyTorch requires system libraries like libgomp, blas, and lapack. These are missing in standard Lambda runtimes but can be installed easily in a Docker container.

Cross-Platform Consistency: Docker ensures the code runs on AWS (Linux/AMD64) exactly as it does locally, even when building from a Mac (ARM64).

## 3. Building the PyTorch Image (Docker Method)

Step 1 — Create Project Files
Create a folder and add the following two files.

File 1: app.py

File 2: Dockerfile

Step 2 — Build the Image (Mac/Cross-Platform Fix)

We use a specific build command to ensure compatibility with AWS Lambda (which expects AMD64 architecture and standard Docker manifests).

### docker buildx build --platform linux/amd64 --provenance=false --load -t pytorch-lambda .

--platform linux/amd64: Ensures it runs on AWS servers, not just Mac chips.

--provenance=false: Forces the classic image format that AWS supports.

## 4. Upload Image to Amazon ECR
Step 1 — Create Repository

Go to AWS Console → ECR → Create Repository.

 Name: pytorch-lambda-api Copy the URI (e.g., 020211321234.dkr.ecr.ap-south-1.amazonaws.com/pytorch-lambda-api).

Step 2 — Login and Push
Run these commands in your terminal:

# 1. Login to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <YOUR_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com

# 2. Tag the image
docker tag pytorch-lambda:latest <YOUR_ECR_URI>:latest

# 3. Push to AWS
docker push <YOUR_ECR_URI>:latest

## 5. Create Lambda Function
Go to AWS Console → Lambda → Create Function.

Select Container Image .

Name: pytorch-api

Container Image URI: Browse and select the image you just pushed to ECR.

Architecture: x86_64.

Click Create.

6. Create API Endpoint (Function URL)
Go to Configuration → Function URL.

Click Create function URL.

Auth type: NONE (Public).

Click Save.

## Output

Below are three output tests

A) Output without query param (Defaults to 2)

https://xn4qvsoz7st5oog64jd2pdhl2y0sxmzf.lambda-url.ap-south-1.on.aws/

![Output](./out19.png)

B) Output with query param (?number=10)

https://xn4qvsoz7st5oog64jd2pdhl2y0sxmzf.lambda-url.ap-south-1.on.aws/?number=10

![Output](./out20.png)

C) Output with Invalid Input (?number=abc) 

https://xn4qvsoz7st5oog64jd2pdhl2y0sxmzf.lambda-url.ap-south-1.on.aws//?number=abc

![Output](./out21.png)