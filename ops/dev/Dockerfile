# pull official base image
FROM python:3.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installing dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libpq-dev netcat-openbsd gcc && \
    apt-get clean

# Install app dependencies
RUN pip install --upgrade pip
COPY  requirements ./requirements
RUN pip install -r requirements/dev.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/ops/dev/entrypoint.sh"]
