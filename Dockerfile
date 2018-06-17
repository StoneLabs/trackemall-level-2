FROM python:3

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN pip install gunicorn

EXPOSE 2438


#CMD ["python", "app.py"]
CMD "gunicorn --bind 0.0.0.0:2438 app:app"
