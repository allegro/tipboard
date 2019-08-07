FROM bitnami/python:3.7

RUN apt-get update && apt-get install redis-server -y

RUN groupadd -g 1001 app && useradd -r -u 1001 -g app app
RUN mkdir /home/app && chown 1001 /home/app
USER 1001
WORKDIR /app

#Do we really have to put this on CDN ? :(
ADD static ./static

#You can override config in ./tipboard/Config/*
ADD ./tipboard ./tipboard

ADD ./templates ./templates
ADD ./webserver ./webserver
ADD ./manage.py ./manage.py
ADD ./entrypoint.sh ./entrypoint.sh

ADD requirements.txt .
RUN pip install --user -r requirements.txt

EXPOSE 8080

CMD ["bash", "entrypoint.sh"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"]