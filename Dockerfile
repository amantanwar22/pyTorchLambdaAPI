FROM public.ecr.aws/lambda/python:3.10

# 1. Install system libraries required by PyTorch CPU
RUN yum -y install blas-devel lapack-devel libgomp

# 2. Install PyTorch (CPU version to save space)
RUN pip install torch==1.13.1 --no-cache-dir --index-url https://download.pytorch.org/whl/cpu

# 3. Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# 4. Set the command handler
CMD ["app.lambda_handler"]