from python:3.8

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
CMD [ "flask", "run" ]
