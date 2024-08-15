FROM python:3.11
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY /requirements .
RUN pip install --upgrade pip
RUN pip install -r base.txt

WORKDIR /code
COPY . .
RUN python manage.py collectstatic --noinput
