FROM bitnami/python:3.8

RUN apt-get update \
 && apt-get install redis-server sqlite3 -y --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1001 app && useradd -r -u 1001 -g app app
RUN mkdir /home/app && chown 1001 /home/app
USER 1001
WORKDIR /app

#COPY src/tipboard src/tipboard
#COPY src/manage.py src/manage.py

COPY src/ src/

COPY requirements.txt .
COPY entrypoint.sh entrypoint.sh

ENV PATH="/home/app/.local/bin:${PATH}"
RUN pip install --upgrade pip &&  pip install --user -r requirements.txt

EXPOSE 8080

CMD ["bash", "entrypoint.sh"]
