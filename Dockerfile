FROM node:current-alpine3.11
WORKDIR /app
COPY static/package.json /app
RUN npm install

FROM python:3.8

WORKDIR /app
COPY requirements.txt /app
COPY --from=0 /app/* /app/static/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install whois

ENV FLASK_APP=app.py
CMD [ "flask", "run", "--host", "0.0.0.0" ]
