FROM python:3.12-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /project

RUN chmod 777 /project

COPY requirements.txt /project/
RUN pip install -r /project/requirements.txt

COPY . /project

WORKDIR /project
