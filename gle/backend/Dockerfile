FROM python:3.13-slim

WORKDIR /app

COPY requirements_docker.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y cron

COPY . .

# Copy crontab file and apply it
COPY cleaner /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron && crontab /etc/cron.d/mycron

RUN chmod +x start.sh

CMD [ "./start.sh" ]
