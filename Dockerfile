FROM python:3.9-alpine
 
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./app /app

RUN chmod a+x /app/docker-entrypoint.sh
WORKDIR /app

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
