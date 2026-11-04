#DOCKER  BUILDER IMAGE 
FROM python:3.11-slim AS builder
WORKDIR /build

COPY ./requirement.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirement.txt

#DOCKER FINAL IMAGE
FROM python:3.11-slim
WORKDIR /code

copy --from=builder /install /usr/local


COPY ./app /code/app 

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]