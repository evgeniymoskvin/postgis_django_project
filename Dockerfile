FROM python:3.9.6

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt update && apt -qy install gcc redis poppler-utils
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y python3-gdal
RUN apt-get install -y binutils libproj-dev

WORKDIR /app

#RUN mkdir /app/static && mkdir /app/media
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /app

