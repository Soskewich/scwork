FROM python:3.10
RUN apt-get update -y && apt-get install -y build-essential
WORKDIR /backend
COPY ./requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
COPY ./ /backend
