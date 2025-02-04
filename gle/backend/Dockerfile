FROM python:3.13-slim

WORKDIR /app

COPY requirements_docker.txt .

RUN pip install -r requirements_docker.txt

COPY . .

CMD ["python", "api.py"]
