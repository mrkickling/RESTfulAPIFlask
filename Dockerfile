from python:3.9.7

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app app

EXPOSE 8080

CD app
CMD export FLASK_APP=app
RUN flask run -p 8080