FROM python:3.10-buster

WORKDIR /code

RUN apt-get update
RUN python3 -m venv venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt
