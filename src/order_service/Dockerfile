FROM python:3.9-slim

RUN apt-get update

RUN pip install --upgrade pip

COPY requirements.txt /

RUN pip install -r requirements.txt

ENV PYTHONPATH "/"

COPY order_service_consumer.py variables.py /

ENTRYPOINT ["python", "order_service_consumer.py"]