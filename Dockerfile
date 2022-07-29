FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
RUN apt update && apt install -y PACKAGE && rm -rf /var/lib/apt/lists/*
RUN apt install python3-dev
RUN apt install libmysqlclient-dev

COPY ./core /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
