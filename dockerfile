FROM python:alpine

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/PY/BIN:$PATH"

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

