FROM docker.io/python:latest AS BASE

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# CMD python manage.py runserver 0.0.0.0:8000


