FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/frtest/frtest

COPY requirements.txt /usr/src/frtest

RUN pip install --no-cache-dir -r /usr/src/frtest/requirements.txt