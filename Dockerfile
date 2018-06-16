FROM python:3

ADD . /app
WORKDIR /app

RUN pip install .
CMD ["python3", "main.py"]
